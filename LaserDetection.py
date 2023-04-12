import cv2
import tkinter as tk
from PIL import ImageTk, Image


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Laser Detection")

        self.camera_selection = tk.StringVar(self.window)
        self.camera_selection.set(0)

        self.start_button = tk.Button(
            self.window, text="Start", command=self.start_camera)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(
            self.window, text="Stop", command=self.stop_camera, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)

        self.camera_selector = tk.OptionMenu(
            self.window, self.camera_selection, *self.get_camera_list())
        self.camera_selector.pack(side=tk.LEFT)

        self.video_frame = tk.Label(self.window)
        self.video_frame.pack()

        self.is_running = False
        self.camera = None
        self.video_stream = None

    def get_camera_list(self):
        cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()
        return cameras

    def start_camera(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.camera_selector.config(state=tk.DISABLED)

        self.camera = int(self.camera_selection.get())
        self.video_stream = cv2.VideoCapture(self.camera)

        self.update_camera()

    def stop_camera(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.camera_selector.config(state=tk.NORMAL)

        self.video_stream.release()

    def update_camera(self):
        ret, frame = self.video_stream.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)
            self.video_frame.configure(image=photo)
            self.video_frame.image = photo
        if self.is_running:
            self.window.after(1, self.update_camera)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
