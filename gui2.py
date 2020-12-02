#Name: Gulnaz Serikbay
''' Description: Contains Tkinter Window classes Paint and PBN'''

from tkinter import *
from tkinter import ttk,colorchooser,filedialog, messagebox
from tkinter import simpledialog
from PIL import *
from PIL import Image, ImageTk, ImageGrab
import main
import processing

""" tk_ToolTip_class101.py
gives a Tkinter widget a tooltip as the mouse is above the widget
tested with Python27 and Python34  by  vegaseat  09sep2014
www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

Modified to include a delay time by Victor Zaccardo, 25mar16
"""
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

#Painting interface
class Paint:
    def __init__(self,master,user = None,image = None, palette = ["black","brown4", "pink2", "violet", 'blue', 'pink4', 'grey','red']):
        self.master = master
        self.user = user
        self.image = image
        self.palette = palette
        self.master.title("E-Paint by Numbers")
        self.master.geometry("830x620")
        self.master.configure()
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)
        self.penwidth = 2
        self.bgcolor = "white"
        self.txtcolor = "black"
        self.pencolor = "black"
        self.erasercolor = "white"
        self.x = None
        self.y = None
        self.createWidgets()
        self.c.bind('<Button-1>',self.locate_xy)
        self.c.bind('<B1-Motion>',self.paint)
        self.c.bind('<ButtonRelease-1>',self.reset)
        self.master.mainloop()
    
    def locate_xy(self,event):
        self.x,self.y = event.x,event.y

    def paint(self,event):
        if self.x and self.y:
            self.penwidth = self.slider.get()
            self.c.create_oval(self.x-self.penwidth,self.y-self.penwidth,event.x+self.penwidth,event.y+self.penwidth, fill = self.pencolor, outline = self.pencolor)
            self.x,self.y = event.x,event.y
            if self.currentpen:
                self.c.delete(self.currentpen)
                self.currentpen = self.c.create_oval(640,30,640+2*self.penwidth, 30+2*self.penwidth, fill = self.pencolor)
                self.clabel = Label(self.c, text = "Current Brush",font = ("Verdana", 10), bg = "white")

    def reset(self,event):
        self.x = None
        self.y = None

    def createWidgets(self):
        self.welcome = Label(self.master,text = "Paint your PBN digitally!", font = ("Verdana", 24), fg = "#883858")
        self.welcome.pack()

        self.colors = LabelFrame(self.master, text = "Palette", font = ("Verdana", 10), bd = 5, bg = "white")
        self.colors.place(x = 712, y = 50, width = 115, height = 260)
        self.createPalette()
        tt0 = CreateToolTip(self.colors, "Use the numbered colors to paint the corresponding numbered regions")

        self.tools = LabelFrame(self.master, text = "Tools", font = ("Verdana", 10), bd = 5, bg = "white")
        self.tools.place(x = 712, y = 315, width = 115, height = 90)
        
        #image = PhotoImage(file = "image.png")
        self.inpbtn = Button(self.tools, font = ("Verdana", 10), text = "Image", compound = LEFT, bg = "white", relief = RIDGE, command = self.inputImage)
        self.inpbtn.grid(row = 0)
        
        tt1 = CreateToolTip(self.inpbtn, "Import new image")
        
        
        self.eraser = Button(self.tools, text = "Eraser", font = ("Verdana", 10), bg = "white",
                            command = self.erase, width = 5, relief = RIDGE)
        self.eraser.grid(row = 1, column = 0)
        
        self.save = Button(self.tools, text = "Save", font = ('Verdana', 10), bg = "white",  command = self.saveImage, width = 5, relief = RIDGE)
        self.save.grid(row = 1, column = 1)
        tt2 = CreateToolTip(self.save, "Save your painting")

        #self.text = Button(self.tools, text = "T", font = ('Verdana', 10), bg = "white", command = self.addText, width = 5, relief = RIDGE)
        #self.text.grid(row = 1, column = 1)

        self.widthlabel = LabelFrame(self.master, text = "Pen Width", font = ('Verdana', 9, "bold"), bd = 5, bg = "white", relief = RIDGE)
        self.widthlabel.place(x = 712, y = 415, height = 150, width = 115)
        tt3 = CreateToolTip(self.widthlabel, "Change the penwidth/eraser width")

        self.slider = ttk.Scale(self.widthlabel, from_= 1, to = 18, orient = VERTICAL, length = 120)
        self.slider.set(self.penwidth)
        self.slider.grid(row = 0, column = 1, padx = 30)
        self.slider.bind("<Button-1>", self.setpenwidth)
        
        self.c = Canvas(self.master, width = 700, height= 520, bg = self.bgcolor, relief = GROOVE)
        self.c.place(x = 3, y = 50)
        #current penwidth,pencolor
        self.currentpen = self.c.create_oval(640,30,640+2*self.penwidth, 30+2*self.penwidth, fill = self.pencolor)
        self.clabel = Label(self.c, text = "Current Brush",font = ("Verdana", 10), bg = "white")
        self.clabel.place(x = 610,y = 4)
        tt5 = CreateToolTip(self.clabel, "This is how your current pen looks like")
        if self.image:
            self.image = Image.open(self.image)
            self.image = ImageTk.PhotoImage(self.image)
            self.c.image = self.c.create_image(0,0, image = self.image, anchor = "nw")   
        self.saveimage = False     
        
        menu = Menu(self.master)
        self.master.config(menu = menu)
        paintmenu = Menu(menu)
        menu.add_cascade(label = 'Edit', menu = paintmenu)
        paintmenu.add_command(label = "Clear Canvas", command = self.clearCanvas)
        paintmenu.add_command(label = "Set Brush color", command = self.setPencolor)
        paintmenu.add_command(label = "Set Background color", command = self.setbg)
        #paintmenu.add_command(label = "Insert text", command = self.addText)
        
        filemenu = Menu(menu)
        menu.add_cascade(label = 'File', menu = filemenu)
        filemenu.add_command(label = "Save image", command = self.saveImage)
        filemenu.add_command(label = "Exit", command = self.exit)
        filemenu.add_command(label = "Back to Home", command = self.gohome)
    
    def setpenwidth(self,event):
        self.penwidth = self.slider.get()
        self.c.delete(self.currentpen)
        self.currentpen = self.c.create_oval(640,30,640+2*self.penwidth, 30+2*self.penwidth, fill = self.pencolor)

    def clearCanvas(self):
        self.c.delete('all')
        self.createPalette()
        if self.image:
            self.c.image = self.c.create_image(0,0, image = self.image, anchor = "nw")
        self.currentpen = self.c.create_oval(640,30,640+2*self.penwidth, 30+2*self.penwidth, fill = self.pencolor)
        self.clabel = Label(self.c, text = "Current Brush",font = ("Verdana", 10), bg = "white")

    def setbg(self):
        self.bgcolor = colorchooser.askcolor(color = self.bgcolor)[1]
        self.master.config(bg = self.bgcolor)
        self.welcome.config(bg = self.bgcolor)
             
    def erase(self):
        self.pencolor = self.erasercolor
        self.widthlabel.config(text = "Eraser Width")
    
    def setPencolor(self):
        self.pencolor = colorchooser.askcolor(color = self.pencolor)[1]
        self.widthlabel.config(text = "Pen Width")
        self.c.delete(self.currentpen)
        self.penwidth = self.slider.get()
        self.currentpen = self.c.create_oval(640,30,640+2*self.penwidth, 30+2*self.penwidth, fill = self.pencolor)
    
    def inputImage(self):
        img = filedialog.askopenfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images/outputs", title = "Select a file", filetypes = [('png files',".png")])
        cheight = self.c.winfo_height()
        if self.image:
            self.c.delete(self.c.image)
        if img:
            self.image = Image.open(img)
            width, height = self.image.size
            if not (height == cheight):
                self.image = self.image.resize((width*cheight//height,cheight))
            self.image = ImageTk.PhotoImage(self.image)
            self.c.image = self.c.create_image(0,0, image = self.image, anchor = "nw")

    def saveImage(self):
        imagename = filedialog.asksaveasfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images/outputs",
                                                    confirmoverwrite = False,defaultextension = '.png')
        self.c.delete(self.currentpen)
        self.clabel.destroy()
        if imagename:
            x = self.master.winfo_rootx() + self.c.winfo_x()
            y = self.master.winfo_rooty() + self.c.winfo_y()
            x1 = x + self.c.winfo_width()
            y1 = y + self.c.winfo_height()
            ImageGrab.grab().crop((x,y,x1,y1)).save(imagename)
            messagebox.showinfo("Save success","Image saved as " + str(imagename))
            self.saveimage = True
        self.clabel = Label(self.c, text = "Current Brush",font = ("Verdana", 10), bg = "white")
        self.currentpen = self.c.create_oval(640,30,640+2*self.penwidth, 30+2*self.penwidth, fill = self.pencolor)

    def gohome(self):
        if not self.saveimage:
            response = messagebox.askyesno("Save the file?","Do you want to save the image?")
            if response == 1:
                self.saveImage()
        self.master.destroy()
        wnd = Tk()
        main.Main(wnd, self.user)
        wnd.mainloop()

    def exit(self):
        if not self.saveimage:
            response = messagebox.askyesno("Save the file?","Do you want to save the image?")
            if response == 1:
                self.saveImage()
        messagebox.showinfo("Thank YOU!","Thank you for using the app!")
        self.master.destroy()

    def addNewcolor(self):
        self.setPencolor()
        self.usedcolor.config(bg = self.pencolor, command = lambda col = self.pencolor:self.showColor)

    def showColor(self,color):
        self.pencolor = color
        self.c.delete(self.currentpen)
        self.penwidth = self.slider.get()
        self.currentpen = self.c.create_oval(640,30,640+2*self.penwidth, 30+2*self.penwidth, fill = self.pencolor)

    def createPalette(self):
        addbtn = Button(self.colors, bg = "white", text = "+", relief = RIDGE, width = 2, command = self.addNewcolor)
        addbtn.grid(row = 0, column = 0)
        tt4 = CreateToolTip(addbtn, "Add new color to palette")
        self.usedcolor = Button(self.colors, bg = "black", relief = RIDGE, width = 2, command = lambda: self.showColor("black"))
        self.usedcolor.grid(row = 1,column = 0)
        if self.palette != None:
            j,k = 2,0
            for i in self.palette:
                Button(self.colors,bg = i, fg = "white", text = self.palette.index(i), relief = RIDGE,width = 2, command = lambda col = i:self.showColor(col)).grid(row = j, column = k)
                j += 1
                if j == 9:
                   j = 0
                   k += 1
      
#PBN Generator interface
class PBN:
    def __init__(self, master,user = None):
        self.master = master
        self.user = user
        self.image = None
        self.N = 15
        self.master.title("PBN Generator")
        self.master.geometry("900x650")
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)
        self.createWidgetsPBN()

    def createWidgetsPBN(self):
        #img = ImageTk.PhotoImage(self.image)

        welcome = Label(self.master,text = "Welcome, %s!"%self.user, font = ("Verdana", 24), fg = "#883858")
        welcome.pack()

        font = ("Verdana", 10)
        self.exit = Button(self.master, text = "Back to Home", font = font, command = self.exit)
        self.exit.place(x = 2, y = 2,width = 100,height = 40)
        tt0 = CreateToolTip(self.exit, "Return to main page")
        
        #Label Frame for processing options

        self.colorrange = IntVar()
        self.colors = LabelFrame(self.master, text = "Color Limit",font = font)
        self.colors.place(x = 2, y = 100, width = 115, height = 145)
        tt1 = CreateToolTip(self.colors, "Choose the range of colors you want")

        Radiobutton(self.colors, text = "More colors", variable = self.colorrange, value = 10).grid(row = 0, column = 0)
        Radiobutton(self.colors, text = "Medium", variable = self.colorrange, value = 16).grid(row = 1, column = 0)
        Radiobutton(self.colors, text = "Less colors", variable = self.colorrange, value = 20).grid(row = 2, column = 0)

        numlabel = Label(self.colors, text = "Details")
        numlabel.grid(row = 3, column = 0)
        tt2 = CreateToolTip(numlabel, "How detailed is your image? Choose on slider")
        
        self.numcells = ttk.Scale(self.colors, from_= 15, to = 80, orient = HORIZONTAL, length = 100)
        self.numcells.set(self.N)
        self.numcells.grid(row = 4, column = 0)

        self.startbtn = Button(self.master, text = "Start PBNing", state = DISABLED, font = font, command = self.startProcessing)
        self.startbtn.place(x = 2, y = 250, width = 110, height = 30)
        tt3 = CreateToolTip(self.startbtn, "Press to start processing your image")

        self.paint = Button(self.master, text = "Paint virtually", state = DISABLED, font = font, command = self.goPaint)
        self.paint.place(x = 2, y = 285, width = 110, height = 30)
        tt4 = CreateToolTip(self.paint, "Go to paint window")

        self.download = Button(self.master, text = "Save outlined", state = DISABLED, font = font, command = self.downloadoutlineImage)
        self.download.place(x = 2, y = 320, width = 110, height = 30)
        tt5 = CreateToolTip(self.download, "Download the outlined PBN image")

        self.download2 = Button(self.master, text = "Save in color", state = DISABLED, font = font, command = self.downloadcolorImage)
        self.download2.place(x = 2, y = 355, width = 110, height = 30)
        tt6 = CreateToolTip(self.download2, "Download the colored PBN image")

        self.c = Canvas(self.master, bg='white')
        self.c.place(x = 115, y = 50, width = 700, height = 540)

        self.pickbtn = Button(self.c, text = "Pick new image", font = font, bg = "#8395A7", command = self.pickFile)
        self.pickbtn.pack(pady = 200)
        tt7 = CreateToolTip(self.pickbtn, "Import new image to process")

        Label(self.master, text = "Image processing status:", font = ("Verdana", 14)).place(x = 115, y = 590)
        self.imagestate = StringVar()
        self.imagestate.set("Image not uploaded")
        self.state = Label(self.master, textvariable = self.imagestate, font = ("Verdana", 14))
        self.state.place(x = 380, y = 590)

    def exit(self):
        self.master.destroy()
        wnd = Tk()
        main.Main(wnd,self.user)
        wnd.mainloop()
    
    def goPaint(self):
        self.master.destroy()
        filename = self.file.split("/")[-1].split(".")[0]
        self.outimagename =  "/Users/Gulnaz/Documents/GitHub/PBN/images/outputs/out" + filename + ".png"
        self.outimage1.save(self.outimagename)
        wnd = Tk()
        paint = Paint(wnd,self.user, self.outimagename, self.palette)
        wnd.mainloop()

    def downloadcolorImage(self):
        imagename = filedialog.asksaveasfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images/outputs", confirmoverwrite = False,defaultextension = '.png')
        if imagename:
            self.image1.save(imagename)
            messagebox.showinfo("Save colored success","Colored PBN saved as " + str(imagename))

    def downloadoutlineImage(self):
        self.outimagename = filedialog.asksaveasfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images/outputs", confirmoverwrite = False,defaultextension = '.png')
        if self.outimagename:
            self.outimage1.save(self.outimagename)
            messagebox.showinfo("Save PBN success","PBN saved as " + str(self.outimagename))

    def downloadPalette(self):
        downname = filedialog.asksaveasfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images/outputs", confirmoverwrite = False,defaultextension = '.png')
        if downname:
            x = self.master.winfo_rootx() + self.pCanvas.winfo_x()
            y = self.master.winfo_rooty() + self.pCanvas.winfo_y()
            x1 = x + self.pCanvas.winfo_width()
            y1 = y + self.pCanvas.winfo_height()
            ImageGrab.grab().crop((x,y,x1,y1)).save(downname)
            messagebox.showinfo("Save palette success","Palette saved as " + str(downname))
    
    def showColored(self):
        self.c.delete("all")
        self.c.image = self.c.create_image(0,0, image = self.image2, anchor = "nw")
        self.showcolored.config(text = "Show outlined image", command = self.showoutlined)
    
    def showoutlined(self):
        self.c.delete("all")
        self.c.image = self.c.create_image(0,0, image = self.outimage2, anchor = "nw")
        self.showcolored.config(text = "Show colored image", command = self.showColored)
    
    def startProcessing(self):
        
        self.N = int(self.numcells.get())
        self.ImgProcessing = processing.Processing(self.master,self.imagestate, self.file, self.N, self.colorrange.get())
        ImgProcessing = self.ImgProcessing

        self.image1 = ImgProcessing.image
        self.image2 = ImageTk.PhotoImage(self.image1)

        self.outimage1 = ImgProcessing.outimage

        self.outimage2 = (ImgProcessing.outimage)
        self.outimage2 = ImageTk.PhotoImage(self.outimage2)
        self.c.delete("all")
        self.c.image = self.c.create_image(0,0, image = self.outimage2, anchor = "nw")
        self.showcolored = Button(self.c, text = "Show colored result", relief = RIDGE, bg = "white", command = self.showColored)
        self.showcolored.place(x = 2, y = 2, height = 30)

        self.paint.config(state = NORMAL)
        self.download.config(state = NORMAL)
        self.download2.config(state = NORMAL)
        self.palette = ImgProcessing.palette
        
        self.pCanvas = Canvas(self.master)
        self.pCanvas.place(x = 2, y = 425, width = 110, height = 180)

        self.createPalette()

        self.download3 = Button(self.master, text = "Save palette", font = ("Verdana",10), command = self.downloadPalette)
        self.download3.place(x = 2, y = 390, width = 110, height = 30)
        tt8 = CreateToolTip(self.download3, "Download the color palette for the processed image")
    
    def createPalette(self):
        if self.palette != None:
            if len(self.palette) <= 10:
                padx = 10
            else:
                padx = 0
            j,k = 0,0
            for i in self.palette:
                Button(self.pCanvas,bg = i, fg = "black", text = self.palette.index(i), relief = RIDGE, width = 3).grid(padx = padx, row = j, column = k)
                j += 1
                if j == 7:
                   j = 0
                   k += 1

    def pickFile(self):
        #JPG recommended
        if self.image:
            self.c.delete("all")
            self.showcolored.destroy()
            self.file = None
        self.file = filedialog.askopenfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images", title = "Select a file", filetypes = (('jpg files',"*.jpg"),('png files',"*.png")))
        if self.file:
            self.image = Image.open(self.file)
            width, height = self.image.size

            self.pickbtn.destroy()
            self.pickbtn = Button(self.master, text = "New image", font = ("Verdana", 10), bg = "#8395A7", command = self.pickFile)
            self.pickbtn.place(x = 2, y = 50, width = 110,height = 40)

            cwidth = self.c.winfo_width()
            cheight = self.c.winfo_height()
            if not (height == cheight):
                self.image = self.image.resize((width*cheight//height,cheight))
                newwidth = self.image.size[0]
                self.c.config(width = newwidth)

            self.image = ImageTk.PhotoImage(self.image)
            self.c.image = self.c.create_image(0,0, image = self.image, anchor = "nw")
            self.imagestate.set("Image uploaded")
            self.startbtn.config(state = NORMAL)
            
if __name__ == '__main__':
    wnd = Tk()
    paint = Paint(wnd)
    #pbn = PBN(wnd)
    wnd.mainloop()
        


    