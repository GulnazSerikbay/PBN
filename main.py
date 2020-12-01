#Name: Gulnaz Serikbay
'''Description: Main user interface that allow to run the program'''
import tkinter
from tkinter import *
import gui2
from processing import *

class Main:
    def __init__(self, master,user = ""):
        self.master = master
        self.name = user
        self.master.title("Welcome to PBN")
        self.master.geometry("800x800")
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)

        self.createWidgets()
    
    def createWidgets(self):
        label1 = Label(self.master, text = "Welcome to PBN world!", font = ("Verdana", 30), fg = "#883858")
        label1.pack(pady = 30)

        label2 = Label(self.master, text = "Your name", font = ("Verdana", 18), fg = "black")
        label2.pack(pady = 10)

        self.input = Entry(self.master, font = ("Verdana", 16))
        self.input.pack(pady = 20,ipady = 10, ipadx = 10)
        if self.name:
            inputtext = StringVar()
            inputtext.set(self.name)
            self.input.config(textvariable = inputtext)

        generatorbtn = Button(self.master, text = "PBN Generator", command = self.goPBN, bg = "#8395A7", fg = "#DAE0E2",font = ("Verdana", 18), relief = GROOVE, width = 30)
        generatorbtn.pack(pady = 20)

        paintbtn = Button(self.master, text = "Start coloring", command = self.goColoring, bg = "#758AA2", fg = "#DAE0E2", font = ("Verdana", 18), relief = GROOVE, width = 30)
        paintbtn.pack(pady = 20)

    def goPBN(self):
        self.name = self.input.get()
        self.master.destroy()
        window = Tk()
        gui2.PBN(window,self.name)
        window.mainloop()

    def goColoring(self):
        self.name = self.input.get()
        self.master.destroy()
        window = Tk()
        gui2.Paint(window,self.name)
        window.mainloop()

if __name__ == '__main__':
    wnd = Tk()
    startpage = Main(wnd)
    wnd.mainloop()
