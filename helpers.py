SymbolTable = {
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8,
    'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
    'SCREEN': 16384, 'KBD': 24576,
    'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4
}

destTable = {'': '000',
    'null': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'
}

compTable = {
    '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100', 'A': '0110000', 'M': '1110000',
    '!D': '0001101', '!A': '0110001', '!M': '1110001', '-D': '0001111', '-A': '0110011', '-M': '1110011',
    'D+1': '0011111', 'A+1': '0110111', 'M+1': '1110111', 'D-1': '0001110', 'A-1': '0110010', 'M-1': '1110010',
    'D+A': '0000010', 'D+M': '1000010', 'D-A': '0010011', 'D-M': '1010011', 'A-D': '0000111', 'M-D': '1000111',
    'D&A': '0000000', 'D&M': '1000000', 'D|A': '0010101', 'D|M': '1010101'
}

jumpTable = {'': '000',
    'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'
}

A_COMMAND = 1
C_COMMAND = 2
L_COMMAND = 3

class Parser:

    def __init__(self, file):
        self.line = file.readline()
        self.next = file.readline()
        self.updateCommandType()
        self.getSymbol()
        self.getDestCompJump()

    def hasMoreCommands(self):
        if self.next == '':
            return 0
        else:
            return 1

    def advance(self, file):
        if self.hasMoreCommands() == 1:
            self.line = self.next
            self.next = file.readline()
            self.updateCommandType()
            self.getSymbol()
            self.getDestCompJump()
        else:
            print("End of The line")

    def updateCommandType(self):
        for char in self.line:
            if char == '@':
                self.commandType = A_COMMAND
                break
            elif char == 'n' or char == 'M' or char == 'A' or char == 'D' or char == '0':
                #'n' stands for the beninning of the "null" keyword, if used
                self.commandType = C_COMMAND
                break
            elif char == '(':
                self.commandType = L_COMMAND
                break
            elif char == '/':   #if line starts with a comment, we ignore it alltogeher
                self.commandType = 0
                break

    def getSymbol(self):
        #we strip the endlines and whitespace at the beginning and end of the line
        stripped = self.line.strip('\n')
        stripped = stripped.strip('\t')
        stripped = stripped.strip()

        #if we encoounter a comment in the line, we only keep the part before the comment
        if '/' in stripped:
                stripped = stripped.split('/', 1)[0]

        if self.commandType == A_COMMAND:
            #in case more whitespaces are in the command,
            #we discard the rest of the string after the symbol/address: "stripped.split(' ', 1)[0]"
            #we use the [1:] index to discard the '@' before the symbol/address
            self.symbol = stripped.split(' ', 1)[0][1:]
        elif self.commandType == L_COMMAND:
            #we use the [1:-1] index to discard both the leading and end parenthesis
            self.symbol = stripped.split(' ', 1)[0][1:-1]
        else:
            self.symbol = ''
        return self.symbol

    def getDestCompJump(self):
        self.dest = 'null'
        self.comp = 'null'
        self.jump = 'null'
        if self.commandType == C_COMMAND:
            stripped = self.line.strip('\n')
            stripped = stripped.strip('\t')
            stripped = stripped.replace(" ", "")
            if '/' in stripped:
                stripped = stripped.split('/', 1)[0]
            if '=' in stripped:
                #if no '=' encountered in the instruction, it means that the dest is null, and it remains as such
                self.dest = stripped.split('=', 1)[0]
                stripped = stripped.split('=', 1)[1]
            if ';' in stripped:
                #if no ';' encountered in the instruction, it means that the jump is null, and it remains as such
                self.comp = stripped.split(';', 1)[0]
                self.jump = stripped.split(';', 1)[1]
            else:
                self.comp = stripped

def to16binary(string):
    smallBin = bin(int(string))[2:] #discard the '0b' prefix added by the bin() function
    fullBin = ''
    #adding the rest of the 0s, up to a 16-bit binary number
    for i in range (16 - len(smallBin)):
        fullBin = fullBin + '0'
    return fullBin + smallBin