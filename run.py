#written by ilerm
#28/12/2018
import numpy
import nbt
from PIL import Image, ImageFont, ImageDraw


from numpy import array, zeros, fromstring
from io import StringIO
'''
size = (100, 100)
canvas = Image.new('RGB',size,(200,200,255))
draw = ImageDraw.Draw(canvas)
draw.text((10, 10), "hello")
canvas.show()
'''
filename = "test.schematic"
infile = nbt.nbt.NBTFile(filename, 'rb')

width = infile['Width'].value
length = infile['Length'].value
height = infile['Height'].value

##### Load textures #####
i_clay = Image.open('./res/clay.png')
i_black_wool = Image.open('./res/black_wool.png')
i_gray_clay = Image.open('./res/gray_clay.png')
i_cyan_clay = Image.open('./res/cyan_clay.png')
i_gray_wool = Image.open('./res/gray_wool.png')
i_lgray_wool = Image.open('./res/lgray_wool.png')
i_snow = Image.open('./res/snow.png')
i_diorite = Image.open('./res/diorite.png')
i_stone = Image.open('./res/stone.png')
i_diamond = Image.open('./res/diamond.png')

textures = [i_clay, #0
i_black_wool, 		#1
i_gray_clay ,		#2
i_cyan_clay ,		#3
i_gray_wool ,		#4
i_lgray_wool,		#5
i_snow,				#6
i_diorite,			#7
i_stone,			#8
i_diamond]			#9

sizeZ = 16*length
sizeY = 16*height
size = (sizeZ, sizeY)
topY = 0
hasBlockinRow = False

##### Generate images #####
for x in range(width):
	if (x < 50):
		continue
		
	topY = 0
	canvas = Image.new('RGB',size,(200,200,255))
	
	for y in range(height):
		hasBlockinRow = False
		for z in range(length):
			arrayPos = (y * length + z) * width + x
			id = infile['Blocks'][arrayPos]
			data = infile['Data'][arrayPos]
			
			#print("{}, {}, {}".format(arrayPos, id, data))
			if (id != 0):
				hasBlockinRow = True
				
			if arrayPos == 1:
				id = 0
			if (id == 35): #wool
				if (data == 15):#black wool
					tex_index = 1
				elif (data == 8):#light gray wool
					tex_index = 5
				elif (data == 7):#gray wool
					tex_index = 4
				elif (data == 0):#white wool
					tex_index = 6
			elif (id == 159):#terracotta
				if (data == 7):#gray terracotta
					tex_index = 2
				elif(data == 9):#cyan terracotta
					tex_index = 3
			elif (id == 1):#stone
				tex_index = 8
			elif (id == 17):#birch log
				tex_index = 7
			elif (id == 82):#clay
				tex_index = 0
			elif (id == 57):#diamond
				tex_index = 9
			elif (id == 20):#glass
				tex_index = 9
			else:
				continue
			
			canvas.paste(textures[tex_index],(z*16, sizeY - (y*16) - 16, z*16 + 16, sizeY - (y*16)))
		canvas.paste(textures[9],(sizeZ - 16,sizeY - (y*16) - 16,sizeZ,sizeY - (y*16)))
			
		if (hasBlockinRow == True):
			topY = y
	
	draw = ImageDraw.Draw(canvas)
	draw.text(((sizeZ) - 20, sizeY - 64), format(x))
	ci = canvas.crop((0,sizeY - topY*16 - 16,sizeZ,sizeY))
	ci.save('./out/{}.png'.format(x))
	
	print ("saved image {}".format(x))
print ("finished")
