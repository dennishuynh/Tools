import sys
import ctypes

class SpliceBinFile():
    def __init__(self):
        self.input = ''
        self.output1 = ''
        self.output2 = ''
        self.spliceAfterByte = ''
        self.max_bytes_read_at_a_time = 8192
    
    def parseCommands(self):
        for i in range(len(sys.argv)):
            #output file 1
            if sys.argv[i] == '-o1':
                self.output1 = sys.argv[i+1]
                
            #output file 2
            elif sys.argv[i] == '-o2':
                self.output2 = sys.argv[i+1]
                
            #input file
            elif sys.argv[i] == '-i':
                self.input = sys.argv[i+1]
                
            #number of bytes to splice after
            elif sys.argv[i] == '-s':
                self.spliceAfterByte = int(sys.argv[i+1])
        if self.input == '' or self.output1 == '' or self.output2 == '' or self.spliceAfterByte == '':
            print('ERROR: missing required arguments')
            
    def main(self):
        if len(sys.argv) < 2:
            print('Not enough arguments')
            sys.exit(1)
        self.parseCommands()
        
        outputFile1 = open(self.output1, 'wb')
        outputFile2 = open(self.output2, 'wb')
        inputFile = open(self.input, 'rb')
        
        #read in number of bytes up to splice number and write to output 1
        while self.spliceAfterByte > 0:
            if self.spliceAfterByte > self.max_bytes_read_at_a_time:
                buffer = inputFile.read(self.max_bytes_read_at_a_time)
                if len(buffer) == 0:
                    break
                outputFile1.write(buffer)
                self.spliceAfterByte -= len(buffer)
            else:
                buffer = inputFile.read(self.spliceAfterByte)
                if len(buffer) == 0:
                    break
                outputFile1.write(buffer)
                self.spliceAfterByte -= len(buffer)
        
        #read in rest of file and write to output 2
        buffer = inputFile.read(self.max_bytes_read_at_a_time)
        while len(buffer) != 0:
            outputFile2.write(buffer)
            buffer = inputFile.read(self.max_bytes_read_at_a_time)
            
        inputFile.close()
        outputFile1.close()
        outputFile2.close()
        sys.exit(0)
        
        
temp = SpliceBinFile()
temp.main()