#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import image_png
import re

class BrainFuck:
    """Interpretr jazyka brainfuck."""

    def getInput(self, data):
        tmp = data.split("!")
        if len(tmp) == 1:
            return tmp[0], ''
        return tmp[0], tmp[1]

    def __init__(self, data, memory=b'\x00', memory_pointer=0, skipOptimalization=False):
        """Inicializace interpretru brainfucku."""
        stack = list()
        dataPointer = 0
        self.data, inputData = self.getInput(data)
        if skipOptimalization == False:
            print(len(self.data))
            self.data = re.sub('[^\[\]\.,+-><]', '', self.data)
            self.data = re.sub('[:/0-9]', '', self.data)
            print(len(self.data))
            print(self.data)
        inputPointer = 0
        dataLength = len(self.data)

        # inicializace proměnných
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer
        memoryLength = len(self.memory)

        # DEBUG a testy
        # a) paměť výstupu
        self.output = ''

        while 1:
            x = self.data[dataPointer]
            if   x == '+':
                tmp = self.memory[self.memory_pointer]
                tmp = (tmp + 1) % 256
                self.memory[self.memory_pointer] = tmp

            elif x == '-':
                tmp = self.memory[self.memory_pointer]
                tmp = (tmp - 1) % 256
                self.memory[self.memory_pointer] = tmp

            elif x == '>':
                self.memory_pointer += 1
                if self.memory_pointer == memoryLength:
                    self.memory.append(0)
                    memoryLength += 1

            elif x == '<':
                self.memory_pointer -= 0 if self.memory_pointer == 0 else 1

            elif x == '[':
                if self.memory[self.memory_pointer] > 0:
                    stack.append(dataPointer)
                else:
                    vnoreni = 1
                    dataPointer += 1
                    while vnoreni > 0:
                        if self.data[dataPointer] == ']':
                            vnoreni -= 1
                        if self.data[dataPointer] == '[':
                            vnoreni += 1
                        dataPointer += 1
                        if dataPointer == dataLength:
                            break
                    dataPointer -= 1
            elif x == ']':
                if self.memory[self.memory_pointer] == 0:
                    stack.pop()
                else:
                    dataPointer = stack[len(stack)-1]

            elif x == '.':
                tmp = chr(self.memory[self.memory_pointer])
                self.output = self.output + tmp
                sys.stdout.write(tmp)
                sys.stdout.flush()

            elif x == ',':
                if inputPointer == len(inputData):
                    tmp = ord(sys.stdin.read(1))
                else:
                    tmp = ord(inputData[inputPointer])
                    inputPointer += 1
                self.memory[self.memory_pointer] = tmp % 256

            dataPointer += 1;
            if dataPointer >= dataLength:
                break

    #
    # pro potřeby testů
    #
    def get_memory(self):
        return self.memory


class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""

    def move(self, x, y, direction):
        if   direction == 0:
            x += 1
            if x ==  self.width:
                return None, None
            return x, y
        elif direction == 1:
            y += 1
            if y == self.height:
                return None, None
            return x, y
        elif direction == 2:
            x -= 1
            if x == -1:
                return None, None
            return x, y
        else:
            y -= 1
            if y == -1:
                return None, None
            return x, y

    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""

        if not os.path.exists(filename):
            print("Soubor neexistuje")
            return

        self.commands = []
        image = image_png.PngReader(filename)
        self.width = image.width
        self.height = image.height
        x = 0
        y = 0
        direction = 0
        while 1:
            cell = image.rgb[y][x]
            if   cell[0] == 255:
                if   cell[1] == 255:
                    self.commands.append('[')
                elif cell[1] ==   0:
                    self.commands.append('>')
            elif cell[0] == 128:
                if   cell[1] == 128:
                    self.commands.append(']')
                elif cell[1] ==   0:
                    self.commands.append('<')
            elif cell[0] ==   0:
                if   cell[1] == 255:
                    if   cell[2] == 255:
                        direction = (direction + 1) % 4
                    elif cell[2] ==   0:
                        self.commands.append('+')
                elif cell[1] == 128:
                    if   cell[2] == 128:
                        direction = 3 if direction == 0 else direction - 1
                    elif cell[2] ==   0:
                        self.commands.append('-')
                elif cell[1] ==   0:
                    if   cell[2] == 255:
                        self.commands.append('.')
                    elif cell[2] == 128:
                        self.commands.append(',')

            x, y = self.move(x, y, direction)
            if x == None:
                break
        self.data = ''.join(self.commands)
        self.program = BrainFuck(self.data, skipOptimalization = True)

class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""

    def move(self, x, y, direction):
        if   direction == 0:
            x += 1
            if x ==  self.width:
                return None, None
            return x, y
        elif direction == 1:
            y += 1
            if y == self.height:
                return None, None
            return x, y
        elif direction == 2:
            x -= 1
            if x == -1:
                return None, None
            return x, y
        else:
            y -= 1
            if y == -1:
                return None, None
            return x, y

    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""

        if not os.path.exists(filename):
            print("Soubor neexistuje")
            return

        self.commands = []
        image = image_png.PngReader(filename)
        self.width = image.width
        self.height = image.height
        x = 0
        y = 0
        direction = 0
        while 1:
            cell = image.rgb[y][x]
            code = (65536 * cell[0] + 256 * cell[1] + cell[2]) % 11
            if   code == 0:
                self.commands.append('>')
            elif code == 1:
                self.commands.append('<')
            elif code == 2:
                self.commands.append('+')
            elif code == 3:
                self.commands.append('-')
            elif code == 4:
                self.commands.append('.')
            elif code == 5:
                self.commands.append(',')
            elif code == 6:
                self.commands.append('[')
            elif code == 7:
                self.commands.append(']')
            elif code == 8:
                direction = (direction + 1) % 4
            elif code == 9:
                direction = 3 if direction == 0 else direction - 1

            x, y = self.move(x, y, direction)
            if x == None:
                break
        self.data = ''.join(self.commands)
        self.program = BrainFuck(self.data, skipOptimalization = True)
