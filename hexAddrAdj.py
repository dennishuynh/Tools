import sys

class HexAddrAdj():
    def __init__(self):
        self.input = ''
        self.output = ''
        self.baseAddr = ''  

    def parseCommands(self):
        if(len(sys.argv) < 2):
            print('Not enough arguments')
            sys.exit(1)
        else:
            for i in range(len(sys.argv)):
                if sys.argv[i] == '-i':
                    self.input = sys.argv[i+1]
                elif sys.argv[i] == '-o':
                    self.output = sys.argv[i+1]
                elif sys.argv[i] == '-b':
                    self.baseAddr = sys.argv[i+1]
            if self.input == '' or self.output == '' or self.baseAddr == '':
                print('ERROR: Missing mandatory arguments')
                sys.exit(1)
            self.main()
        
    def setCommands(self, inp, outp, addr):
        self.input = inp
        self.output = outp
        self.baseAddr = addr
        self.main()
    
    def asciiHex2Binary(self, byte):
        if byte == 'a' or byte == 'b' or byte == 'c' or byte == 'd' or byte == 'e' or byte == 'f':
            return (int(byte, 16) - int('a', 16)) + 10
        elif byte == 'A' or byte == 'B' or byte == 'C' or byte == 'D' or byte == 'E' or byte == 'F':
            return (int(byte, 16) - int('A', 16)) + 10
        elif int(byte, 16) >= int('0', 16) and int(byte, 16) <= int('9', 16):
            return int(byte, 16) - int('0', 16)
        
        
    def main(self):   
        inputFile = open(self.input, 'r')
        outputFile = open(self.output, 'w')
        
        upperBaseAddr = self.baseAddr[:4]
        
        upperBaseAddrValue = self.asciiHex2Binary(upperBaseAddr[0]) * 4096
        upperBaseAddrValue += self.asciiHex2Binary(upperBaseAddr[1]) * 256
        upperBaseAddrValue += self.asciiHex2Binary(upperBaseAddr[2]) * 16
        upperBaseAddrValue += self.asciiHex2Binary(upperBaseAddr[3])

        while(1):
            line = inputFile.readline()
            if not line:
                break 
            line = HexRecord(line)
            checkSum = 0
            check = 0
            
            #adjust address of line
            if line.type == '04':
                self.baseAddr = "%04x" % upperBaseAddrValue
                upperBaseAddrValue += 1
                line.data = self.baseAddr[:5]
                line.newLine()
                for i in range(1, 12, 2):
                    binaryValue = self.asciiHex2Binary(line.line[i]) * 16
                    binaryValue += self.asciiHex2Binary(line.line[i+1])
                    checkSum += binaryValue
                checkSum = -checkSum
                #convert checksum into correct hex value
                checkSum = hex(int(bin(checkSum & 0b1111111111111111), 2))
                newCheckSum = checkSum[-2:].upper()
#                 newCheckSum = "%2x" % checkSum
#                 line.line[i] = newCheckSum
                newLine = str(line.mark) + str(line.length) + str(line.loadOffset) + str(line.type) + str(line.data) + str(newCheckSum) + '\n'
                newLine = newLine.upper()
                check = 1
            if check == 1:
                outputFile.write(newLine)
            else:
                outputFile.write(line.line)
        outputFile.close()
        inputFile.close()
        
        
#used to parse each line of intel hex
class HexRecord():
    def __init__(self, line):
        self.line = line
        self.lengthLine = int(line[1:3], 16)
        self.mark = line[:1]
        self.length = line[1:3]
        self.loadOffset = line[3:7]
        self.type = line[7:9]
        self.data = line[9:9 + (2 * self.lengthLine)]
        self.checksum = line[-2:]
    def newLine(self):
        self.line = str(self.mark) + str(self.length) + str(self.loadOffset) + str(self.type) + str(self.data) + str(self.checksum)

        
if __name__ == "__main__":
    temp = HexAddrAdj()
    temp.parseCommands()