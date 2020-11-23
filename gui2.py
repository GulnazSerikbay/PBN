from tkinter import *
from tkinter import ttk,colorchooser,filedialog
from PIL import Image, ImageTk
import gui
import processing

#Painting interface
class Paint:
    def __init__(self,master):
        self.master = master
        self.master.title("E-Paint by Numbers")
        self.master.geometry("800x800")
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)
        self.penwidth = 10
        self.bgcolor = "white"
        self.txtcolor = "black"
        self.pencolor = "black"
        self.x = None
        self.y = None
        self.createWidgets()
        self.c.bind('<Button-1>',self.locate_xy)
        self.c.bind('<B1-Motion>',self.paint)
        self.c.bind('<ButtonRelease-1>',self.reset)
        
    def locate_xy(self,event):
        self.x,self.y = event.x,event.y

    def paint(self,event):
        print(self.x,self.y,event.x,event.y)
        if self.x and self.y:
            self.c.create_line(self.x, self.y, event.x,event.y, fill = self.pencolor, smooth = True, capstyle = ROUND)
            self.x,self.y = event.x,event.y

    def reset(self,event):
        self.x = None
        self.y = None
    

    def createWidgets(self):
        self.control = Frame(self.master,padx = 5,pady = 5)
        Label(self.control, text = "Pen Width", font = ('arial 18')).grid(row = 0, column = 0)

        self.slider = ttk.Scale(self.control, from_= 10, to = 100, command = self.setpenwidth, orient = HORIZONTAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row = 0, column = 0, ipadx = 30)
        #self.slider.pack(slide = LEFT)
            
        self.c = Canvas(self.master, width = 500, height= 500, bg = self.bgcolor)
        self.c.pack(fill = BOTH, expand = False)
            
        self.modebtn = Button(self.master, text = "Dark mode", command = self.changemode)
        self.modebtn.pack(fill = BOTH)

        self.inpbtn = Button(self.master, text = "Input Image", command = self.inputImage)
        self.inpbtn.pack()

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
        optionmenu.add_command(label = "Clear Canvas", command = self.createCanvas)
        optionmenu.add_command(label = "Exit", command = self.exit)
        self.palette()

    def createCanvas(self):
        self.c.delete('all')
        self.palette()

    def setpenwidth(self,event):
        self.penwidth = event
    
    def setbg(self):
        self.bgcolor = colorchooser.askcolor(color = self.bgcolor)[1]
        self.c['bg'] = self.bgcolor
    
    def setPencolor(self):
        self.pencolor = colorchooser.askcolor(color = self.pencolor)[1]
    
    def inputImage(self):

        img = filedialog.askopenfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images", title = "Select a file", filetypes = (('jpg files',"*.jpg"),('png files',"*.png")))
        self.c.image = PhotoImage(img)
        self.c.create_image(0,0, image = self.c.image, anchor = "nw")

    def exit(self):
        #msg box
        #if yes: save the file,
        #if no:
        self.master.destroy()

    def palette(self):
        def showColor(color):
            self.pencolor = color

        palette = ["black","brown4", "pink2", "violet"]
        j =0
        for i in palette:
            id = self.c.create_rectangle((10,10+j,30,30+j),fill = "%s"%i)
            j += 30
            self.c.tag_bind(id,"<Button-1>",lambda x: showColor(i))

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
    def __init__(self, master,image = None):
        self.master = master
        self.file = image
        self.image = None
        self.master.title("PBN Generator")
        self.master.geometry("800x800")
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)
        self.createWidgetsPBN()

    def createWidgetsPBN(self):
        #img = ImageTk.PhotoImage(self.image)

        self.c = Canvas(self.master, width=400, height=400, bg='white')
        self.c.pack()

        btn = Button(self.master, text = "Pick an image", command = self.pickFile)
        btn.pack()
        
        self.startbtn = Button(self.master, text = "Start PBNing", state = DISABLED, command = self.startProcessing)

    def startProcessing(self):
        ImgProcessing = processing.Processing(self.master, self.file, 70)

        for i in range(len(processing.ImgProcessing.palette)):
            color = ImgProcessing.palette[i]
            self.c.create_rectangle((i, i+30, 20, i+30), fill = color)

    def pickFile(self):
        #JPG recommended
        file = filedialog.askopenfilename(initialdir = "/Users/Gulnaz/Documents/GitHub/PBN/images", title = "Select a file", filetypes = (('jpg files',"*.jpg"),('png files',"*.png")))
        self.file = file
        self.image = PhotoImage(self.file)
        self.c.create_image(0,0, image = self.image, anchor = "nw")

        self.startbtn.config(state = NORMAL)
        

if __name__ == '__main__':
    wnd = Tk()

    pbn = PBN(wnd,"images/hi.jpg")
    
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
    