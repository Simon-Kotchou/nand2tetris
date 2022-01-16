#Author: Simon Kotchou

import sys

class Parser(object):

    def __init__(self):
        self.pc = 16
        self.symbDict = {
            'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,'SCREEN':16384,'KBD':24576,'R0':0,'R1':1,'R2':2,'R3':3,
            'R4':4,'R5':5,'R6':6,'R7':7,'R8':8,'R9':9,'R10':10,'R11':11,'R12':12,'R13':13,'R14':14,'R15':15}

    def getDstCode(self,dst):
        if dst == 'M':
            return '001'
        elif dst == 'D':
            return '010'
        elif dst == 'MD':
            return '011'
        elif dst == 'A':
            return '100'
        elif dst == 'AD':
            return '110'
        elif dst == 'AM':
            return '101'
        elif dst == 'AMD':
            return '111'
        else:
            return'000'


    def getJmpCode(self,jmp):
        if jmp == 'JMP':
            return '111'
        elif jmp == 'JGT':
            return '001'
        elif jmp == 'JEQ':
            return '010'
        elif jmp == 'JGE':
            return '011'
        elif jmp == 'JTL':
            return '100'
        elif jmp == 'JNE':
            return '101'
        elif jmp == 'JLE':
            return '110'
        else:
            return '000'

    def getCmpCode(self,cmp):
        if cmp == '0':
            return '0101010'
        elif cmp == '1':
            return '0111111'
        elif cmp == '-1':
            return '0111010'
        elif cmp == 'D':
            return '0001100'
        elif cmp == 'A':
            return '0110000'
        elif cmp == 'M':
            return '1110000'
        elif cmp == '!D':
            return '0001101'
        elif cmp == '!A':
            return '0110001'
        elif cmp == '!M':
            return '1110001'
        elif cmp == '-D':
            return '0001111'
        elif cmp == '-A':
            return '0110011'
        elif cmp == '-M':
            return '1110011'
        elif cmp == 'D+1'or cmp == '1+D':
            return '0011111'
        elif cmp == 'A+1'or cmp == '1+A':
            return '0110111'
        elif cmp == 'M+1'or cmp == '1+M':
            return '1110111'
        elif cmp == 'D-1':
            return '0001110'
        elif cmp == 'A-1':
            return '0110010'
        elif cmp == 'M-1':
            return '1110010'
        elif cmp == 'A+D'or cmp == 'D+A':
            return '0000010'
        elif cmp == 'D+M'or cmp == 'M+D':
            return '1000010'
        elif cmp == 'D-A':
            return '0010011'
        elif cmp == 'D-M':
            return '1010011'
        elif cmp == 'A-D':
            return '0000111'
        elif cmp == 'M-D':
            return '1000111'
        elif cmp == 'D&A'or cmp == 'A&D':
            return '0000000'
        elif cmp == 'D&M'or cmp == 'M&D':
            return '1000000'
        elif cmp == 'D|A'or cmp == 'A|D':
            return '0010101'
        elif cmp == 'D|M'or cmp == 'M|D':
            return '1010101'
        else:
            return ''

    def parseFile(self,fn):
        parsedLines = []
        with open(fn,'r') as txt:
            for line in txt.readlines():
                line=line.split('/')[0]
                line=line.replace(' ','')
                line = line.strip('\r\n')
                if line:
                    parsedLines.append(line)
        return parsedLines

            
    def parseSymb(self,symb):
        if symb not in self.symbDict:
            self.symbDict[symb] = self.pc
            self.pc += 1
        return self.symbDict[symb]

    def parseAInst(self,inst):
        inst = inst[1:]
        try:
            inst = int(inst)
            inst = bin(inst)[2:]
            inst = (16 - len(inst)) * '0' + inst
        except ValueError:
            inst = self.parseSymb(inst)
            inst = bin(inst)[2:]
            inst = (16 - len(inst)) * '0' + inst
        return inst
        

    def parseCInst(self, inst):
        comp = None
        dest= None
        jump = None

        if inst.find('=') != -1:
            #print(inst.split('='))
            [dest,inst] = inst.split('=')

        if inst.find(';') != -1:
            [comp,jump] = inst.split(';')

        else:
            comp = inst

        start_out = '111'
        start_out += self.getCmpCode(comp)
        start_out += self.getDstCode(dest)
        start_out += self.getJmpCode(jump)
        return start_out

if __name__ == '__main__':
    global temp
    temp=0

    if len(sys.argv) == 1:
        raise ValueError
    else:
        fn = sys.argv[1]

    parser = Parser()

    inst = parser.parseFile(fn)

    outfn = fn.rstrip('.asm')+'.hack'

    for n,i in enumerate(inst):
        if i[0] == '(' and i[-1] == ')':
            t = i.strip('(').strip(')')
            parser.symbDict[t] = n - temp
            temp += 1

    with open(outfn,'w') as out:

        for i in inst:
            if i[0] == '@':
                binInst = parser.parseAInst(i)
            elif i[0] == '(':
                continue
            else:
                binInst = parser.parseCInst(i)

            out.write(binInst +'\n')

        
        
    

        



        





        
