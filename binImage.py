import sys, struct

class BinImage():
    
    def __init__(self):
        self.buffer_height = 1030
        self.buffer_width = 1030
        self.buffer_size = self.buffer_height * self.buffer_width
        self.test_square_width = 30
        self.test_square_height = self.test_square_width
        self.major = 1
        self.minor = 2
        self.input = ''
        self.output = ''
        self.start = 0x0000
        
    def parseCommands(self):
        if(len(sys.argv) < 2):
            print('Not enough arguments')
            sys.exit(1)
        req = 0
        for i in range(1, len(sys.argv), 2):
            #output file
            if sys.argv[i] == '-o':
                self.output = sys.argv[i+1]
            
            #input file
            elif sys.argv[i] == '-i':
                self.input = sys.argv[i+1]
            
            #number of rows
            elif sys.argv[i] == '-r':
                self.rows = int(sys.argv[i+1])
                req += 1
                
            #number of columns
            elif sys.argv[i] == '-c':
                self.cols = int(sys.argv[i+1])
                req += 1
            
            #number of blinds
            elif sys.argv[i] == '-b':
                self.blinds = int(sys.argv[i+1])
                req += 1
                
            #value that test square is set to
            elif sys.argv[i] == '-v':
                self.value = int(sys.argv[i+1])
                req += 1
            
            #test square width
            elif sys.argv[i] == '-sw':
                #if * is passed in then test square is entire image
                if sys.argv[i+1] == '*':
                    self.test_square_width = self.buffer_width
                    self.test_square_height = self.buffer_height
                else:
                    self.test_square_width = int(sys.argv[i+1])
                    self.test_square_height = self.test_square_width
                    if self.test_square_width > self.buffer_width:
                        self.test_square_width = self.buffer_width
                    if self.test_square_height > self.buffer_height:
                        self.test_square_height = self.buffer_height
            
            #test square location
            elif sys.argv[i] == '-sl':
                if sys.argv[i+1] == 'ul' or sys.argv[i+1] == 'ml' or sys.argv[i+1] == 'll' or sys.argv[i+1] == 'ur' or sys.argv[i+1] == 'mr' or sys.argv[i+1] == 'lr':
                    self.test_square_location = sys.argv[i+1]
                else:
                    print('Invalid argument: ' + sys.argv[i+1])
                    sys.exit(1)
                req += 1
            
            #if creating a gain image
            elif sys.argv[i] == '-gain':
                self.start = 0x00A0
            
            else:
                print('Invalid argument ' + sys.argv[i])
                sys.exit(1)   
        
        #if required args arent given
        if req != 5:
            print('Usage: -r #rows -c #cols -b #blindrows -sl ul|ml|ll|ur|mr|lr|* [-sw #] -v # -o OutputFileName -i InputFileName [-gain]')
            sys.exit(1)
        
        if len(self.output) == 0:
            print('ERROR: You must specify an output file using the -o switch')
            sys.exit(1)
        
        self.calcLoc()
        self.main()
        
    def calcLoc(self):
        #set the top left coordinate of the test square
        if self.test_square_location == 'ul':
            self.x = 0
            self.y = self.blinds
        elif self.test_square_location == 'ml':
            self.x = 0
            self.y = ((self.rows-self.blinds) /2) - self.test_square_height + self.blinds
            #self.y = (self.rows/2) - self.test_square_height - self.blinds  #(self.rows/2) - (self.test_square_height/2) - self.blinds
        elif self.test_square_location == 'll':
            self.x = 0
            self.y = self.rows - self.test_square_height #- self.blinds 
        elif self.test_square_location == 'ur':
            self.x = self.cols - self.test_square_width
            self.y = self.blinds
        elif self.test_square_location == 'mr':
            self.x = self.cols - self.test_square_width
            self.y = ((self.rows-self.blinds) /2) - self.test_square_height + self.blinds
            #self.y = (self.rows/2) - self.test_square_height - self.blinds  #(self.rows/2) - (self.test_square_height/2) - self.blinds
        elif self.test_square_location == 'lr':
            self.x = self.cols - self.test_square_width
            self.y = self.rows - self.test_square_height #- self.blinds
    
    def setCommands(self, outp, inp, rows, cols, blinds, value, sw, sl, gain):
        self.output = outp
        self.input = inp
        self.rows = int(rows)
        self.cols = int(cols)
        self.blinds = int(blinds)
        self.value = int(value)
        self.test_square_location = sl
        self.calcLoc()
        if gain == 1:
            self.start = 0x00A0
        if sw == '*':
            self.test_square_width = self.buffer_width
            self.test_square_height = self.buffer_height
        else:
            self.test_square_width = sw
            self.test_square_height = self.test_square_width
            if self.test_square_width > self.buffer_width:
                self.test_square_width = self.buffer_width
            if self.test_square_height > self.buffer_height:
                self.test_square_height = self.buffer_height
        self.main()
        
    def main(self):
        outputFile = open(self.output, 'wb')
        
        #initialize buffer
        buffer = [[self.start for x in range(self.buffer_height)] for x in range(self.buffer_width)]
            
        #read input into buffer
        if self.input != '':
            inputFile = open(self.input, 'rb')
            for row in range(self.blinds + self.rows):
                buf = inputFile.read(self.cols*2)
                for col in range(self.cols):
                    val = struct.unpack('>h', buf[2*col:2*col+2])[0]
                    buffer[row][col] = val
                
                
        #set test square to input value
        for row in range(self.blinds + self.rows):
            if row >= self.y and row < (self.y + self.test_square_height):
                for col in range(self.x, self.x + self.test_square_width):
                    buffer[row][col] = self.value
                    
            #to output text image
#             temp = str(buffer[row][:self.cols]).replace('[', '').replace(']', '').replace(',', '').strip('\n').strip('\r')
#             outputFile.write(temp)
#             outputFile.write('\n')

            #grab just size of requested image from buffer
            temp = buffer[row][:self.cols]
            temp1 = ''
            #convert hex values into bytes and write to file
            for i in temp:
                if i != self.start:
                    if i > 32767 or i < -32767 :
                        temp1 = struct.pack('>i', i)[2:]
                    else:
                        temp1 = struct.pack('>h', i)
                    outputFile.write(temp1)
                else:
                    temp1 = struct.pack('<h', i)
                    outputFile.write(temp1)
        outputFile.close()
        
if __name__ == "__main__":
    #initialize object and run
    binImg = BinImage()
    binImg.parseCommands()