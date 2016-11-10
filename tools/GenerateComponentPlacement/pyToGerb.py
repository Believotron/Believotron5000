#!/usr/bin/env python
import csv
import os

def PrintGerberHeader():
    f.write("%FSLAX33Y33*%\n")
    f.write("%MOMM*%\n")
    f.write("%ADD10C,0.381*%\n")
    f.write("D10*\n")
    f.write("%LNpath-145*%\n")
    f.write("G01*\n")
    return

def PrintGerberFooter():
    f.write("%LNmechanical details_traces*%\n")
    f.write("M02*")
    return

def PrintGerberMoveTo(xy):
    f.write("X"+str(xy[0])+"Y"+str(xy[1])+"D02*\n")
    return

def PrintStartLine(xy):
    f.write("X"+str(xy[0])+"Y"+str(xy[1])+"D01*\n")
    return

def PrintLineContinue(xy):
    f.write("X"+str(xy[0])+"Y"+str(xy[1])+"*\n")

def PrintGerberDrawList(coords):
    PrintGerberMoveTo(coords[0])
    PrintStartLine(coords[1])
    shortCoords = coords
    shortCoords.pop(0)
    shortCoords.pop(0)
    for coordinate in shortCoords:
        PrintLineContinue(coordinate)
    return



def PrintRectangle(x, y, width, height, orientation):
    tempx=0
    tempy=0

    #print orientation
    # 90 degress, rect is taller than wide
    if ((orientation=="90") or (orientation=="270") ):
        tempx=width
        tempy=height
        width  = tempy
        height = tempx
        #print "wubba"

    x0 = int(x-float(width/2.0))
    x1 = int(x+float(width/2.0))
    y0 = int(y-float(height/2.0))
    y1 = int(y+float(height/2.0))

    theseCoords = [[x0,y0], [x1,y0], [x1,y1], [x0,y1], [x0,y0]]
    PrintGerberDrawList(theseCoords)
    return

#------------------------------------------------------------------------------
#f = open('tempGerber.gko', 'w')
#PrintGerberHeader();


# open parts list
with open('BOM.csv', 'rb') as fIn:
    reader = csv.reader(fIn)
    your_list = list(reader)

# open xy list
with open('partxy.csv', 'rb') as fxy:
    reader = csv.reader(fxy)
    listxy = list(reader)

if "J18" in listxy:
    print "artichoke"

for part in your_list:
    partNumber = part[3]
    refdes = part[0].split()

    PNSanitized = partNumber.replace("/", "")

    filename = "output\gerbXY_" + PNSanitized + ".gko"
    f = open(filename, 'w')
    PrintGerberHeader()

    #f.write("doomslayer 0001\n")

    # Original Board outline
    f.write("X0Y0D02*\n")
    f.write("X218200Y0D01*\n")
    f.write("X218200Y128500*\n")
    f.write("X0Y128500*\n")
    f.write("X0Y0*\n")

    for line in listxy:
        thisRefdes = line[0]
        boardSide = line[1]
        for part in refdes:
            #print part
            if part == thisRefdes:
                if boardSide == "top":
                    xInches = float(line[2]) / 1000.0
                    yInches = float(line[3]) / 1000.0
                    xmm = xInches * 25.4
                    ymm = yInches * 25.4
                    xGerber = int( xmm * 1000 )
                    yGerber = int( ymm * 1000 )
                    orientation = line[4]
                    PrintRectangle(xGerber,yGerber,3000.0,1500.0,orientation) # need to add rotation checking

                    #f.write(thisRefdes + ", [" + str(xGerber) + ", " + str(xGerber) + "]" + ", [" + str(xmm) + ", " + str(ymm) + "]" + ", [" + str(xInches) + ", " + str(yInches) +"\n" )
                    ##print filename + " " + part

    #PrintRectangle(1000,1000,1000,500,1)

    PrintGerberFooter()
    f.close()
    pasteFile   = ".\Believotron_Wanderlust_Beta0_C.gtp"
    outlineFile = ".\Believotron_Wanderlust_Beta0_C.gko"
    outputFile  = ".\PDFs\partxy_" + PNSanitized + ".pdf"
    #filename    = ".\Believotron_Wanderlust_Beta0_C.gto"
    #command = "gerbv -b#FFFFFF " + pasteFile + " -f#000000 " + outlineFile + " -f#000000 " + filename + " -f#FF0000 -o " + outputFile + " -x pdf"
    command  = "gerbv -b#FFFFFF "
    command += pasteFile   + " -f#000000 "
    #command += outlineFile + " -f#000000 "
    #filename = ".\output\gerbXY_APA102C.gko"
    #command += filename    + " -f#FF0000"
    command += ".\\" +filename    + " -f#FF0000"

    command += " -o " + outputFile + " -x pdf"
    print command
    os.system(command)
    #filename
    #gerbv -b#FFFFFF .\Believotron_Wanderlust_Beta0_C.gtp -f#FF0000 .\Believotron_Wanderlust_Beta0_C.gko -f#00FF00 -o foolala.pdf -x pdf

# works
"gerbv -b#FFFFFF .\Believotron_Wanderlust_Beta0_C.gtp -f#000000 .\output\gerbXY_APA102C.gko -f#FF0000 -o .\PDFs\partxy_APA102C.pdf -x pdf"
# doesn't work
"gerbv -b#FFFFFF .\Believotron_Wanderlust_Beta0_C.gtp -f#000000 .\output\gerbXY_APA102C.gko -f#FF0000 -o .\PDFs\partxy_APA102C.pdf -x pdf"
"gerbv -b#FFFFFF .\Believotron_Wanderlust_Beta0_C.gtp -f#000000 output\gerbXY_APA102C.gko -f#FF0000 -o .\PDFs\partxy_APA102C.pdf -x pdf"



#f.write("blacklist\n")
#for item in blacklist:
#    print item
#    f.write(str(item)+"\n")
#f.write("endblacklist\n")

# open xy placement file
