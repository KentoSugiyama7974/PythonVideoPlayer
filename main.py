from MainWindows.MainWindow import MainWindow
from SubWindows.SubWindow import SubWindow
import tkinter as tk

class Application():
    def __init__(self,master=None):
        self.main_window = MainWindow(master)
        self.sub_window = SubWindow()
        self.change_command()

    def change_command(self):
        self.main_window.select_file_frame.file_select_button["command"] \
            = self.push_file_select_button

    def push_file_select_button(self):
        self.main_window.push_select_button()
        if self.main_window.path == "":
            return
        path = self.main_window.path
        self.sub_window.set_path(path)

if __name__ == "__main__":
    root = tk.Tk()
    window = Application(root)
    root.mainloop()