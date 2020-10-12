import tkinter
from tkinter import *
import os
from datetime import datetime

from parse_web import WeatherParser
import generate_sample as gen
import plotter


root = Tk()
root.wm_geometry("1000x800")
root.resizable(False, False)
root.title("CSV Visualizer")

class App:
    def __init__(self,master):
        self.master = master
        gui = Wetterdienst(self.master)
    
class Wetterdienst:
    def __init__(self,parent):
        self.parent = parent
        self.parser = WeatherParser()
        
        # ----
        self.upper = Frame(self.parent)
        self.lower_left = Frame(self.parent)
        self.lower_right = Frame(self.parent)
        self.plotter = plotter.Plotter(self.lower_right)
        
        self.b_create = Button(self.upper,text="Create Sample", command=self.press_create)
        self.file_view = Listbox(self.lower_left, width=15, height=24, font=("Helvetica", 12), selectmode=SINGLE)
        self.scrollbar = Scrollbar(self.lower_left, orient="vertical")
        self.scrollbar.config(command=self.file_view.yview)
        self.file_view.config(yscrollcommand=self.scrollbar.set)
        
        self.upper.grid(row="0")
        self.b_create.grid(row="0",column="0")
        self.lower_left.grid(row="1",column="0")
        self.file_view.pack(side=LEFT)
        self.scrollbar.pack(side=RIGHT, fill="y")
        self.lower_right.grid(row="1",column="1")
        
        self.file_view.bind("<Double-Button>", lambda event: self.plot_csv(event))
        self.update_textbox()
    
    def plot_csv(self, event):
        self.plotter.clear_plot()
        self.plotter.plot_by_day(self.file_view.get(ANCHOR))
    
    def press_create(self):
        gen.generate_sample()
        self.update_textbox()
        
    def update_textbox(self):
        all_csvs = [datetime.strptime(filename,"%d.%m.%Y.csv") for filename in os.listdir(self.parser.csv_directory) if filename.endswith(".csv")]
        all_csvs.sort()
        self.file_view.delete(0,END)
        for filename in all_csvs:
            filename = datetime.strftime(filename,"%d.%m.%Y.csv")
            self.file_view.insert(END,filename)

app = App(root)
root.mainloop()