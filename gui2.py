from tkinter import *
from tkinter import ttk,colorchooser,filedialog, messagebox
from PIL import *
from PIL import Image, ImageTk, ImageGrab
import gui
import processing

#Painting interface
class Paint:
    def __init__(self,master,user = None,image = None, palette = ["black","brown4", "pink2", "violet", 'blue', 'pink4', 'grey','red']):
        self.master = master
        self.user = user
        self.image = image
        self.palette = palette
        self.master.title("E-Paint by Numbers")
        self.master.geometry("800x620")
        self.master.configure(bg = "violet")
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
        #print(self.x,self.y,event.x,event.y)
        if self.x and self.y:
            self.penwidth = self.slider.get()
            self.c.create_oval(self.x-self.penwidth,self.y-self.penwidth,event.x+self.penwidth,event.y+self.penwidth, fill = self.pencolor, outline = self.pencolor)
            #self.c.create_line(self.x, self.y, event.x,event.y, fill = self.pencolor, smooth = True, capstyle = ROUND)
            self.x,self.y = event.x,event.y

    def reset(self,event):
        self.x = None
        self.y = None

    def createWidgets(self):
        #self.control = Frame(self.master,padx = 5,pady = 5)

        welcome = Label(self.master,text = "Welcome, %s!"%self.user, font = ("Verdana", 24), fg = "#883858")
        welcome.pack()

        self.colors = LabelFrame(self.master, text = "Palette", font = ("Verdana", 10), bd = 5, bg = "white")
        self.colors.place(x = 705, y = 50, width = 100, height = 260)
        self.createPalette()

        self.inpbtn = Button(self.master, text = "Input Image", font = ("Verdana", 10), bg = "white", relief = RIDGE, width = 8, command = self.inputImage)
        self.inpbtn.place(x = 705, y = 325, width = 100)

        self.eraser = Button(self.master, text = "Eraser", font = ("Verdana", 10), bg = "white", command = self.erase, width = 8, relief = RIDGE)
        self.eraser.place(x = 705, y = 355,width = 100)

        self.save = Button(self.master, text = "Save image", font = ('Verdana', 10), bg = "white", command = self.saveImage, width = 8, relief = RIDGE)
        self.save.place(x = 705, y = 385,width = 100)

        self.widthlabel = LabelFrame(self.master, text = "Pen Width", font = ('Verdana', 10, "bold"), bd = 5, bg = "white", relief = RIDGE)
        self.widthlabel.place(x = 705, y = 415, height = 150, width = 100)

        self.slider = ttk.Scale(self.widthlabel, from_= 1, to = 18, orient = VERTICAL, length = 120)
        self.slider.set(self.penwidth)
        self.slider.grid(row = 0, column = 1, padx = 30)
        
        self.c = Canvas(self.master, width = 700, height= 520, bg = self.bgcolor, relief = GROOVE)
        self.c.place(x = 0, y = 50)
        
        if self.image != None:
            print(self.image)
            self.image = Image.open(self.image)
            self.c.image = ImageTk.PhotoImage(self.image)
            self.c.create_image(0,0, image = self.c.image, anchor = "nw")

        #self.master.filename = filedialog.askopenfilename(initial = "/images", title = "Select a file", filetypes = (('jpg files',"*.jpg"),('png files',"*.png")))
        
        menu = Menu(self.master)
        self.master.config(menu = menu)
        filemenu = Menu(menu)
        clrmenu = Menu(menu)
        menu.add_cascade(label = 'Colors', menu = clrmenu)
        clrmenu.add_command(label = "Brush color", command = self.setPencolor)
        clrmenu.add_command(label = "Background color", command = self.setbg)
        optionmenu = Menu(menu)
        menu.add_cascade(label = 'Options', menu = optionmenu)
        optionmenu.add_command(label = "Clear Canvas", command = self.clearCanvas)
        optionmenu.add_command(label = "Exit", command = self.exit)

    def clearCanvas(self):
        self.c.delete('all')
        self.createPalette()
        self.c.create_image(0,0, image = self.c.image, anchor = "nw")

    def setbg(self):
        self.bgcolor = colorchooser.askcolor(color = self.bgcolor)[1]
        self.c['bg'] = self.bgcolor
        self.erasercolor = self.bgcolor

    def erase(self):
        self.pencolor = self.erasercolor
    
    def setPencolor(self):
        self.pencolor = colorchooser.askcolor(color = self.pencolor)[1]
    
    def inputImage(self):

        img = filedialog.askopenfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images", title = "Select a file", filetypes = (('jpg files',"*.jpg"),('png files',"*.png")))
        
        img = Image.open(img)
        self.c.image = ImageTk.PhotoImage(img)
        self.c.create_image(0,0, image = self.c.image, anchor = "nw")

    def saveImage(self):
        self.imagename = filedialog.asksaveasfilename(confirmoverwrite = False,defaultextension = '.png')
        x = self.master.winfo_rootx() + self.c.winfo_x()
        y = self.master.winfo_rooty() + self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(self.imagename)
        messagebox.showinfo("Save success","Image saved as " + str(self.imagename))

    def exit(self):
        response = messagebox.askyesno("Save the file?","Do you want to save the image?")
        if response == 1:
            self.saveImage()
        else:
            messagebox.showinfo("Thank YOU!","Thank you for using the app!")
        self.master.destroy()

    def addNewcolor(self):
        self.setPencolor()
        self.usedcolor.config(bg = self.pencolor, command = lambda col = self.pencolor:self.showColor)

    def showColor(self,color):
        self.pencolor = color

    def createPalette(self):
        Button(self.colors, bg = "white", text = "+", relief = RIDGE, width = 2, command = self.addNewcolor).grid(row = 0, column = 0)
        self.usedcolor = Button(self.colors, bg = "black", relief = RIDGE, width = 2, command = lambda: self.showColor("black"))
        self.usedcolor.grid(row = 1,column = 0)
        if self.palette != None:
            j,k = 2,0
            for i in self.palette:
                Button(self.colors,bg = i, fg = "white", text = self.palette.index(i), relief = RIDGE,width = 2, command = lambda col = i:self.showColor(col)).grid(row = j, column = k)
                #id = self.create_rectangle((10,10+j,30,30+j),fill = "%s"%i)
                j += 1
                if j == 9:
                   j = 0
                   k += 1


        '''self.wnd = Tk()
        self.wnd.title("Coloring page")
        self.wnd.state('zoomed')'''
        
        #controls = Frame(wnd, padx = 5, pady = 5)
        #Label(controls, text = "Pen Width: ", font = 16).grid(row = 0,column = 0)
        #slider = ttk.Scale(wnd, from_ = 5, to = 100,command = changeWidth, orient = HORIZONTAL)
        #controls.grid(row = 0, column = 0)
        
        """ menu = Menu(self.wnd)
        self.wnd.config(menu = menu)
        minimenu = Menu(menu, tearoff = 0)

        menu.add_cascade(label = "File", menu = minimenu)
        minimenu.add_command(label = "New Canvas", command = createCanvas)

        canvas = Canvas(self.wnd, width = 500,height = 500, bg = "white")
        canvas.pack()

        canvas.bind('<Button-1>',self.locate_xy)
        canvas.bind('<B1-Motion>',self.addLine) """
