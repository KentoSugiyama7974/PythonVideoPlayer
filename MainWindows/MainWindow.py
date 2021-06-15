import tkinter as tk
from tkinter import messagebox
from MainWindows.SelectFile import SelectFile
from MainWindows.VideoPlayer import VideoPlayer

class MainWindow(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=1000,height=500)
        self.root = master
        self.config(bg="#EEEEEE")
        self.pack(expand=True,fill=tk.BOTH)
        self.select_file_frame = SelectFile(self)
        self.video_player_frame = VideoPlayer(self)
        self.change_command()
        self.playing = False
        self.root.protocol("WM_DELETE_WINDOW",self.push_x_button)
        self.frame_timer()

    def change_command(self):
        self.select_file_frame.file_select_button["command"] \
            = self.push_select_button
        self.video_player_frame.play_button["command"] \
            = self.push_play_button

    def push_select_button(self):
        self.select_file_frame.push_file_select_button()
        self.path = self.select_file_frame.get_path()
        if len(self.path) > 0:
            self.video_player_frame.get_video_frames(self.path)
            self.max_frame = self.video_player_frame.get_frames_num()

    def push_play_button(self):
        if self.video_player_frame.video == None:
            messagebox.showerror('エラー','ファイル選択する前に動画再生するな')
            return
        self.playing = not self.playing
        if self.playing:
            self.video_player_frame.play_button["text"] \
                = "Stop Video!"
        else:
            self.video_player_frame.play_button["text"] \
                = "Start Video!"

    def frame_timer(self):
        if self.playing:
            self.video_player_frame.next_frame()
            self.now = self.video_player_frame.get_now_frame()
        self.after(1,self.frame_timer)

    def push_x_button(self):
        self.video_player_frame.video_completion()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    main_frame = MainWindow(root)
    root.mainloop()
