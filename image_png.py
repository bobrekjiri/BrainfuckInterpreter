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
    
    def getScanlines(self, data):
        lines = []
        return lines
    
    def __init__(self, filepath):
        data = bytearray()
        
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
                    data += chunkData
                elif chunkType == b'IHDR':
                    self.height = self.byteArrayToNumber(chunkData[0:4])
                    self.width = self.byteArrayToNumber(chunkData[4:8])
                    if chunkData[8:] != b'\x08\x02\x00\x00\x00':
                        raise PNGNotImplementedError()
                elif chunkType == b'IEND':
                    break
            
            decompressed = zlib.decompress(data)
            print(decompressed)
            lines = self.getScanlines(decompressed)
            
        
        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        self.rgb = []
        
        
        
        
        
        
        
        
