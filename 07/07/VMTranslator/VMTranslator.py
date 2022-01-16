import sys
import Write
import Parse
import os

def getExt(fn):
    idx = fn.rindex('.')
    return fn[idx:]

def getFns(dirName):
    vmFiles = []
    dirFiles = os.listdir(dirName)
    for fn in dirFiles:
        if fn.endswith('.vm'):
            vmFiles.append(fn)
    return dirFiles

if __name__ == '__main__':

    if (len(sys.argv) == 1):
        raise IOError

    fileIn = sys.argv[1]
    files = []
    fileOut = None

    if(getExt(fileIn) != '.vm'):
        raise IOError
    files.append(fileIn)
    fileOut = fileIn.rstrip('.vm') + '.asm'
    
    
    writer = Write.Writer(fileOut)
    parser = Parse.Parse(fileIn)
    while(parser.cmdCheck()):
        parser.getNextCmd()
        aType = parser.cmdType()
        if(aType != 'Null'):
            if(aType == 'C_PUSH' or aType == 'C_POP'):
                parser.lexInput()
                writer.writePP(parser.type,parser.arg1,parser.arg2)
            else:
                parser.lexInput()
                writer.writeArith(parser.type)
    writer.close()
