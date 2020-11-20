from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

image = Image.open('outputs/outmario.png')

image.show()
print(image.size)
#pixels = image.load()
#test2 outlining the image
width, height = image.size
print(width,height)
previousColor = ()
outline = []
rgb = image.convert('RGB')
for y in range(height):
   for x in range(width):
    currentColor = rgb.getpixel((x,y))
    if currentColor != previousColor:
        outline.append((x,y))
        previousColor = currentColor
for x in range(width):
   for y in range(height):
    currentColor = rgb.getpixel((x,y))
    if currentColor != previousColor:
        outline.append((x,y))
        previousColor = currentColor
   
outimg = Image.new(image.mode,image.size)
#newim.show()
for y in range(height):
   for x in range(width):
      outimg.putpixel((x,y),(255,255,255))
for i in outline:
   outimg.putpixel(i, (0, 0, 0)) 
ImageEnhance.Sharpness(outimg).enhance(1.6)
outimg.show()
outimg.save("outputs/outlinedmario.png")    

