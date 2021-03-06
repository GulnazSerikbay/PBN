#Name: Gulnaz Serikbay
""" Description: Backend of the project - Image Processing """

from __future__ import division
from tkinter import *
from tkinter import filedialog,ttk
from PIL import Image, ImageTk, ImageFilter,ImageEnhance, ImageFont, ImageDraw
import random, math, time
from collections import Counter, defaultdict, namedtuple
import numpy as np
#implement class structure

class Processing:
  
  def __init__(self, wnd, imagestate, file = "", N = 0, clrrange = 16):
    self.inpfile = file
    self.master = wnd
    
    self.master.update()
    total_time = time.time()
    self.clrrange = clrrange
    
    self.OUTPUT_ALL = True # Whether to output the image at each step
    self.OUTFILE_STEM = "out"

    self.FLOOD_FILL_TOLERANCE = 10
    self.CLOSE_CELL_TOLERANCE = 5
    self.SMALL_CELL_THRESHOLD = 10
    self.HEIGHT = 520
    self.N = N
    if self.master:
      #display in the canvas
      self.state = StringVar()
      self.state.set("Processing started")
      self.imagestate = Label(self.master, textvariable = self.state, font = ("Verdana", 14))
      self.imagestate.place(x = 370, y = 590, width = 500)
      self.master.update()

    self.cell_sets, self.cell_means, self.image = self.processToNCells(self.N)
    
    self.palette = self.clustering()
    self.cell_centers = self.findCenters()
    self.outimage = self.outline()
    self.placeNumbers()
    self.createHexPalette()
    self.state.set("Done! (Time taken: {})".format(time.time() - total_time))
    self.master.update()
 
  #Color conversion functions
  # http://www.easyrgb.com/?X=MATH    
  def rgb2xyz(self,rgb):
    r,g,b=rgb;r/=255;g/=255;b/=255;r=((r+0.055)/1.055)**2.4 if r>0.04045 else r/12.92
    g=((g+0.055)/1.055)**2.4 if g>0.04045 else g/12.92;b=((b+0.055)/1.055)**2.4 if b>0.04045 else b/12.92
    r*=100;g*=100;b*=100;x=r*0.4124+g*0.3576+b*0.1805;y=r*0.2126+g*0.7152+b*0.0722
    z=r*0.0193+g*0.1192+b*0.9505;return(x,y,z)
  def xyz2lab(self,xyz):
    x,y,z=xyz;x/=95.047;y/=100;z/=108.883;x=x**(1/3)if x>0.008856 else 7.787*x+16/116
    y=y**(1/3)if y>0.008856 else 7.787*y+16/116;z=z**(1/3)if z>0.008856 else 7.787*z + 16/116
    L=116*y-16;a=500*(x-y);b=200*(y-z);return(L,a,b)
  def rgb2lab(self,rgb):return self.xyz2lab(self.rgb2xyz(rgb))
  def lab2xyz(self,lab):
    L,a,b=lab;y=(L+16)/116;x=a/500+y;z=y-b/200;y=y**3 if y**3>0.008856 else(y-16/116)/7.787
    x=x**3 if x**3>0.008856 else (x-16/116)/7.787;z=z**3 if z**3>0.008856 else(z-16/116)/7.787
    x*=95.047;y*=100;z*=108.883;return(x,y,z)
  def xyz2rgb(self,xyz):
    x,y,z=xyz;x/=100;y/=100;z/=100;r=x*3.2406+y*-1.5372+z*-0.4986
    g=x*-0.9689+y*1.8758+z*0.0415;b=x*0.0557+y*-0.2040+z*1.0570
    r=1.055*(r**(1/2.4))-0.055 if r>0.0031308 else 12.92*r;g=1.055*(g**(1/2.4))-0.055 if g>0.0031308 else 12.92*g
    b=1.055*(b**(1/2.4))-0.055 if b>0.0031308 else 12.92*b;r*=255;g*=255;b*=255;return(r,g,b)
  def lab2rgb(self,lab):rgb=self.xyz2rgb(self.lab2xyz(lab));return tuple([int(round(x))for x in rgb])
  
  X = range
  def neighbours(self,pixel):
      nb = []
      neighbours = [(pixel[0]+1, pixel[1]), (pixel[0]-1, pixel[1]),
                (pixel[0], pixel[1]+1), (pixel[0], pixel[1]-1)]
      for neighbour in neighbours:
        if 0 <= neighbour[0] < self.width and 0 <= neighbour[1] < self.height:
          nb.append(neighbour)
      return nb
  
  def processToNCells(self, N):
    """
    Stage 1: Read the image with PIL and convert to CIELAB(color)
    """
    im = Image.open(self.inpfile)
    width, height = im.size
    area = width*height
    if N == 15:
      if 1 <= area <= 60000:
        N = 15
      elif 60000 <= area <= 80000:
        N = 20
      elif 80000 < area <= 300000:
        N = 50
      elif area> 300000:
        N = 70
    if not (height == self.HEIGHT):
      im = im.resize((width*self.HEIGHT//height,self.HEIGHT))

    self.width,self.height = im.size
    width,height = self.width,self.height #used in this function
    
    if self.OUTPUT_ALL:
      im.save(self.OUTFILE_STEM + "0.png")

    def createPixlab(im):
      width, height = im.size
      pixlab_map = {}
      for i in range(width):
        for j in range(height):
          pixlab_map[(i, j)] = self.rgb2lab(im.getpixel((i, j)))
      return pixlab_map

    pixlab_map = createPixlab(im)
    self.state.set("Stage 1: CIELAB conversion complete")
    self.master.update()

    '''Algorithms in this function are adapted from:
    https://codegolf.stackexchange.com/questions/42217/paint-by-numbers
    It generates the pixel map, makes the image more convenient for further changes
    Was written in python2 and algorithms were repeated, I avoided repetitions, adapted some variables according to my project 
    contains my codelines
    '''
    """
    Stage 2: Partitioning the image into like-colored cells using flood fill
    """
    #color difference
    def d(color1, color2):
      return (abs(color1[0]-color2[0])**2 + abs(color1[1]-color2[1])**2 + abs(color1[2]-color2[2])**2)**.5

    def neighbours(pixel):
      nb = []
      neighbours = [(pixel[0]+1, pixel[1]), (pixel[0]-1, pixel[1]),
                (pixel[0], pixel[1]+1), (pixel[0], pixel[1]-1)]
      for neighbour in neighbours:
        if 0 <= neighbour[0] < width and 0 <= neighbour[1] < height:
          nb.append(neighbour)
      return nb

    def flood_fill(start_pixel):
      to_search = {start_pixel}
      cell = set()
      searched = set()
      start_color = pixlab_map[start_pixel]
      while to_search:
        pixel = to_search.pop()
        if d(start_color, pixlab_map[pixel]) < self.FLOOD_FILL_TOLERANCE:
          cell.add(pixel)
          unplaced_pixels.remove(pixel)
          for n in self.neighbours(pixel):
            if n in unplaced_pixels and n not in cell and n not in searched:
              to_search.add(n)
        else:
          searched.add(pixel)
      return cell

    # These two maps are inverses, pixel/s <-> number of cell containing pixel
    cell_sets = {}
    pixcell_map = {}
    unplaced_pixels = {(i, j) for i in range(width) for j in range(height)}

    while unplaced_pixels:
      start_pixel = unplaced_pixels.pop()
      unplaced_pixels.add(start_pixel)
      cell = flood_fill(start_pixel)
      cellnum = len(cell_sets)
      cell_sets[cellnum] = cell
      for pixel in cell:
        pixcell_map[pixel] = cellnum

    self.state.set("Stage 2: Flood fill partitioning complete, %d cells" % len(cell_sets))
    self.master.update()
    """
    Stage 3: Merge cells with less than a specified threshold amount of pixels to reduce the number of cells
        +Get rid of noise
    """
    def mean_color(cell, color_map):
      L_sum = 0
      a_sum = 0
      b_sum = 0
      n = len(cell)
      for pixel in cell:
        L, a, b = color_map[pixel]
        L_sum += L
        a_sum += a
        b_sum += b
      return L_sum/n, a_sum/n, b_sum/n

    def remove_small(cell_size):
      if len(cell_sets) <= N:
        return
      small_cells = []
      for cellnum in cell_sets:
        if len(cell_sets[cellnum]) <= cell_size:
          small_cells.append(cellnum)
      for cellnum in small_cells:
        neighbour_cells = []
        for cell in cell_sets[cellnum]:
          for n in self.neighbours(cell):
            neighbour_reg = pixcell_map[n]
            if neighbour_reg != cellnum:
              neighbour_cells.append(neighbour_reg)

        closest_cell = max(neighbour_cells, key=neighbour_cells.count)

        for cell in cell_sets[cellnum]:
          pixcell_map[cell] = closest_cell

        if len(cell_sets[closest_cell]) <= cell_size:
          small_cells.remove(closest_cell)

        cell_sets[closest_cell] |= cell_sets[cellnum]
        del cell_sets[cellnum]
        if len(cell_sets) <= N:
          return

    for cell_size in range(1, self.SMALL_CELL_THRESHOLD):
      remove_small(cell_size)

    if self.OUTPUT_ALL:
      frame_im = Image.new("RGB", im.size)

      for cellnum in cell_sets:
        cell_color = mean_color(cell_sets[cellnum], pixlab_map)
        for pixel in cell_sets[cellnum]:
          frame_im.putpixel(pixel, self.lab2rgb(cell_color))
      
      frame_im.save(self.OUTFILE_STEM + "1.png")
      
    self.state.set("Stage 3: Small cell merging complete, %d cells" % len(cell_sets))
    self.master.update()
    """
    Stage 4: Close color merging
    """
    cell_means = {}#stores colors of each cell

    for cellnum in cell_sets:
      cell_means[cellnum] = mean_color(cell_sets[cellnum], pixlab_map)

    n_graph = defaultdict(set)

    for i in range(width):
      for j in range(height):
        pixel = (i, j)
        cell = pixcell_map[pixel]

        for n in neighbours(pixel):
          neighbour_cell = pixcell_map[n]

          if neighbour_cell != cell:
            n_graph[cell].add(neighbour_cell)
            n_graph[neighbour_cell].add(cell)

    def merge_cells(merge_from, merge_to):
      merge_from_cell = cell_sets[merge_from]

      for pixel in merge_from_cell:
        pixcell_map[pixel] = merge_to

      del cell_sets[merge_from]
      del cell_means[merge_from]

      n_graph[merge_to] |= n_graph[merge_from]
      n_graph[merge_to].remove(merge_to)

      for n in n_graph[merge_from]:
        n_graph[n].remove(merge_from)

        if n != merge_to:
          n_graph[n].add(merge_to)

      del n_graph[merge_from]

      cell_sets[merge_to] |= merge_from_cell
      cell_means[merge_to] = mean_color(cell_sets[merge_to], pixlab_map)

    # Go through the cells from largest to smallest. Keep replenishing the list while we can still merge.
    last_time = time.time()
    to_search = sorted(cell_sets.keys(), key=lambda x:len(cell_sets[x]), reverse=True)
    full_list = True

    while len(cell_sets) > N and to_search:
      if time.time() - last_time > 15:
        last_time = time.time()
        self.state.set("Close color merging... (%d cells remaining)" % len(cell_sets))
        self.master.update()
        
      while to_search:
        cellnum = to_search.pop()
        close_cells = []

        for neighbour_cellnum in n_graph[cellnum]:
          if d(cell_means[cellnum], cell_means[neighbour_cellnum]) < self.CLOSE_CELL_TOLERANCE:
            close_cells.append(neighbour_cellnum)

        if close_cells:
          for neighbour_cellnum in close_cells:
            merge_cells(neighbour_cellnum, cellnum)

            if neighbour_cellnum in to_search:
              to_search.remove(neighbour_cellnum)
          break

      if full_list == True:
        if to_search:
          full_list = False

      else:
        if not to_search:
          to_search = sorted(cell_sets.keys(), key=lambda x:len(cell_sets[x]), reverse=True)
          full_list = True

    if self.OUTPUT_ALL:
      frame_im = Image.new("RGB", im.size)

      for cellnum in cell_sets:
        cell_color = cell_means[cellnum]

        for pixel in cell_sets[cellnum]:
          frame_im.putpixel(pixel, self.lab2rgb(cell_color))

      frame_im.save(self.OUTFILE_STEM + "2.png")

      #self.state = "Saved image %s2.png" % self.OUTFILE_STEM

    self.state.set("Stage 4: Close color merging complete, %d cells" % len(cell_sets))
    self.master.update()

    """
    Stage 5: N-merging - merge until <= N cells
        Want to merge either 1) small cells or 2) cells close in color
    """
    # Weight score between neighbouring cells by 1) size of cell and 2) color difference
    def score(cell1, cell2):
      return d(cell_means[cell1], cell_means[cell2]) * len(cell_sets[cell1])**.5

    n_scores = {}

    for cellnum in cell_sets:
      for n in n_graph[cellnum]:
        n_scores[(n, cellnum)] = score(n, cellnum)
    last_time = time.time()

    while len(cell_sets) > N :
      if time.time() - last_time > 15:
        last_time = time.time()
        self.state.set("N-merging... (%d cells remaining)" % len(cell_sets))
        self.master.update()
        
      merge_from, merge_to = min(n_scores, key=lambda x: n_scores[x])

      for n in n_graph[merge_from]:
        del n_scores[(merge_from, n)]
        del n_scores[(n, merge_from)]

      merge_cells(merge_from, merge_to)

      for n in n_graph[merge_to]:
        n_scores[(n, merge_to)] = score(n, merge_to)
        n_scores[(merge_to, n)] = score(merge_to, n)

    if self.OUTPUT_ALL:
      frame_im = Image.new("RGB", im.size)

      for cellnum in cell_sets:
        cell_color = cell_means[cellnum]

        for pixel in cell_sets[cellnum]:
          frame_im.putpixel(pixel, self.lab2rgb(cell_color))
      frame_im.save(self.OUTFILE_STEM + "3.png")
    del n_graph, n_scores

    self.state.set("Stage 5: N-merging complete, %d cells" % len(cell_sets))
    self.master.update()

    return cell_sets,cell_means,frame_im
    '''Internet code end'''

  def clustering(self):
    cell_means = self.cell_means
    cell_sets = self.cell_sets

    width, height = self.image.size

    self.state.set("Stage 6 : P-clustering")
    self.master.update()
  
    palette = []
    for i in range(width):
      for j in range(height):
        currentColor = self.image.getpixel((i,j))
        if currentColor not in palette:
            palette.append(currentColor)
    self.state.set(str(len(palette)) + "color clusters")
    self.master.update()

    #cluster the colors until proper palette is created
    def cluster(palette = cell_means):
      prevpalette = palette
      for color in cell_means:
        L1,a1,b1 = cell_means[color]
        
        for c in (cell_means):
          L2,a2,b2 = cell_means[c]
          diff = (abs(L1-L2)**2 + abs(a1-a2)**2 + abs(b1-b2)**2)**.5
          if diff <= self.clrrange: ##user changes the color range
          #if 0.95 < average/average2 < 1.15: - another comparison algorithm
            r1,g1,b1 = self.lab2rgb(cell_means[c])
            r2,g2,b2 = self.lab2rgb(cell_means[color])
            avg = ((r1+r2)/2, (g1+g2)/2, (b1+b2)/2)
            cell_means[c] = self.rgb2lab(avg)
            cell_means[color] = self.rgb2lab(avg)
          
      palette = []
      for i in cell_means:
        if cell_means[i] not in palette:
          palette.append(cell_means[i])
      if prevpalette == palette:
        return palette
      return cluster(palette)

    palette = cluster()
    self.state.set(str(len(palette)) + "colors: clustered image...")
    self.master.update()

    self.image.save(self.OUTFILE_STEM + "_clustered.png")

    self.cell_sets = cell_sets
    self.cell_means = cell_means
    return palette
  
  def findCenters(self):
    def choosecenter(pixels,xs,ys, n, prevpixels = []):
      if n == 0:
        x = len(pixels)
        p = pixels[x//2]
   
      else:
        p = random.choice(pixels)
        if len(pixels) == 1:
          return p
      if p not in pixels:
        prevpixels.append(p)
        return choosecenter(pixels,xs,ys,1,prevpixels)
      if p not in prevpixels:
        neighbours = [(p[0]+1, p[1]), (p[0]-1, p[1]),
                (p[0], p[1]+1), (p[0], p[1]-1)]
        for neighbour in neighbours:
          if neighbour not in pixels:
            pixels.remove(p)
            prevpixels.append(p)
            return choosecenter(pixels,xs,ys,1,prevpixels)
      return (p[0]-3,p[1]-5)

    self.state.set("Stage 7: Identifying the cell centroids")
    self.master.update()
    cell_centers = {}
    cell_sets = self.cell_sets
    cell_means = self.cell_means
  
    for cell in cell_sets:
      pixels = list(cell_sets[cell])
      color = cell_means[cell]
      colorindex = str(self.palette.index(color)) 
        
      n = len(pixels)
      if n == 1 or n == 2:
        centpixel = pixels[0]
      if 3 <= n <= 7:
        centpixel = pixels[3]
      elif n >= 8: 
        xs,ys = [],[]
        for p in pixels:
          if p[0] not in xs:
            xs.append(p[0])
          if p[1] not in ys:
            ys.append(p[1])
        xs, ys = sorted(xs), sorted(ys)
        centpixel = choosecenter(pixels, xs, ys, 0)
        cell_centers[centpixel] = colorindex
    return cell_centers
  
  def outline(self):
    width, height = self.image.size
    previousColor = ()
    outline = []
    rgb = self.image.convert('RGB')
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
      
    outimg = Image.new(self.image.mode,self.image.size)

    for y in range(height):
      for x in range(width):
          outimg.putpixel((x,y),(255,255,255))
    for i in outline:
      outimg.putpixel(i, (0, 0, 0))
    outimg = ImageEnhance.Sharpness(outimg).enhance(1.7)
    self.state.set("Stage 8: Image outlined")
    self.master.update()
    return outimg

  def placeNumbers(self):
    for center in self.cell_centers:
      centext = ImageDraw.Draw(self.outimage)
      font = ImageFont.truetype("calibri.ttf", 11)
      centext.text(center, self.cell_centers[center],font = font, fill = "black")

  def createHexPalette(self):
    #rgbtohex converter
    def rgbtohex(r,g,b):
      r,g,b = hex(r)[2:], hex(g)[2:], hex(b)[2:]
      if len(r) != 2:
        r = "0" + r
      if len(g) != 2:
        g = "0" + g
      if len(b) != 2:
        b = "0" + b
      return "#%s%s%s"%(r,g,b)

    hexpalette = []
    for i in range(len(self.palette)):
      r,g,b = self.lab2rgb(self.palette[i])
      color = rgbtohex(r,g,b)
      hexpalette.append(color)
    self.palette = hexpalette
      
if __name__ == '__main__':
  pass