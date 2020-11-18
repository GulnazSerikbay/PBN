from tkinter import *
from tkinter import ttk,colorchooser,filedialog
from PIL import Image
print(hex(0))
class paint:
    def __init__(self):
        self.penwidth = 10
        self.bgcolor = "white"
        self.txtcolor = "black"
        self.pencolor = "black"
        
        x,y = 0,0
        def locate_xy(event):
            global x,y
            x,y = event.x,event.y
        def addLine(event,color = "black"):
            global x,y
            print(x,y,event.x,event.y)
            canvas.create_line((x,y,event.x,event.y), fill = self.pencolor)
            x,y = event.x,event.y
        def showColor(color):
            self.pencolor = color
        def createCanvas():
            canvas.delete('all')
            palette()
        def palette(): 
            palette = ["black","brown4", "pink2", "violet"]
            j =0
            for i in palette:
                id = canvas.create_rectangle((10,10+j,30,30+j),fill = "%s"%i)
                j += 30
                canvas.tag_bind(id,"<Button-1>",lambda x: showColor(i))

        self.wnd = Tk()
        self.wnd.title("Coloring page")
        self.wnd.state('zoomed')
        self.wnd.rowconfigure(0,weight = 1)
        self.wnd.columnconfigure(0,weight = 1)
        #controls = Frame(wnd, padx = 5, pady = 5)
        #Label(controls, text = "Pen Width: ", font = 16).grid(row = 0,column = 0)
        #slider = ttk.Scale(wnd, from_ = 5, to = 100,command = changeWidth, orient = HORIZONTAL)
        #controls.grid(row = 0, column = 0)
        self.modebtn = Button(self.wnd, text = "Dark mode", command = self.changemode)
        self.modebtn.pack()
        menu = Menu(self.wnd)
        self.wnd.config(menu = menu)
        minimenu = Menu(menu, tearoff = 0)

        menu.add_cascade(label = "File", menu = minimenu)
        minimenu.add_command(label = "New Canvas", command = createCanvas)


        canvas = Canvas(self.wnd, width = 500,height = 500, bg = "white")
        canvas.pack()

        canvas.bind('<Button-1>',locate_xy)
        canvas.bind('<B1-Motion>',addLine)
        palette()
        
        

        

        self.wnd.geometry("800x800")
        self.wnd.mainloop()
    def changemode(self):
        if self.wnd.bg == "white":
            self.wnd.config(bg = "black", fg = "white")
            self.modbtn.config(text = "Bright mode")
        else: 
            self.wnd.config(bg = "white", fg = "black")
            self.modbtn.config(text = "Dark mode")
    '''def changeWidth(self,e):
        self.penwidth = e'''
paint = paint()