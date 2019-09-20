"""CPU functionality."""

import sys


LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # DO NOT ADD COMMAS
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.ram[0] = 0x00

        # Markers
        self.PC = 0

        #  Flags
        self.E = None
        self.L = None
        self.G = None

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

            with open(filename) as f:
                for line in f:

                    # parse each line
                    # split before and after comment symbol
                    comment_split = line.split("#")

                    # remove extra white space
                    instruction = comment_split[0].strip()

                    # ignore blanks
                    if instruction == "":
                        continue

                    # convert instruction to binary int
                    # instruction = f"0b{instruction}"
                    value = int(instruction, 2)

                    # set binary value as memory at current address
                    self.ram[address] = value

                    # increment address for next value
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            """If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

            If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0."""

            self.E = 0
            self.L = 0
            self.G = 0

            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1

            if self.reg[reg_a] < self.reg[reg_b]:
                self.L = 1

            if self.reg[reg_a] > self.reg[reg_b]:
                self.G = 1

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        """ram_read() should accept the address to read and return the value stored there."""
        self.MAR = address
        value = self.ram[self.MAR]

        return value

    def ram_write(self, value, address):
        """ raw_write() should accept a value to write, and the address to write it to."""
        self.MDR = value
        self.MAR = address

        self.ram[self.MAR] = self.MDR

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            pc = self.PC
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            # read the memory address stored in register PC, and store in IR
            self.IR = self.ram[pc]

            # starting at beginning
            # command = self.ram[pc]
            # command is self.IR

            if self.IR == LDI:
                self.reg[operand_a] = operand_b
                # print("Reg:", operand_a, "Value: ", self.reg[operand_a])
                self.PC += 3

            elif self.IR == PRN:
                print(self.reg[operand_a])
                self.PC += 2

            elif self.IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.PC += 3

            elif self.IR == HLT:
                running = False
                self.PC += 1

            elif self.IR == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.PC += 3

            elif self.IR == JMP:
                self.PC = self.reg[operand_a]

            elif self.IR == JEQ:

                if self.E == 1:
                    self.PC = self.reg[operand_a]

                elif self.E != 1:
                    self.PC += 2

            elif self.IR == JNE:

                if self.E != 1:
                    self.PC = self.reg[operand_a]

                elif self.E == 1:
                    self.PC += 2

            else:
                print(f"Unknown instruction: {self.IR}")
                sys.exit(1)