#PBN Genarator interface
class PBN:
    def __init__(self, master,user = None):
        self.master = master
        self.user = user
        
        self.master.title("PBN Generator")
        self.master.geometry("800x600")
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)
        self.createWidgetsPBN()

    def createWidgetsPBN(self):
        #img = ImageTk.PhotoImage(self.image)

        welcome = Label(self.master,text = "Welcome, %s!"%self.user, font = ("Verdana", 24), fg = "#883858")
        welcome.pack()

        font = ("Verdana", 10)
        self.exit = Button(self.master, text = "Back to Home", font = font, command = self.exit)
        self.exit.place(x = 0, y = 50,width = 100,height = 40)
        
        btn = Button(self.master, text = "Pick an image", font = font, command = self.pickFile)
        btn.place(x = 0, y = 95,width = 100,height = 40)

        #Label Frame for processing options

        self.colorrange = IntVar()
        self.colors = LabelFrame(self.master, text = "Choose the color Limit",font = font)
        self.colors.place(x = 0, y = 140, width = 100, height = 110)
        Radiobutton(self.colors, text = "Less colors", variable = self.colorrange, value = 10).grid(row = 0, column = 0)
        Radiobutton(self.colors, text = "Medium", variable = self.colorrange, value = 16).grid(row = 1, column = 0)
        Radiobutton(self.colors, text = "More colors", variable = self.colorrange, value = 20).grid(row = 2, column = 0)

        self.startbtn = Button(self.master, text = "Start PBNing", state = DISABLED, font = font, command = self.startProcessing)
        self.startbtn.place(x = 0, y = 255, width = 100, height = 30)
        
        
        self.paint = Button(self.master, text = "Paint virtually", state = DISABLED, command = self.goPaint)
        self.paint.place(x = 0, y = 290, width = 100, height = 30)

        self.download = Button(self.master, text = "Download outlined", state = DISABLED, command = self.downloadoutlineImage)
        self.download.place(x = 0, y = 325, width = 100, height = 30)

        self.download2 = Button(self.master, text = "Download in color", state = DISABLED, command = self.downloadoutlineImage)
        self.download2.place(x = 0, y = 360, width = 100, height = 30)

        self.c = Canvas(self.master, bg='white')
        self.c.place(x = 110, y = 50, width = 700, height = 500)

        Label(self.master, text = "Image processing status:", font = ("Verdana", 14)).place(x = 110, y = 570)
        self.state = Label(self.master, text = "", font = ("Verdana", 14))
        self.state.place(x = 350, y = 570)

    def exit(self):
        self.master.destroy()
        wnd = Tk()
        gui.Main(wnd)
        wnd.mainloop()
    
    def goPaint(self):
        self.master.destroy()
        wnd = Tk()
        paint = Paint(wnd,self.user, self.outimagename, self.palette)

    def downloadcolorImage(self):
        self.imagename = filedialog.asksaveasfilename(confirmoverwrite = False,defaultextension = '.png')
        self.image1.save(self.imagename)
        messagebox.showinfo("Save colored success","Colored PBN saved as " + str(self.imagename))

    def downloadoutlineImage(self):
        self.outimagename = filedialog.asksaveasfilename(confirmoverwrite = False,defaultextension = '.png')
        self.outimage1.save(self.outimagename)
        messagebox.showinfo("Save PBN success","PBN saved as " + str(self.outimagename))
        self.paint.config(state = NORMAL)

    def downloadPalette(self):
        self.downname = filedialog.asksaveasfilename(confirmoverwrite = False,defaultextension = '.png')
        x = self.master.winfo_rootx() + self.pCanvas.winfo_x()
        y = self.master.winfo_rooty() + self.pCanvas.winfo_y()
        x1 = x + self.pCanvas.winfo_width()
        y1 = y + self.pCanvas.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(self.downname)
        messagebox.showinfo("Save palette success","Palette saved as " + str(self.downname))


    def startProcessing(self):
        self.state.config(text = "Image started")

        ImgProcessing = processing.Processing(self.state, self.file, 70, self.colorrange.get())
        #self.imgfile = ImgProcessing.OUTFILE_STEM + ".png"
        #self.image = Image.open(self.imgfile)
        #self.image = ImageTk.PhotoImage(self.image)

        self.image1 = ImgProcessing.image
        self.outimage1 = ImgProcessing.outimage
        self.outimage2 = ImageTk.PhotoImage(ImgProcessing.outimage)
        self.c.image = self.c.create_image(0,0, image = self.outimage2, anchor = "nw")
        
        self.download.config(state = NORMAL)
        self.download2.config(state = NORMAL)
        self.palette = ImgProcessing.palette
        
        self.pCanvas = Canvas(self.master)
        self.pCanvas.place(x = 0, y = 395, width = 100, height = 180)

        self.createPalette()

        self.download3 = Button(self.master, text = "Download palette", font = ("Verdana",10), command = self.downloadPalette)
        self.download3.place(x = 0, y = 580, width = 100, height = 30)

    def createPalette(self):
        if self.palette != None:
            if len(self.palette) <= 10:
                padx = 10
            else:
                padx = 0
            j,k = 0,0
            for i in self.palette:
                Button(self.pCanvas,bg = i, fg = "black", text = self.palette.index(i), relief = RIDGE, width = 3).grid(padx = padx, row = j, column = k)
                #id = self.create_rectangle((10,10+j,30,30+j),fill = "%s"%i)
                j += 1
                if j == 7:
                   j = 0
                   k += 1
                    

    def pickFile(self):
        #JPG recommended
        self.file = filedialog.askopenfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images", title = "Select a file", filetypes = (('jpg files',"*.jpg"),('png files',"*.png")))
        self.image = Image.open(self.file)
        self.image = ImageTk.PhotoImage(self.image)
        self.c.image = self.c.create_image(0,0, image = self.image, anchor = "nw")

        self.startbtn.config(state = NORMAL)
    
if __name__ == '__main__':
    wnd = Tk()
    #paint = Paint(wnd)
    pbn = PBN(wnd)
    wnd.mainloop()
        

'''
if __name__ == '__main__':
    wnd = Tk()
    fmain = Frame(wnd)
    fPBN = Frame(wnd)
    fPaint = Frame(wnd)
    main = gui.Main(fmain)
    #Paint(fPaint)
    #PBN(fPBN)
    '''
    