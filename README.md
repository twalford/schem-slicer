# schem-slicer
Generate PNGs from Schematic.

Perfect for creating Minecraft map art in survival mode.

run.py only supports textures in the 'blocks' folder (see also Minecraft versions 1.13+ / Textures below).

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

# Minecraft versions 1.13+

1.13 removed numeric block IDs and changed NBT tags, in the change known as "The Flattening".

Schematics saved in these newer Minecraft versions store the block data in NBT tag 'BlockData' rather than 'Blocks' and 'Data'.
For this newer format data, use **slicer.py** instead.  Options are the same as run.py except -c is not implemented.

### Textures

slicer.py uses images from textures/ rather than blocks/

These are copied from the default Minecraft 1.17.1 resource pack, a merge of these 2 directories: minecraft/textures/block/ minecraft/textures/item/

It needs weeding out as it currently contains many non-placeable items as well as duplicate/redundant orientations. Some blocks may also be missing or need renaming to match the actual minecraft resource names.

If you get error: "Missing texture file ......." then you'll need to add the missing file.