#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class PNGWrongHeaderError(Exception):
    """Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""
    pass


class PNGNotImplementedError(Exception):
    """Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""
    pass


class PngReader():
    """Třída pro práci s PNG-obrázky."""
    
    def __init__(self, filepath):
        
        with open(filepath, mode='br') as f:
            header = f.read(8)
            if header != b'\x89PNG\r\n\x1a\n':
                raise PNGWrongHeaderError()
            while 1:
                sizeData = f.read(4)
                chunkSize = (sizeData[0] << 24) + (sizeData[1] << 16) + (sizeData[2] << 8) + sizeData[3]
                print(chunkSize)
                chunkType = f.read(4)
                print(chunkType)
                chunkData = f.read(chunkSize)
                print(chunkData)
                chunkCRC = f.read(4)
                print(chunkCRC)
                break
        
        
        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        self.rgb = []
        
        
        
        
        
        
        
        
