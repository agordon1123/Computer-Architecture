"""CPU functionality."""

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

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
            # TODO: printing dec val of bin num
            if IR == LDI:
                # Load immediate
                reg = self.ram[self.pc + 1]
                val = self.ram[self.pc + 2]
                self.reg[reg] = val
                self.pc += 3
            elif IR == PRN:
                # PRINT
                reg = self.ram[self.pc + 1]
                print(f"{self.reg[reg]}")
                self.pc += 2
            elif IR == HLT:
                # HALT
                running = False
                break


    def ram_write(self, address, value):
        self.ram[address] = value
        return f"Wrote {value} to RAM address: {address}"

    def ram_read(self, address):
        # TODO: does not have any check here. do we need one?
        return self.ram[address]
