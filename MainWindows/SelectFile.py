import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

class SelectFile(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=100,height=100)
        self.config(bg="#000000")
        self.pack(fill=tk.BOTH)
        self.create_file_select_button()
        self.create_label()
        self.path = "" 

    def create_file_select_button(self):
        self.file_select_button = ttk.Button(
            self,
            text="File Select!",
            padding=[3,10],
            command = self.push_file_select_button,
        )
        self.file_select_button.pack(side=tk.LEFT)

    def create_label(self):
        self.label = tk.Label(
            self,
            text="<- このボタンでファイルを選択",
            font=("",30),
            background="#000000",
            foreground="#FFFFFF"
        )
        self.label.pack(side=tk.LEFT)

    def push_file_select_button(self):
        path = tk.filedialog.askdirectory(initialdir="C:/Users/ymtlab/Documents/20210430/")
        if self.path == "" and path == "":
            self.label["text"] = "<- もう一回ファイル選択してね"
        else:
            if path != "":
                self.path = path
            self.label["text"] = self.path

    def get_path(self):
        return self.path

if __name__ == "__main__":
    root = tk.Tk()
    a = SelectFile(master=root)
    root.mainloop()