
class Writer(object):

    def __init__(self,fn):

        self.code = []
        self.counter = 0
        try:
            self.f = open(fn,'w')
        except IOError:
            print('Could not open output file')
            
    #@staticmethod
    def pushCmd(self,seg, idx):
        if(seg == 'static' or seg == 'constant' or seg == 'temp' or seg =='pointer'):
            if(seg == 'static'):
                self.code.append('@'+str(16 + idx))
                self.code.append('D=M')
            elif(seg == 'constant'):
                self.code.append('@'+str(idx))
                self.code.append('D=A')
            elif(seg == 'temp'):
                self.code.append('@R5')
                self.code.append('D=M')
                self.code.append('@' + str(5+idx))
                self.code.append('A=D+A')
                self.code.append('D=M')
            elif(seg == 'pointer'):
                if(idx == 0):
                    self.code.append('@THIS')
                else:
                    self.code.append('@THAT')
                self.code.append('D=M')
            else:
                print('Error')
        elif(seg == 'local' or seg == 'argument' or seg == 'this' or seg == 'that'):
            if(seg == 'local'):
                self.code.append('@LCL')
            elif(seg == 'argument'):
                self.code.append('@ARG')
            elif(seg == 'this'):
                self.code.append('@THIS')
            elif(seg == 'that'):
                self.code.append('@THAT')
            else:
                print('ERROR1')

            self.code.append('D=M')
            self.code.append('@' + str(idx))
            self.code.append('A=D+A')
            self.code.append('D=M')
        self.code.append('@SP')
        self.code.append('A=M')
        self.code.append('M=D')
        self.code.append('@SP')
        self.code.append('M=M+1')

    def popCmd(self,seg,idx):
        if(seg == 'static' or seg == 'constant' or seg == 'temp' or seg =='pointer'):
            if(seg == 'static'):
                self.code.append('@'+str(16 + idx))
                self.code.append('D=A')
            elif(seg == 'constant'):
                print('This is not possible')
            elif(seg == 'temp'):
                self.code.append('@R5')
                self.code.append('D=M')
                self.code.append('@' + str(5+idx))
                self.code.append('D=D+A')
            elif(seg == 'pointer'):
                if(idx == 0):
                    self.code.append('@THIS')
                else:
                    self.code.append('@THAT')
                self.code.append('D=M')
            else:
                print('Error2')
        elif(seg == 'local' or seg == 'argument' or seg == 'this' or seg == 'that'):
            if(seg == 'local'):
                self.code.append('@LCL')
            elif(seg == 'argument'):
                self.code.append('@ARG')
            elif(seg == 'this'):
                self.code.append('@THIS')
            elif(seg == 'that'):
                self.code.append('@THAT')
            else:
                print('ERROR3')

            self.code.append('D=M')
            self.code.append('@' + str(idx))
            self.code.append('D=D+A')
        self.code.append('@R13')
        self.code.append('M=D')
        self.code.append('@SP')
        self.code.append('AM=M-1')
        self.code.append('D=M')
        self.code.append('@R13')
        self.code.append('A=M')
        self.code.append('M=D')

    def aSAOCmd(self,aType):
        self.code.append('@SP')
        self.code.append('AM=M-1')
        self.code.append('D=M')
        self.code.append('A=A-1')
        if(aType == 'Add'):
            self.code.append('M=M+D')
        elif(aType =='Sub'):
            self.code.append('M=M-D')
        elif(aType =='And'):
            self.code.append('M=M&D')
        elif(aType == 'Or'):
            self.code.append('M=M|D')
        else:
            print('Error4')

    def nnCmd(self,aType):
        self.code.append('@SP')
        self.code.append('A=M-1')
        if(aType == 'Not'):
            self.code.append('M=!M')
        elif(aType == 'Neg'):
            self.code.append('M=-M')
        else:
            print('Error5')

    def falseStart(self,idx):
        return '@'+'FALSE'+str(idx)
    def falseEnd(self,idx):
        return '(' + 'FALSE' + str(idx) + ')'
    def continueStart(self,idx):
        return '@' + 'CONTINUE' + str(idx)
    def continueEnd(self,idx):
        return '(' + 'CONTINUE' + str(idx) + ')'

    def cmdCmp(self,aType):
        self.code.append('@SP')
        self.code.append('AM=M-1')
        self.code.append('D=M')
        self.code.append('A=A-1')
        self.code.append('D=M-D')
        self.code.append(self.falseStart(self.counter))
        if(aType == 'Eq'):
            self.code.append('D;JNE')
        elif(aType == 'Gt'):
            self.code.append('D;JLE')
        elif(aType == 'Lt'):
            self.code.append('D;JGE')
        else:
            print('Error6')
            
        self.code.append('@SP')
        self.code.append('A=M-1')
        self.code.append('M=-1')
        self.code.append(self.continueStart(self.counter))
        self.code.append('0;JMP')
        self.code.append(self.falseEnd(self.counter))
        self.code.append('@SP')
        self.code.append('A=M-1')
        self.code.append('M=0')
        self.code.append(self.continueEnd(self.counter))
        self.counter += 1

    def write(self):
        try:
            for line in self.code:
                self.f.write(line +'\n')
        except IOError:
            print('couldnt write lines to file')
        self.code.clear()

    def writeArith(self,cmd):
        if(cmd == 'add'):
            self.aSAOCmd('Add')
        elif(cmd == 'sub'):
            self.aSAOCmd('Sub')
        elif(cmd == 'neg'):
            self.nnCmd('Neg')
        elif(cmd == 'eq'):
            self.cmdCmp('Eq')
        elif(cmd == 'gt'):
            self.cmdCmp('Gt')
        elif(cmd == 'lt'):
            self.cmdCmp('Lt')
        elif(cmd == 'and'):
            self.aSAOCmd('And')
        elif(cmd == 'or'):
            self.aSAOCmd('Or')
        elif(cmd == 'not'):
            self.nnCmd('Not')
        else:
            print(cmd)
            print('Error7')
        self.write()

    def writePP(self,cmd,seg,idx):

        if( cmd == 'push'):
            self.pushCmd(seg,idx)
        elif(cmd == 'pop'):
            self.popCmd(seg,idx)
        else:
            print('Error')
            return
        self.write()

    def close(self):
        self.counter = 0
        try:
            self.f.close()
        except IOError:
            print('Couldnt close file')
        


        
                                
    
