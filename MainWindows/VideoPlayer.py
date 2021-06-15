import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox

class VideoPlayer(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=1000,height=500)
        self.config(bg="#000000")
        self.pack(expand=True,fill=tk.BOTH)
        self.path = None
        self.game_num = None
        self.video = None
        self.create_video_canvas()
        self.create_play_button()

    def create_video_canvas(self):
        self.video_canvas = tk.Canvas(
            self,
            width = 1000,
            height = 500,
            bg="#DDDDDD"
        )
        self.video_canvas.pack(expand=True,fill=tk.BOTH)

    def create_play_button(self):
        self.play_button = ttk.Button(
            self,
            text="Start Video!",
            padding=[10,10],
            command = self.push_play_button
        )
        self.play_button.pack()

    def get_video_frames(self,path):
        self.path = path
        self.game_num = path.split("/")[-1]
        self.video = cv2.VideoCapture(self.path+"/"+self.game_num+".mp4")
        self.next_frame()

    def push_play_button(self):
        self.next_frame()

    def next_frame(self):
        ret, self.frame = self.video.read()
        if not ret:
            messagebox.showerror("エラー","次のフレームがないので最初に戻ります")
            self.set_frame(0)
        rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        x = self.video_canvas.winfo_width()/pil.width
        y = self.video_canvas.winfo_height()/pil.height
        ratio = x if x<y else y
        pil = pil.resize((int(ratio*pil.width),int(ratio*pil.height)))
        self.image = ImageTk.PhotoImage(pil)
        objs = self.video_canvas.find_withtag("image")
        for obj in objs:
            self.video_canvas.delete(obj)
        x = (self.video_canvas.winfo_width()-self.image.width())//2
        y = (self.video_canvas.winfo_height()-self.image.height())//2
        self.video_canvas.create_image(
            x,y,
            image=self.image,
            anchor = tk.NW,
            tag = "image"
        )

    def set_frame(self,frame):
        self.video.set(cv2.CAP_PROP_POS_FRAMES,frame)
        self.next_frame()

    def get_now_frame(self):
        return self.video.get(cv2.CAP_PROP_POS_FRAMES)

    def get_frames_num(self):
        return self.video.get(cv2.CAP_PROP_FRAME_COUNT)

    def video_completion(self):
        if self.video != None:
            self.video.release()

if __name__ == "__main__":
    root = tk.Tk()
    path = "C:/Users/ymtlab/Documents/20201118/1_1"
    a = VideoPlayer(master=root)
    a.get_video_frames(path)
    root.mainloop()