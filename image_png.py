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

    def paeth(self, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            return a
        elif pb <= pc:
            return b
        else:
            return c

    def getScanlines(self, data):
        lines = []
        for i in range(self.height):
            linedata = []
            base = i*((self.width * 3) + 1)
            for j in range(self.width):
                offset = j * 3
                rgb = (data[base + offset + 1], data[base + offset + 2], data[base + offset + 3])
                linedata.append(rgb)
            lines.append((data[base], linedata))
        return lines

    def decode(self, lines):
        output = []
        for i in range(self.height):
            linefilter = lines[i][0]
            linedata   = lines[i][1]
            if   linefilter == 0:
                output.append(linedata)
            elif linefilter == 1:
                newlinedata = []
                newlinedata.append(linedata[0])
                for j in range(1,len(linedata)):
                    r = (linedata[j][0] + newlinedata[j-1][0]) % 256
                    g = (linedata[j][1] + newlinedata[j-1][1]) % 256
                    b = (linedata[j][2] + newlinedata[j-1][2]) % 256
                    newlinedata.append((r, g, b))
                output.append(newlinedata)
            elif linefilter == 2:
                if i == 0:
                    output.append(linedata)
                else:
                    newlinedata = []
                    for j in range(0,len(linedata)):
                        r = (linedata[j][0] + output[i-1][j][0]) % 256
                        g = (linedata[j][1] + output[i-1][j][1]) % 256
                        b = (linedata[j][2] + output[i-1][j][2]) % 256
                        newlinedata.append((r, g, b))
                    output.append(newlinedata)
            elif linefilter == 3:
                newlinedata = []
                for j in range(0,len(linedata)):
                    fr = ((0 if j == 0 else newlinedata[j-1][0]) + (0 if i == 0 else output[i-1][j][0])) // 2
                    fg = ((0 if j == 0 else newlinedata[j-1][1]) + (0 if i == 0 else output[i-1][j][1])) // 2
                    fb = ((0 if j == 0 else newlinedata[j-1][2]) + (0 if i == 0 else output[i-1][j][2])) // 2
                    r = (linedata[j][0] + fr) % 256
                    g = (linedata[j][1] + fg) % 256
                    b = (linedata[j][2] + fb) % 256
                    newlinedata.append((r, g, b))
                output.append(newlinedata)
            elif linefilter == 4:
                newlinedata = []
                for j in range(0,len(linedata)):
                    ra = 0 if           j == 0  else newlinedata[j-1][0]
                    rb = 0 if i == 0            else output[i-1][j  ][0]
                    rc = 0 if i == 0 or j == 0  else output[i-1][j-1][0]

                    ga = 0 if           j == 0  else newlinedata[j-1][1]
                    gb = 0 if i == 0            else output[i-1][j  ][1]
                    gc = 0 if i == 0 or j == 0  else output[i-1][j-1][1]

                    ba = 0 if           j == 0  else newlinedata[j-1][2]
                    bb = 0 if i == 0            else output[i-1][j  ][2]
                    bc = 0 if i == 0 or j == 0  else output[i-1][j-1][2]

                    r = (linedata[j][0] + self.paeth(ra, rb, rc)) % 256
                    g = (linedata[j][1] + self.paeth(ga, gb, gc)) % 256
                    b = (linedata[j][2] + self.paeth(ba, bb, bc)) % 256
                    newlinedata.append((r, g, b))
                output.append(newlinedata)
        return output

    def __init__(self, filepath):
        data = bytearray()

        with open(filepath, mode='br') as f:
            header = f.read(8)
            if header != b'\x89PNG\r\n\x1a\n':
                raise PNGWrongHeaderError()
            while 1:
                sizeData  = f.read(4)
                chunkSize = self.byteArrayToNumber(sizeData)
                chunkType = f.read(4)
                chunkData = f.read(chunkSize)
                chunkCRC  = f.read(4)
                computedCRC = zlib.crc32(chunkType + chunkData)
                givenCRC  = self.byteArrayToNumber(chunkCRC)
                if computedCRC != givenCRC:
                    raise PNGNotImplementedError()
                if   chunkType == b'IDAT':
                    data += chunkData
                elif chunkType == b'IHDR':
                    self.width  = self.byteArrayToNumber(chunkData[0:4])
                    self.height = self.byteArrayToNumber(chunkData[4:8])
                    if chunkData[8:] != b'\x08\x02\x00\x00\x00':
                        raise PNGNotImplementedError()
                elif chunkType == b'IEND':
                    break

        decompressed = zlib.decompress(data)
        lines = self.getScanlines(decompressed)

        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        self.rgb = self.decode(lines)
