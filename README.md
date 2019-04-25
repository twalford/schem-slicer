# schem-slicer
Generate PNGs from Schematic.

Only supports textures in the 'blocks' folder.

# Usage
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
  -a  Generate a txt file with the block amounts
```
### examples
```
  run.py test.schematic x -n -f -c -a
  run.py test.schematic y -n -bg 255 255 255 
  run.py test.schematic z -g 
```
