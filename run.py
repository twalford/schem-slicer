#Written by ilerm
#28/12/2018

#Made for splitting minecraft map art into rows.
#When used with redstonehelpers generator, use axis x.
#Only supports a specific set of textures. Add your own :)
 
import sys
import numpy
import nbt
import glob

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
	try:
		for f in glob.glob('./blocks/*'):
			textures.append(Image.open(f))
	except:
		print("print error loading textures")
		
	tmap = [
		[0],#0
		[174,179,180,177,178,175,176],#1
		[84],#2
		[52,11,53],#3
		[12],#4
		[133,134,131,132,129,130],#5
		[0],#6
		[1],#7
		[0],#8
		[0],#9
		[0],#10
		[0],#11
		[162,152],#12
		[85],#13
		[83],#14
		[107],#15
		[10],#16
		[116,117,114,115],#17
		[0],#18
		[172,173],#19
		[0],#20
		[11],#21
		[110],#22
		[54],#23
		[165,164,166],#24
		[126],#25
		[0],#26
		[0],#27
		[0],#28
		[0],#29
		[189],#30
		[0],#31
		[0],#32
		[0],#33
		[0],#34
		[204,199,198,196,205,197,200,194,203,193,201,191,192,195,202,190],#35
		[0],#36
		[0],#37
		[0],#38
		[0],#39
		[0],#40
		[82],#41
		[106],#42
		[0],#43
		[0],#44
		[4],#45
		[187],#46
		[3],#47
		[13],#48
		[128],#49
		[0],#50
		[0],#51
		[0],#52
		[0],#53
		[0],#54
		[0],#55
		[51],#56
		[50],#57
		[46],#58
		[0],#59
		[0],#60
		[61],#61
		[62],#62
		[0],#63
		[0],#64
		[0],#65
		[0],#66
		[0],#67
		[0],#68
		[0],#69
		[0],#70
		[0],#71
		[0],#72
		[161],#73
		[161],#74
		[0],#75
		[0],#76
		[0],#77
		[170],#78
		[104],#79
		[170],#80
		[5],#81
		[8],#82
		[0],#83
		[109],#84
		[0],#85
		[140],#86
		[125],#87
		[171],#88
		[81],#89
		[0],#90
		[139],#91
		[6],#92
		[0],#93
		[0],#94
		[0],#95
		[188],#96
		[174,12,183,186,185,184],#97
		[183,186,185,184],#98
		[120],#99
		[121],#100
		[0],#101
		[0],#102
		[119],#103
		[0],#104
		[0],#105
		[0],#106
		[0],#107
		[0],#108
		[0],#109
		[112],#110
		[0],#111
		[123],#112
		[0],#113
		[0],#114
		[0],#115
		[58],#116
		[0],#117
		[7],#118
		[0],#119
		[0],#120
		[60],#121
		[0],#122
		[159],#123
		[160],#124
		[0],#125
		[0],#126
		[0],#127
		[0],#128
		[57],#129
		[0],#130
		[0],#131
		[0],#132
		[56],#133
		[0],#134
		[0],#135
		[0],#136
		[0],#137
		[0],#138
		[0],#139
		[0],#140
		[0],#141
		[0],#142
		[0],#143
		[0],#144
		[0],#145
		[0],#146
		[0],#147
		[0],#148
		[0],#149
		[0],#150
		[49],#151
		[158],#152
		[150],#153
		[0],#154
		[149,144,146],#155
		[0],#156
		[0],#157
		[55],#158
		[101,96,95,93,102,94,97,91,100,90,98,88,89,92,99,87],#159
		[0],#160
		[0],#161
		[112,113],#162
		[0],#163
		[0],#164
		[169],#165
		[0],#166
		[108],#167
		[137,135,136],#168
		[168],#169
		[103],#170
		[0],#171
		[86],#172
		[9],#173
		[105],#174
		[0],#175
		[0],#176
		[0],#177
		[48],#178
		[155,154,156],#179
		[0],#180
		[0],#181
		[0],#182
		[0],#183
		[0],#184
		[0],#185
		[0],#186
		[0],#187
		[0],#188
		[0],#189
		[0],#190
		[0],#191
		[0],#192
		[0],#193
		[0],#194
		[0],#195
		[0],#196
		[0],#197
		[0],#198
		[0],#199
		[0],#200
		[141],#201
		[142],#202
		[0],#203
		[0],#204
		[0],#205
		[59],#206
		[0],#207
		[0],#208
		[0],#209
		[0],#210
		[0],#211
		[0],#212
		[118],#213
		[124],#214
		[151],#215
		[2],#216
		[0],#217
		[127],#218
		[0],#219
		[0],#220
		[0],#221
		[0],#222
		[0],#223
		[0],#224
		[0],#225
		[0],#226
		[0],#227
		[0],#228
		[0],#229
		[0],#230
		[0],#231
		[0],#232
		[0],#233
		[0],#234
		[79],#235
		[74],#236
		[73],#237
		[71],#238
		[80],#239
		[72],#240
		[75],#241
		[69],#242
		[78],#243
		[68],#244
		[76],#245
		[66],#246
		[67],#247
		[70],#248
		[77],#249
		[65],#250
		[44,23,22,20,45,21,24,18,43,17,41,15,16,19,42,14],#251
		[39,34,33,31,40,32,35,29,38,28,36,26,27,30,37,25],#252
	]
	
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
				
				#bitwise adjustment to correct Log data/orientation
				if (id == 17 or id == 162):
					data &= 2
					
				#texture index lookup
				if (id != 0):	
					try:
						tex_index = tmap[id][data]
					except:
						print("cant find texture for {}:{}".format(id,data))
						continue
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