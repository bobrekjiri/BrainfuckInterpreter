#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zlib


class PNGWrongHeaderError(Exception):
    """Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""
    pass


class PNGNotImplementedError(Exception):
    """Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""
    pass


class PngReader():
    """Třída pro práci s PNG-obrázky."""
    
    def byteArrayToNumber(self, array):
        return (array[0] << 24) + (array[1] << 16) + (array[2] << 8) + array[3]
    
    def __init__(self, filepath):
        
        with open(filepath, mode='br') as f:
            header = f.read(8)
            if header != b'\x89PNG\r\n\x1a\n':
                raise PNGWrongHeaderError()
            while 1:
                sizeData = f.read(4)
                chunkSize = self.byteArrayToNumber(sizeData)
                chunkType = f.read(4)
                chunkData = f.read(chunkSize)
                chunkCRC = f.read(4)
                computedCRC = zlib.crc32(chunkType + chunkData)
                givenCRC = self.byteArrayToNumber(chunkCRC)
                if computedCRC != givenCRC:
                    raise PNGNotImplementedError()
                if chunkType == b'IDAT':
                    pass
                elif chunkType == b'IHDR':
                    pass
                elif chunkType == b'IEND':
                    break
        
        
        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        self.rgb = []
        
        
        
        
        
        
        
        
