import cv2
import tkinter as tk
from tkinter import ttk


class CameraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera GUI")

        # Create a label for the camera selection dropdown
        camera_label = ttk.Label(self.root, text="Select camera:")
        camera_label.pack()

        # Create a dropdown menu for camera selection
        self.camera_dropdown = ttk.Combobox(self.root, state="readonly")
        self.camera_dropdown.pack()
        self.camera_dropdown["values"] = self.get_camera_list()
        self.camera_dropdown.current(0)

        # Create a button to start the camera stream
        start_button = ttk.Button(
            self.root, text="Start", command=self.start_camera)
        start_button.pack()

        # Create a button to stop the camera stream
        stop_button = ttk.Button(
            self.root, text="Stop", command=self.stop_camera, state=tk.DISABLED)
        stop_button.pack()

        # Create a canvas to display the camera feed
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        # Create a variable to store the VideoCapture object
        self.cap = None

    def get_camera_list(self):
        """Return a list of available camera indices."""
        camera_list = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(str(i))
                cap.release()
        return camera_list

    def start_camera(self):
        """Start the camera stream."""
        # Get the selected camera index from the dropdown
        camera_index = int(self.camera_dropdown.get())

        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(camera_index)

        # Check if camera opened successfully
        if not self.cap.isOpened():
            print("Error opening video stream or file")
            return

        # Get the dimensions of the first frame from the camera
        ret, frame = self.cap.read()
        if not ret:
            print("Error reading frame from camera")
            return
        height, width, channels = frame.shape

        # Set the dimensions of the canvas to match the frame dimensions
        self.canvas.config(width=width, height=height)

        # Enable the stop button and disable the start button
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        # Start the camera loop
        self.update_camera()

    def stop_camera(self):
        """Stop the camera stream."""
        # Release the VideoCapture object
        self.cap.release()

        # Enable the start button and disable the stop button
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_camera(self):
        """Update the canvas with a new frame from the camera."""
        # Read a frame from the camera
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB format and resize it to fit the canvas
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(
                frame, (self.canvas.winfo_width(), self.canvas.winfo_height()))

            # Update the canvas with the new frame
            self.photo = tk.PhotoImage(
                data=cv2.imencode('.png', frame)[1].tobytes())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # Schedule the next update
            self.root.after(20, self.update_camera)

    def run(self):
        """Run the GUI loop."""
        self.start_button =
