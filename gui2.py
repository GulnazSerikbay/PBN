from tkinter import *
from tkinter import ttk,colorchooser,filedialog
from PIL import Image

class paint:
    def __init__(self):
        self.penwidth = 10
        self.bgcolor = "white"
        self.txtcolor = "black"
        
        def changemode():
            wnd.config(bg = "black")
            modbtn.config(text = "Bright mode")
        def changeWidth(self,e):
            self.penwidth = e

        wnd = Tk()
        wnd.title("Coloring page")
        wnd.state('zoomed')
        wnd.rowconfigure(0,weight = 1)
        wnd.columnconfigure(0,weight = 1)
        controls = Frame(wnd, padx = 5, pady = 5)
        Label(controls, text = "Pen Width: ", font = 16).grid(row = 0,column = 0)
        slider = ttk.Scale(wnd, from_ = 5, to = 100,command = changeWidth, orient = HORIZONTAL)
        controls.grid(row = 0, column = 0)

        modebtn = Button(wnd, text = "Dark mode", command = changemode)
        modebtn.grid(row = 0,column = 1)
        canvas = Canvas(wnd, width = 500,height = 500, bg = 'white')
        canvas.grid(row=0,column=0)

        canvas.create_line(20,20,60,20)

        wnd.geometry("800x800")
        wnd.mainloop()
        
paint = paint()