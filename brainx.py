#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import image_png

class BrainFuck:
    """Interpretr jazyka brainfuck."""

    def getInput(self, data):
        tmp = data.split("!")
        if len(tmp) == 1:
            return ""
        return tmp[1]

    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""
        stack = list()
        dataPointer = 0
        self.data = data
        inputData = self.getInput(data)
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

    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""

        image = image_png.PngReader(filename)

        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        #self.program = BrainFuck(self.data)


class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""

    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""

        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)
