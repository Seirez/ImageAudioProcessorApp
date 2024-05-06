import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from pydub import AudioSegment

class ImageAudioProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Audio Processor")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Menu
        self.menu_frame = tk.Frame(self.main_frame)
        self.menu_frame.pack(pady=5)

        self.choose_label = tk.Label(self.menu_frame, text="Choose Task:")
        self.choose_label.grid(row=0, column=0)

        self.task_var = tk.StringVar()
        self.task_var.set("")

        self.image_resizer_button = tk.Radiobutton(self.menu_frame, text="Image Resizer", variable=self.task_var, value="Image Resizer")
        self.image_resizer_button.grid(row=0, column=1)

        self.audio_compressor_button = tk.Radiobutton(self.menu_frame, text="Audio Compressor", variable=self.task_var, value="Audio Compressor")
        self.audio_compressor_button.grid(row=0, column=2)

        self.perform_button = tk.Button(self.menu_frame, text="Perform Task", command=self.perform_task)
        self.perform_button.grid(row=0, column=3, padx=10)

        # Image Resizer Widgets
        self.image_frame = tk.Frame(self.main_frame)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        self.size_label = tk.Label(self.image_frame, text="Enter size (widthxheight):")
        self.size_label.pack()

        self.size_entry = tk.Entry(self.image_frame)
        self.size_entry.pack()

        self.load_image_button = tk.Button(self.image_frame, text="Load Image", command=self.load_image)
        self.load_image_button.pack(pady=5)

        self.resize_button = tk.Button(self.image_frame, text="Resize Image", command=self.resize_image)
        self.resize_button.pack(pady=5)

        self.save_image_button = tk.Button(self.image_frame, text="Save Image", command=self.save_image)
        self.save_image_button.pack(pady=5)

        # Audio Compressor Widgets
        self.audio_frame = tk.Frame(self.main_frame)

        self.load_audio_button = tk.Button(self.audio_frame, text="Load Audio", command=self.load_audio)
        self.load_audio_button.pack(pady=5)

        self.compress_button = tk.Button(self.audio_frame, text="Compress Audio", command=self.compress_audio)
        self.compress_button.pack(pady=5)

        self.save_audio_button = tk.Button(self.audio_frame, text="Save Audio", command=self.save_audio)
        self.save_audio_button.pack(pady=5)

        # Hide processing frames by default
        self.image_frame.pack_forget()
        self.audio_frame.pack_forget()

        # Initialize attributes
        self.image = None
        self.audio = None
        self.resized_image = None

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image = cv2.imread(path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def display_image(self, image):
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.image_label.config(image=image)
        self.image_label.image = image

    def resize_image(self):
        if self.image is not None:
            size = self.size_entry.get()
            try:
                width, height = map(int, size.split('x'))
                self.resized_image = cv2.resize(self.image, (width, height))
                self.display_image(self.resized_image)
            except ValueError:
                print("Invalid size format. Please use format 'widthxheight' (e.g., '800x600').")


    def save_image(self):
        if self.resized_image is not None:
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if path:
                cv2.imwrite(path, cv2.cvtColor(self.resized_image, cv2.COLOR_RGB2BGR))
                print("Image saved successfully.")
        else:
            print("No processed image to save.")

    def load_audio(self):
        path = filedialog.askopenfilename()
        if path:
            self.audio = AudioSegment.from_file(path)

    def compress_audio(self):
        if self.audio:
            self.audio.export("compressed_audio.mp3", format="mp3", bitrate="64k")
            print("Audio compressed successfully.")

    def save_audio(self):
        if self.audio:
            path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if path:
                self.audio.export(path, format="mp3")
                print("Audio saved successfully.")

    def perform_task(self):
        task = self.task_var.get()
        if task == "Image Resizer":
            self.audio_frame.pack_forget()
            self.image_frame.pack()
        elif task == "Audio Compressor":
            self.image_frame.pack_forget()
            self.audio_frame.pack()

def main():
    root = tk.Tk()
    app = ImageAudioProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
