import tkinter as tk
from tkinter import ttk
from SubWindows.PlotData import PlotData
from SubWindows.ImportData import ImportData
from tkinter import messagebox

class SubWindow():
    def __init__(self):
        self.sub_window = tk.Toplevel(bg="#000000",width=1000)
        self.sub_window.geometry("1000x500")
        self.chack_text = ["チーム活動量","チーム相関係数"]
        self.chack_bool = {}
        self.path = None
        self.choice_button = ttk.Button(
            self.sub_window,
            padding=[10,10],
            text="グラフの種類を選べ",
            command = self.push_choice_button,
        )
        self.choice_button.pack(fill=tk.BOTH)
        self.plot_data_frame = PlotData(self.sub_window)

    def set_path(self,path):
        self.path = path + "/"
        self.import_data = ImportData(self.path)
        self.team_act,self.team_corr,self.time = self.import_data.get_team_item()
        self.plot_data_frame.draw()

    def push_choice_button(self):
        if self.path == None:
            messagebox.showerror('エラー','Select Fileでフォルダを選択してください')
            return
        self.config_window = tk.Toplevel(bg="#DDDDDD")
        self.decision_button = tk.Button(
            self.config_window,
            text="グラフ化",
            command = self.push_decision_button
        )
        self.set_config_window()

    def set_config_window(self):
        for i in self.chack_text:
            self.chack_bool[i] = tk.BooleanVar()
            chack_box = tk.Checkbutton(
                self.config_window, 
                variable=self.chack_bool[i],
                text = i
                )
            chack_box.pack(side=tk.LEFT)
        self.decision_button.pack(side=tk.TOP)

    def push_decision_button(self):
        self.config_window.destroy()
        self.plot_data_frame.clear_plots()
        if self.chack_bool["チーム活動量"].get():
            self.plot_data_frame.set_title("team activity")
            self.plot_data_frame.plot_data(self.team_act)
        if self.chack_bool["チーム相関係数"].get():
            self.plot_data_frame.set_title("team corrcoef")
            self.plot_data_frame.plot_data(self.team_corr)
        self.plot_data_frame.plot_axis_data(self.time, 4)
        self.plot_data_frame.draw()

if __name__ == "__main__":
    root = tk.Tk()
    sub = SubWindow()
    sub.set_path("C:/Users/ymtlab/Documents/20210430/1_1")
    root.mainloop()
