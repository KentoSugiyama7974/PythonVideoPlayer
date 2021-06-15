import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotData(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=1000,height=200)
        self.config(bg="#000000")
        self.pack(expand=True,fill=tk.BOTH)
        self.data = None
        self.fig = None
        self.strs = None
        self.create_plot_canvas()

    def create_plot_canvas(self):
        plt.rcParams["xtick.direction"] = "in"
        plt.rcParams["ytick.direction"] = "in"
        self.fig, self.ax = plt.subplots()
        self.ax.xaxis.set_ticks_position('both')
        self.ax.yaxis.set_ticks_position('both')
        self.plot_canvas = FigureCanvasTkAgg(self.fig, self)
        self.plot_canvas.get_tk_widget().pack(expand=True,fill=tk.BOTH)
        self.plot_canvas.mpl_connect("button_press_event",self.click_event)

    def set_title(self,title):
        self.fig.suptitle(title)

    def plot_data(self,data):
        self.data = data
        for key,value in data.items():
            self.ax.plot(range(len(value)),value,label=key)
        self.ax.legend()
        # self.plot_canvas.draw()

    def plot_vertical(self,x):
        self.ax.axvline(x,color='black')
        # self.plot_canvas.draw()

    def plot_axis_data(self,strs,blank):
        self.strs = strs
        self.blank = blank
        self.ax.set_xticks(range(0,len(strs),blank))
        self.ax.set_xticklabels(strs[::blank],rotation=90)
        # self.plot_canvas.draw()

    def clear_plots(self):
        self.ax.cla()

    def updata_plos(self,x=None):
        if self.data == None:
            return
        if self.strs == None:
            return
        self.clear_plots()
        self.plot_vertical(x)
        self.plot_data(self.data)
        self.plot_axis_data(self.strs,self.blank)
        self.ax.legend()
        self.draw()

    def draw(self):
        self.plot_canvas.draw()

    def click_event(self, event):
        self.x = event.xdata
        self.y = event.ydata
        self.updata_plos(self.x)

    def plot_completion(self):
        print("plotを正常終了します...")
        if self.fig != None:        
            plt.close(self.fig)

if __name__ == "__main__":
    root = tk.Tk()
    a = PlotData(master=root)
    data = {"A":[1,2,3,4,5],"B":[8,9,6,8,1]}
    strs = ["1","2","3","4","5"]
    a.plot_data(data)
    a.plot_axis_data(strs,1)
    root.mainloop()