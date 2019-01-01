# schem-slicer
Generate PNGs from Schematic.

Does not support all textures!!!! You will need to add your own texture files and change the code.

# Usage
Create an empty folder named "out"
### run.py path axis [options]
```
  path:  The path to your schematic file 
  axis:  The axis to slice into images. Must be x, y, or z 
    x: Looking East. Image 0 is the west-most layer 
    y: Top down. Image 0 is the bottom layer 
    z: Looking North. Image 0 is the north-most layer 
```
### options
```
  -c  Crop out the air at the top of the image
  -f  Flip the image left to right
  -n  Write the slice number on the image
  -g  Draw a grid (grey)
  -bg 0-255 0-255 0-255   Set the background colour (default blue-grey)
```
### examples
```
  run.py test.schematic x -n -f -c 
  run.py test.schematic y -n -bg 255 255 255 
  run.py test.schematic z -g 
```
