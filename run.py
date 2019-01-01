#Written by ilerm
#28/12/2018

#Made for splitting minecraft map art into rows.
#When used with redstonehelpers generator, use axis x.
#Only supports a specific set of textures. Add your own :)
 
import sys
import numpy
import nbt

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
  -c  Crop out the air at the top of the image
  -f  Flip the image left to right
  -n  Write the slice number on the image
  -g  Draw a grid (grey)
  -bg 0-255 0-255 0-255   Set the background colour (default blue-grey)

examples:
  run.py test.schematic x -n -f -c
  run.py test.schematic y -n -bg 255 255 255
  run.py test.schematic z -g"""

def main():
	##### Parse args #####
	if len(sys.argv) <= 2:
		print(strHelp)
		return
		
	doCrop = False
	doFlip = False
	doNumbering = False
	doGrid = False
	bg_R = 200
	bg_G = 200
	bg_B = 255
	
	filename = sys.argv[1]
	axis = sys.argv[2]
	
	if len(sys.argv) > 3:
		for i in range(len(sys.argv)):
			if sys.argv[i] == '-c':
				doCrop = True
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
	
	##### Load schematic #####
	infile = nbt.nbt.NBTFile(filename, 'rb')
	
	##### Load textures #####
	textures = []
	textures.insert(0, Image.open('./res/clay.png'))
	textures.insert(1, Image.open('./res/black_wool.png'))
	textures.insert(2, Image.open('./res/gray_clay.png'))
	textures.insert(3, Image.open('./res/cyan_clay.png'))
	textures.insert(4, Image.open('./res/gray_wool.png'))
	textures.insert(5, Image.open('./res/lgray_wool.png'))
	textures.insert(6, Image.open('./res/snow.png'))
	textures.insert(7, Image.open('./res/diorite.png'))
	textures.insert(8, Image.open('./res/stone.png'))
	textures.insert(9, Image.open('./res/diamond.png'))
	
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
	print ("do crop: {}".format(doCrop))
	print ("do flip: {}".format(doFlip))
	print ("do numbering: {}".format(doNumbering))
	print ("do grid {}".format(doGrid))
	print ("generating images...")
	
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
					
				id = infile['Blocks'][arrayPos]
				data = infile['Data'][arrayPos]
				
				if (id != 0):
					hasBlockinRow = True
				
				#pre 1.13 id's
				if (id == 35): #wool
					if data == 15:#black wool
						tex_index = 1
					elif data == 8:#light gray wool
						tex_index = 5
					elif data == 7:#gray wool
						tex_index = 4
					elif data == 0:#white wool
						tex_index = 6
				elif id == 159:#terracotta
					if data == 7:#gray terracotta
						tex_index = 2
					elif data == 9:#cyan terracotta
						tex_index = 3
				elif id == 1:#stone
					tex_index = 8
				elif id == 17:#birch log
					tex_index = 7
				elif id == 82:#clay
					tex_index = 0
				elif id == 57:#diamond
					tex_index = 9
				elif id == 20:#glass (show as dimaond)
					tex_index = 9
				elif id == 80:#snowblock
					tex_index = 6
				else:
					continue
				
				if (axis == 'y'):
					canvas.paste(textures[tex_index],(innerLoop*16, middleLoop*16)) #draws from top left (favour looking down for y axis)
				else:
					canvas.paste(textures[tex_index],(innerLoop*16, imgH - (middleLoop*16) - 16)) #draws from bottom left
					
				
				#end inner loop
				
			if (hasBlockinRow == True):
				hightestRowNonAir = middleLoop
			#end middle loop
		
		### Options ###
		if doCrop:
			canvas = canvas.crop((0,imgH - hightestRowNonAir*16 - 16,imgW,imgH)) #Crops out the image above hightestRowNonAir.
		if doFlip:
			canvas = canvas.transpose(Image.FLIP_LEFT_RIGHT) #Flips the image left-to-right
			
		draw = ImageDraw.Draw(canvas)
		if doNumbering:
			draw.text((2, imgH - 12), format(outerLoop)) #Draws the slice number in bottom left.
		if doGrid: #Draws a grid
			for i in range(innerRange):
				draw.line((i*16, 0, i*16, imgH), fill=(150,150,150))
			for j in range(middleRange):
				draw.line((0, j*16, imgW+16, j*16), fill=(150,150,150))
		
		del draw
		canvas.save("./out/{}.png".format(outerLoop)) #Saves the image
		
		print ("saved image {}".format(outerLoop))
		#end outer loop
		
	print ("finished. Check the out folder!")

if __name__ == '__main__':
	try:
		main()
	except:
		print(strHelp) # lol