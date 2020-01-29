"""CPU functionality."""

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.branchtable = {}
        # TODO: not sure how to reference and call the function
        self.branchtable[0b10000010] = self.reg_write
        self.branchtable[0b01000111] = self.print_reg

    def load(self):
        """Load a program into memory."""
        try:
            address = 0
            cmd_file = sys.argv[1]
            with open(cmd_file) as f:
                for line in f:
                    # remove any comments "#"
                    cmd_split = line.split("#")
                    command = cmd_split[0].strip()

                    if command == "":
                        # ignore blank lines
                        continue
                    
                    value = int(command, 2)
                    self.ram[address] = value
                    address += 1
                
        except FileNotFoundError:
            print(f"Error. File {cmd_file} not found")
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            return self.reg[reg_a]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # read value in self.pc
        running = True

        while running:
            IR = self.ram[self.pc]
            args = IR>>6

            if IR == 0b00000001: # HLT
                running = False
                break
            elif IR == 0b10100010: #ALU MUL
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
            else: # HELPER METHODS
                self.branchtable[IR]()

            # update program count 
            self.pc += args
            self.pc += 1

    def ram_write(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.ram[address] = value
        return f"Wrote {value} to RAM address: {address}"

    def ram_read(self, address):
        return self.ram[address]

    def reg_write(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[address] = value
        return f"Wrote {value} to REG address: {address}"
    
    def reg_read(self):
        address = self.ram[self.pc + 1]
        return self.reg[address]

    def print_reg(self):
        address = self.ram[self.pc + 1]
        print(self.reg[address])
