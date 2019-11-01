import sys
from helpers import SymbolTable, destTable, compTable, jumpTable, Parser, to16binary, A_COMMAND, C_COMMAND, L_COMMAND

def main():

    if len(sys.argv) < 3:
        print("Error 1: Please input both .asm and .hack filenames at the command line")
        return 1
    elif len(sys.argv) > 3:
        print("Warning: too many arguments, discarding the rest after the 3rd")
    if sys.argv[1][-4:] != ".asm" or sys.argv[2][-5:] != ".hack":
        print("Error 2: Invalid file extension(s), must use .asm and .hack filenames")
        return 2
    print ("success")

    f1 = open(sys.argv[1], "r")
    f2 = open(sys.argv[2], "w")

    theobject = Parser(f1)
    romAddress = 0

    #executing the first pass, in order to save all the labels in the SymbolTable first
    #notice that the romAddress counter does not increase, unless an A or C instruction is encountered
    while theobject.hasMoreCommands():
        if theobject.commandType == L_COMMAND:
            SymbolTable[theobject.symbol] = romAddress
            theobject.advance(f1)
        elif theobject.commandType == A_COMMAND or theobject.commandType == C_COMMAND:
            romAddress += 1
            theobject.advance(f1)
        elif theobject.commandType == 0:
            theobject.advance(f1)
        else:
            sys.exit("Exception: invalid command type encountered, exiting program...")

    f1.seek(0) #resetting the file pointer to the beginning
    theobject.__init__(f1) #reinitializing the object with the reset file pointer
    ramAddress = 16
    romAddress = 0

    #executing the 2nd pass, where all the instructions are translated into binary code
    while True:
        if theobject.commandType == A_COMMAND:
            if theobject.symbol.isdigit() == True:  #addresses are converted directly into binary
                f2.write(f"{to16binary(theobject.symbol)}\n")
            else:
                if theobject.symbol in SymbolTable: #symbols are first looked up in the SymbolTable
                    f2.write(f"{to16binary(SymbolTable[theobject.symbol])}\n")
                else:
                    SymbolTable[theobject.symbol] = ramAddress
                    ramAddress += 1
                    f2.write(f"{to16binary(SymbolTable[theobject.symbol])}\n")
            romAddress += 1

        elif theobject.commandType == C_COMMAND:
            f2.write('111' + compTable[theobject.comp] + destTable[theobject.dest] + jumpTable[theobject.jump] +'\n')
            romAddress += 1

        elif theobject.commandType == L_COMMAND:
            SymbolTable[theobject.symbol] = romAddress

        elif theobject.commandType == 0:
            if theobject.hasMoreCommands() == False:
                break
            theobject.advance(f1)
            continue

        else:
            sys.exit("Exception: invalid command type encountered, exiting program...")

        if theobject.hasMoreCommands() == False:
            break
        theobject.advance(f1)

if __name__ == "__main__":
    main()