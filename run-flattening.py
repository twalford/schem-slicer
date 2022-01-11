#Written by ilerm
#28/12/2018

#Made for splitting minecraft map art into rows.
#When used with redstonehelpers generator, use axis x.
#Only supports a specific set of textures. Add your own :)
 
import sys
import numpy
import nbt
import glob
import os
import re

from PIL import Image, ImageFont, ImageDraw
from numpy import array, zeros, fromstring
from io import StringIO

strHelp = """
Usage: run.py path axis [options]
  path:  The path to your schematic file
  axis:  The axis to slice into images. Must be x, y, or z
    x: Looking East. Image 0 is the west-most layer
    y: Top down. Image 0 is the bottom layer
    z: Looking North. Image 0 is the north-most layer

options:
  -f  Flip the image left to right
  -n  Write the slice number on the image
  -g  Draw a grid (grey)
  -bg 0-255 0-255 0-255   Set the background colour (default blue-grey)
  -a  Generate a txt file with the block amounts

examples:
  run.py test.schematic x -n -f -c
  run.py test.schematic y -n -bg 255 255 255
  run.py test.schematic z -g"""

def main():
	##### Parse args #####
	if len(sys.argv) <= 2:
		print(strHelp)
		return
		
	doFlip = False
	doNumbering = False
	doGrid = False
	doAnalysis = False
	bg_R = 200
	bg_G = 200
	bg_B = 255
	
	filename = sys.argv[1]
	axis = sys.argv[2]
	
	if len(sys.argv) > 3:
		for i in range(len(sys.argv)):
			if sys.argv[i] == '-f':
				doFlip = True
			if sys.argv[i] == '-n':
				doNumbering = True
			if sys.argv[i] == '-g':
				doGrid = True
			if sys.argv[i] == '-bg':
				bg_R = int(sys.argv[i+1])
				bg_G = int(sys.argv[i+2])
				bg_B = int(sys.argv[i+3])	
			if sys.argv[i] == '-a':
				doAnalysis = True
	
	##### Load schematic #####
	infile = nbt.nbt.NBTFile(filename, 'rb')
	#print(infile.pretty_tree())
	
	#### Load font
	if doNumbering:
		font = ImageFont.truetype("./OpenSans-Medium.ttf", 15)
	
	#### Read Palette and build blockList
	blockList = []
	airId = -1
	for blockName in infile['Palette']:
		blockNameBits = re.search("^minecraft:([^[]+)(.*)$", blockName)
		if blockNameBits is not None:
			blockId = infile['Palette'][blockName].value
			blockNameShort = blockNameBits.group(1)
			blockNameFull = blockNameBits.group(1) + blockNameBits.group(2)
			blockList.append([blockId, blockNameShort, blockNameFull])
			if blockNameShort == 'air':
				airId = blockId
		else:
			raise ValueError("Couldn't parse block Name {}".format(blockName))
	
	##### Load needed texture images #####
	textures = []
	try:
		for fileName in glob.glob('./textures/*'):
			fileNameBits = re.search("[\\\\/]([^\\\\/]+).png$", fileName)
			if fileNameBits is not None:
				blockName = fileNameBits.group(1)
				for blockItem in blockList:
					if blockItem[1] == blockName:
						textureImage = Image.open(fileName)
						textureImage = textureImage.crop((0,0,16,16)) # only use first frame if animation
						textures.append([blockItem[0], blockItem[1], blockItem[2], textureImage, 0])
	except:
		raise
		print("print error loading textures")
	
	##### Prepare loops#####
	width = infile['Width'].value
	length = infile['Length'].value
	height = infile['Height'].value

	imgW = 0 #pixel width of the images
	imgH = 0 #pixel height of the images
	size = (0,0) #pixel dimensions of the images 
	
	if axis == 'x':
		outerRange = width
		middleRange = height
		innerRange = length
	if axis == 'y':
		outerRange = height
		middleRange = length
		innerRange = width
	if axis == 'z':
		outerRange = length
		middleRange = height
		innerRange = width
	
	imgW = 16 * innerRange
	imgH = 16 * middleRange
	size = (imgW, imgH)
	
	##### Display settings #####
	print ("image width: {}".format(imgW))
	print ("image height: {}".format(imgH))
	print ("axis: {}".format(axis))
	print ("do flip: {}".format(doFlip))
	print ("do numbering: {}".format(doNumbering))
	print ("do grid {}".format(doGrid))
	print ("generating images...")
	
	if not os.path.exists('./out/'):
		os.makedirs('./out/')

	##### Generate images #####
	for outerLoop in range(outerRange):
		hightestRowNonAir = 0
		canvas = Image.new('RGB',size,(bg_R,bg_G,bg_B))
		
		for middleLoop in range(middleRange):
			
			hasBlockinRow = False
			for innerLoop in range(innerRange):
				
				if axis == 'x':
					arrayPos = (middleLoop * length + innerLoop) * width + outerLoop
				if axis == 'y':
					arrayPos = (outerLoop * length + middleLoop) * width + innerLoop
				if axis == 'z':
					arrayPos = (middleLoop * length + outerLoop) * width + innerLoop
				
				id = infile['BlockData'][arrayPos]
				if id == airId:
					continue
					
				hasBlockinRow = True
				found = False
				for texture in textures:
					if texture[0] == id:
						found = True
						texture[4] += 1
						break
				if found:
					textureImage = texture[3]
				else:
					found = False
					for blockItem in blockList:
						if blockItem[0] == id:
							found = True
							break
					if found:
						raise ValueError("Missing texture file {}.png".format(blockItem[1]))
					else:
						raise ValueError("Couldn't find id {} in Palette".format(id))
					exit()
				
				if (axis == 'y'):
					canvas.paste(textureImage,(innerLoop*16, middleLoop*16)) #draws from top left (favour looking down for y axis)
				else:
					canvas.paste(textureImage,(innerLoop*16, imgH - (middleLoop*16) - 16)) #draws from bottom left
					
				
				#end inner loop
				
			if (hasBlockinRow == True):
				hightestRowNonAir = middleLoop
			#end middle loop
		
		### Options ###
		if doFlip:
			canvas = canvas.transpose(Image.FLIP_LEFT_RIGHT) #Flips the image left-to-right
			
		sliceNo = height-outerLoop
			
		draw = ImageDraw.Draw(canvas)
		if doNumbering:
			draw.text((3, imgH - 19), format(sliceNo), font=font, fill=(0,0,0)) #Draws the slice number in bottom left.
		if doGrid: #Draws a grid
			for i in range(innerRange):
				draw.line((i*16, 0, i*16, imgH), fill=(150,150,150))
			for j in range(middleRange):
				draw.line((0, j*16, imgW+16, j*16), fill=(150,150,150))
		
		del draw
		canvas.save("./out/{}.png".format(sliceNo)) #Saves the image
		
		print ("saved image {}".format(sliceNo))
		#end outer loop
	
	if (doAnalysis):
		f = open("out/analysis.txt","w")
		for texture in textures:
			f.write("{} {}\n".format(texture[2],texture[4]))
		f.close()
		print("Analysis saved to file")
	
	print ("finished. Check the out folder!")

if __name__ == '__main__':
	main()