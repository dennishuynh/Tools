import sys
from os import SEEK_END
from os import SEEK_SET

class Bin2hex():
    def __init__(self):
        self.bmp_Header = 32
        self.bytes_per_line = 32
        self.palette_offset = 0x1FC00
        
    def parseCommands(self):
        if len(sys.argv) < 2:
            print('Not enough arguments')
            sys.exit(1)
        else:
            self.input = sys.argv[1]
            self.output = sys.argv[2]
            self.main()
            
    def setCommands(self, inp, outp):
        self.input = inp
        self.output = outp
        self.main()
    
    def hexOutBytes(self, fout, buf, offset, count):
        #used for checksum
        lo = offset & 255
        hi = (offset >> 8) & 255
        chksum = count
        
        #length and offset
        fout.write(':%02X%02X%02X%02X' % (count, hi, lo, 0))
        
        chksum += hi + lo
        #read from the buffer and write to file
        for i in range(count):
            b = bytes(buf)[i]
            fout.write('%02X' % b)
            chksum += b
        fout.write('%02X\n' % ((256-chksum) & 255))
        
    def hexOutFile(self, finp, fout, base, count):
        off = 0
        while(off < count):
            chunk = count - off
            addr = base + off
            
            if (off & 0xFFFF) == 0:
                chksum = 2+4
                hi = (addr >> 24) & 255;
                lo = (addr >> 16) & 255;
                chksum += hi + lo
                fout.write(':02000004%02X%02X%02X\n' % (hi, lo, (256 - chksum) & 255))
                
            if chunk > self.bytes_per_line:
                chunk = self.bytes_per_line
                
            #read in binary data and output to a file
            buf = finp.read(chunk)
            if len(buf) != chunk:
                print('Premature end of file')
                sys.exit(-4)
            self.hexOutBytes(fout, buf, addr, chunk)
            
            off += chunk
                
        fout.write(':00000001FF\n')
        return 0
        
        
    def main(self):
        result = 0
        
        finp = open(self.input, 'rb')
        if len(sys.argv) > 2:
            fout = open(self.output, 'w')
            
        finp.seek(0, SEEK_END)
        size = finp.tell()
        finp.seek(0, SEEK_SET)
        
        result = self.hexOutFile(finp, fout, 0, size)
        if result < 0:
            sys.exit(-3)
        finp.close()
        fout.close()
        return result
    
if __name__ == "__main__":
    temp = Bin2hex()
    temp.parseCommands()