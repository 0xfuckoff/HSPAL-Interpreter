import math
import sys
import random

def s2i(n):
    return int(n, 16) 

def s2h(n):
    return hex(int(n, 16))

class Stacks:
 
    def __init__(self, n):
        self.size = n
        self.arr = [None] * n
        self.top = math.floor(n/2) + 1
 
    def push(self, x):
        if self.top > 0:
            self.top = self.top - 1
            self.arr[self.top] = x
        else:
            print("Stack Overflow by element : ", x)
 
    def isEmpty(self):
        if self.top - 1 >= self.size / 2:
            return True

    def peek(self):
        return self.arr[self.top] if self.top is not None else None

    def pop(self):
        if self.top <= self.size / 2:
            x = self.arr[self.top]
            self.top = self.top + 1
            return x
        else:
            print("Stack Underflow")
            exit(1)
 
class Interpreter:
    def __init__(self):
        self.script = ''
        self.reg = 0
        self.ip = 0
        self.labels = {}
        self.commands = []
        self.stack = []

    def error(self, code):
        raise Exception(f"Exception thrown with status code: {code}")

    def hspal_file(self):
        with open(self.script, "r") as f:
            return f.read().encode()
    
    def get_commands(self):
        x = self.hspal_file().split(b"\n")
        return [c.decode('utf-8') for c in x]

    def init_stacks(self):
        for s in range(256):
            self.stack.insert(s, Stacks(256))
        return self.stack

    def run(self, file):
        self.script = file
        stack = self.init_stacks()
        cmds = self.get_commands()
        while self.ip < len(cmds):
            op = cmds[self.ip]
            match(op[:2]) :
                case '00': # Mark a new label
                    print(f"Mark Label: {s2h(op[2:])}")
                    self.labels[op[2:]] = self.ip
                case '01': # GOTO a marked label
                    print(f"GOTO Label: {op[2:]}")
                    if op[2:] not in self.labels:
                        raise Exception(f"Label {op[2:]} does not exist!")
                    elif op[2:] not in self.labels:
                        raise Exception(f"Label {op[2:]} does not exist!")
                    self.ip = self.labels[op[2:]]
                case '02': # POP value from stack & goto label
                    if  stack[s2i(op[2:4])].isEmpty():
                        raise Exception('Empty Stack Resulted In Stack Underflow!!')
                    value = stack[s2i(op[2:4])].pop()
                    print(f"POP(STACK[{stack[op[2:4]]}]) -> Result: {value}")
                case '03': # POP value from stack & skip next instruction if nonzero
                    print(f"stack[{s2i(op[2:4])}]")
                    if  stack[s2i(op[2:4])].isEmpty():
                        raise Exception('Empty Stack Resulted In Stack Underflow!!')
                    value = stack[s2i(op[2:4])].pop()
                    print(f"(POP(STACK[{op[2:4]}]) > 0) ?  Skip Next Command : Continue | Popped Value = {value}")
                    if value > hex(0):
                        self.ip += 1
                        print("Skipped Next Instruction")
                    else:
                        print("Continued Execution")
                case '04': # Halt Execution & Return Status Code
                    code = s2h(op[2:])
                    if code == hex(0):
                        print(f"Program Halted With Status Code: {code}")
                        exit(1)
                    elif code == hex(-1):
                        print(f"Program Halted With Status Code: {code}")
                        exit(1)
                    else:
                        print(f"Program Halted With Status Code: {code}")
                        exit(1)
                case '10': # Take single char from stdin and push to specified stack
                    value = hex(ord(sys.stdin.read(1)))
                    stack[s2i(op[2:4])].push(value)
                    print(f"PUSH({value}) ONTO STACK[{op[2:4]}]")
                case '11': # Take in a number from stdin and push to specified stack
                    value = s2i(sys.stdin.read(1))
                    if not isinstance(value, int):
                        raise Exception("Type error, expected integer")
                    stack[s2i(op[2:4])].push(hex(value))
                    print(f"PUSH({hex(value)}) INTO STACK[{op[2:4]}]")
                case '12': # Pop value from specified stack and print to stdout
                    if stack[s2i(op[2:4])].isEmpty():
                        raise Exception("Stack underflow detected!")
                    print(f"POP(STACK[{op[2:4]}]) AND PRINT VALUE TO STDOUT")
                    print(f"POPPED VALUE: {chr(s2i(stack[s2i(op[2:4])].pop()))}")
                case '13': # Pop value from specified stack print corresponding unicode char to stdout
                    if stack[s2i(op[2:4])].isEmpty():
                        raise Exception("Stack underflow detected!")
                    print(f"POP(STACK[{op[2:4]}]) AND PRINT CHARACTER TO STDOUT")
                    print(f"POPPED VALUE: {chr(s2i(stack[s2i(op[2:4])].pop()))}")
                case '14': # Pop values from specified stack until stack is empty and print to stdout
                    if not stack[s2i(op[2:4])].isEmpty():
                        print(f"WHILE STACK[{op[2:4]}] IS NOT EMPTY: POP(STACK[{op[2:4]}]) AND PRINT CHARS TO STDOUT")
                        while not stack[s2i(op[2:4])].isEmpty():
                            print(f"{chr(s2i(stack[s2i(op[2:4])].pop()))}", end="")
                case '20': # Write 4 digits to register
                    self.reg = s2i(op[2:])
                    print(f"REG = {self.reg}")
                case '21': # Pop 2 values from specified stack, add them and push to the same stack
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    stack[s2i(op[2:4])].push(hex(value + value2))
                    print(f"STACK[{op[2:4]}] = POP(STACK[{op[2:4]}]) + POP(STACK[{op[2:4]}])")
                case '22': # Pop 2 values from specified stack, subtract them and push to the same stack
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    print(f"{value} {value2}")
                    stack[s2i(op[2:4])].push(hex(value - value2))
                    print(f"STACK[{op[2:4]}] = POP(STACK[{op[2:4]}]) - POP(STACK[{op[2:4]}])")
                case '23': # Pop 2 values from specified stack, multiply them and push to the same stack
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    stack[s2i(op[2:4])].push(hex(value * value2))
                    print(f"STACK[{op[2:4]}] = POP(STACK[{op[2:4]}]) * POP(STACK[{op[2:4]}])")
                case '24': # Pop 2 values from specified stack, divide them and push to the same stack
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    stack[s2i(op[2:4])].push(hex(value // value2))
                    print(f"STACK[{op[2:4]}] = POP(STACK[{op[2:4]}]) // POP(STACK[{op[2:4]}])")
                case '25': # Pop 2 values from specified stack, raise to the power and push to the same stack
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    stack[s2i(op[2:4])].push(hex(value ** value2))
                    print(f"STACK[{op[2:4]}] = POP(STACK[{op[2:4]}]) ** POP(STACK[{op[2:4]}])")
                case '26': # Write random integer in specified range to register
                    self.reg = hex(int(random(0, s2h(op[2:]))))
                    print(f"REG = {self.reg}")
                case '30': # Pop 2 values from 1st specified stack, if they are equal push 1 to 2nd specified stack else push 0
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    print(f"if POP(STACK[{op[2:4]}]) == POP(STACK[{op[2:4]}]): STACK[{op[4:]}] = 1 ELSE: STACK[{op[4:]}] = 0")
                    if value == value2:
                        stack[s2i(op[4:])].push(hex(1))
                    else:
                        stack[s2i(op[4:])].push(hex(0))
                case '31': # Pop 2 values from 1st specified stack, if first is larger than second then push 1 to 2nd specified stack else push 0
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    print(f"if POP(STACK[{op[2:4]}]) > POP(STACK[{op[2:4]}]): STACK[{op[4:]}] = 1 ELSE: STACK[{op[4:]}] = 0")
                    if value > value2:
                        stack[s2i(op[4:])].push(hex(1))
                    else:
                        stack[s2i(op[4:])].push(hex(0))
                case '32': # Pop 2 values from 1st specified stack, if first is smaller than second then push 1 to 2nd specified stack else push 0
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    print(f"if POP(STACK[{op[2:4]}]) < POP(STACK[{op[2:4]}]): STACK[{op[4:]}] = 1 ELSE: STACK[{op[4:]}] = 0")
                    if value < value2:
                        stack[s2i(op[4:])].push(hex(1))
                    else:
                        stack[s2i(op[4:])].push(hex(0))
                case '33': # Pop 2 values from 1st specified stack, if both or 1 is nonzero then push 1 to 2nd specified stack else push 0
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    print(f"if POP(STACK[{op[2:4]}]) || POP(STACK[{op[2:4]}] > 0): STACK[{op[4:]}] = 1 ELSE: STACK[{op[4:]}] = 0")
                    if (value or value2) > 0:
                        stack[s2i(op[2:4])].push(hex(1))
                    else:
                        stack[s2i(op[2:4])].push(hex(0))
                case '34': # Pop 2 values from 1st specified stack, if both is nonzero then push 1 to 2nd specified stack else push 0
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    print(f"if POP(STACK[{op[2:4]}]) && POP(STACK[{op[2:4]}] > 0): STACK[{op[4:]}] = 1 ELSE: STACK[{op[4:]}] = 0")
                    if (value and value2) > 0:
                        stack[s2i(op[4:])].push(hex(1))
                    else:
                        stack[s2i(op[4:])].push(hex(0))
                case '35': # Pop 2 values from 1st specified stack, if exactly 1 is nonzero then push 1 to 2nd specified stack else push 0
                    value = s2i(stack[s2i(op[2:4])].pop())
                    value2 = s2i(stack[s2i(op[2:4])].pop())
                    print(f"if POP(STACK[{op[2:4]}]) ^ POP(STACK[{op[2:4]}] > 0): STACK[{op[4:]}] = 1 ELSE: STACK[{op[4:]}] = 0")
                    if (value ^ value2) > 0:
                        stack[s2i(op[4:])].push(hex(1))
                    else:
                        stack[s2i(op[4:])].push(hex(0))
                case '36': # Push 1 to stack if register equals zero else push 0
                    if self.reg == 0:
                        stack[s2i(op[2:4])].push(hex(1))
                    else:
                        stack[s2i(op[2:4])].push(hex(0))
                    print(f"IF REGISTER == 0: PUSH 1 ONTO STACK[{op[2:4]}] ELSE PUSH 0")
                case '40': # Push register value onto specified stack
                    stack[s2i(op[2:4])].push(hex(self.reg))
                    print(f"{stack[s2i(op[2:4])].peek()}")
                    self.reg = 0
                    print(f"PUSH REGISTER VALUE TO STACK[{op[2:4]}]")
                case '41': # Pop specified stack and store in register
                    if stack[s2i(op[2:4])].isEmpty():
                        raise Exception("Stack Underflow detected!")
                    self.reg = s2i(stack[s2i(op[2:4])].pop())
                    print(f"POP(STACK[{op[2:4]}]) AND STORE IN REGISTER")
                case '42': # Copy lasted pushed value from specified stack to register
                    if stack[s2i(op[2:4])].isEmpty():
                        raise Exception("Stack Underflow detected!")
                    self.reg = s2i(stack[s2i(op[2:4])].peek())
                    print(f"PEEK(STACK[{op[2:4]}]) AND STORE IN REGISTER")
                case '43': # Count how many values on specified stack and store count in register
                    print(f"COUNT(STACK[{op[2:4]}]) AND STORE RESULT IN REGISTER")
                    self.reg = len(stack[s2i(op[2:4])])
                case _:
                    print("Invalid opcode")
            if self.ip != len(cmds):
                self.ip += 1

if __name__ == '__main__':
    init = Interpreter()
    # Takes random file that has valid HSPAL commands
    init.run('crackme.hspal')
