
class Parse(object):

    def __init__(self, fn):
        self.nextCmd = None
        self.curr = None
        self.type = None
        self.arg1 = None
        self.arg2 = None

        try:
            self.f = open(fn, 'r')
        except IOError:
            print('Could not open file')

    def cmdCheck(self):
        self.nextCmd = self.f.readline()
        if self.nextCmd == '':
            self.f.close()
            return False
        self.nextCmd = self.nextCmd.strip()
        return True

    def getNextCmd(self):
        self.curr = self.nextCmd

    def cmdType(self):
        if(self.curr.startswith('//') or not bool(self.curr.strip())):
            return 'Null'
        else:
            if('push' in self.curr):
                return 'C_PUSH'
            elif('pop' in self.curr):
                return 'C_POP'
            elif('label' in self.curr):
                return 'C_LABEL'
            elif('goto' in self.curr):
                return 'C_GOTO'
            elif('if-goto' in self.curr):
                return 'C_IF'
            elif ('function' in self.curr):
                return 'C_FUNCTION'
            elif ('return' in self.curr):
                return 'C_RETURN'
            elif('call' in self.curr):
                return 'C_CALL'
            else:
                return 'C_ARITHMETIC'
            
    def commentRemove(self,aStr):
        if('/' in aStr):
            return aStr[:aStr.index('/')]
        return aStr

    def lexInput(self):
        lex = self.commentRemove(self.curr).strip().split(' ')
        #print(lex)
        if(len(lex) == 1):
            self.type = lex[0]
        elif(len(lex) == 2):
            self.type = lex[0]
            self.arg1 = lex[1]
        else:
            self.type = lex[0]
            self.arg1 = lex[1]
            self.arg2 = int(lex[2].replace('\\W',''))




            
