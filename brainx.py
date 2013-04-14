#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""
        stack = list()
        dataPointer = 0
        self.data = data
        dataLength = len(self.data)
        
        # inicializace proměnných
        self.memory = bytearray(memory)
        self.memoryPointer = memory_pointer
        memoryLength = len(self.memory)
        
        # DEBUG a testy
        # a) paměť výstupu
        self.output = ''
    
        while 1:
            x = self.data[dataPointer]
            if x == '+':
                self.memory[self.memoryPointer] += 1

            if x == '-':
                self.memory[self.memoryPointer] -= 1

            if x == '>':
                self.memoryPointer += 1
                if self.memoryPointer == memoryLength:
                    self.memory.append(0)
                    memoryLength += 1

            if x == '<':
                self.memoryPointer -= 0 if self.memoryPointer == 0 else 1

            if x == '[':
                if self.memory[self.memoryPointer] > 0:
                    stack.append(dataPointer)
                else:
                    while self.data[dataPointer] != ']':
                        dataPointer += 1

            if x == ']':
                if self.memory[self.memoryPointer] == 0:
                    stack.pop()
                else:
                    dataPointer = stack[len(stack)-1]
            dataPointer += 1;

            if x == '.':
                self.output = self.output + chr(self.memory[self.memoryPointer])

            if dataPointer == dataLength:
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
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""
    
    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


