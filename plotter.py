from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import csv
import sys
from parse_web import WeatherParser


class Plotter:
    def __init__(self, master):
        self.master = master
        self.parser = WeatherParser()
        self.stations_amount = len(self.parser.relevant_stations)
        self.times_amount = len(self.parser.relevant_times)
        
        self.fig = Figure(figsize = (7, 7), dpi = 100)
        self.ax = self.fig.subplots()
        pos = self.ax.get_position()
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.master)
        
        os.chdir(self.parser.csv_directory)
        self.ax.set_position([pos.x0, pos.y0, pos.width * 0.8, pos.height])
    
    def set_legend_position(self):
        leg = self.ax.legend(self.parser.relevant_stations)
        bb = leg.get_bbox_to_anchor().inverse_transformed(self.ax.transAxes)

        xOffset = 0.4
        bb.x0 += xOffset
        bb.x1 += xOffset
        leg.set_bbox_to_anchor(bb, transform = self.ax.transAxes)
    
    def plot_by_day(self, filename):
        with open(filename, "r", encoding="UTF-8") as file:
            reader = csv.reader(file,delimiter=";")
            all_data = [row for row in reader]
            
            for i in range(self.stations_amount):
                temperatures = []
                for j in range(self.times_amount):
                    temp = float(all_data[i + self.stations_amount*j][2])
                    temperatures.append(temp)
                self.ax.plot(self.parser.relevant_times, temperatures, label = all_data[i][1])
                
        self.ax.set(xlabel="Time of Day", ylabel="Temperature in °C",title=filename[:-4])
        self.set_legend_position()
        self.canvas.draw() 
        self.canvas.get_tk_widget().pack()
        
    def clear_plot(self):
        self.ax.clear()