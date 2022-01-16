import sys
import Write
import Parse
import os
from pathlib import Path

def getExt(fn):
    idx = fn.rindex('.')
    return fn[idx:]

def getFns(dirName):
    vmFiles = []
    dirFiles = os.listdir(dirName)
    for fn in dirFiles:
        if fn.endswith('.vm'):
            vmFiles.append(dirName + fn)
    return vmFiles

if __name__ == '__main__':

    if (len(sys.argv) == 1):
        raise IOError

    fileIn = sys.argv[1]
    filePath = Path(fileIn)
    files = []
    outFile = None

    if filePath.is_dir():
        files = getFns(fileIn)
        outFile = str(filePath) + '/' + filePath.name + '.asm'
    else:
        if(getExt(fileIn) != '.vm'):
            raise IOError
        files.append(fileIn)
        #print(fileIn)
        outFile = fileIn.rstrip('.vm') + '.asm'

    writer = Write.Writer(outFile)
    for file in files:
        name =Path(file).name
        if(name == 'Sys.vm'):
            writer.writeIn()

    for file in files: 
        parser = Parse.Parse(file)
        name = Path(file).name
        writer.setFn(name)
        while(parser.cmdCheck()):
            parser.getNextCmd()
            aType = parser.cmdType()
            if(aType != 'Null'):
                parser.lexInput()
                if(aType == 'C_PUSH' or aType == 'C_POP'):
                    
                    writer.writePP(parser.type,parser.arg1,parser.arg2)
                elif(aType == 'C_LABEL'):
                    
                    writer.writeLab(parser.arg1)
                elif(aType == 'C_GOTO'):
                    
                    writer.writeGo(parser.arg1)
                elif(aType == 'C_IF'):
                    
                    writer.writeIf(parser.arg1)
                elif(aType == 'C_FUNCTION'):
                    
                    writer.writeFunct(parser.arg1,parser.arg2)
                elif(aType == 'C_RETURN'):
                    
                    writer.writeRet()
                elif(aType == 'C_CALL'):
                    
                    writer.writeCall(parser.arg1,parser.arg2)
                elif(aType == 'C_ARITHMETIC'):
                    
                    writer.writeArith(parser.type)
    writer.close()
