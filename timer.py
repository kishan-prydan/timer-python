import tkinter as tk
from tkinter import messagebox
import threading
import time
import ctypes
import winsound

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")
        self.root.configure(bg='black')

        self.kernel32 = ctypes.WinDLL('kernel32')
        self.SetThreadExecutionState = self.kernel32.SetThreadExecutionState
        self.SetThreadExecutionState.restype = ctypes.c_uint
        self.SetThreadExecutionState.argtypes = [ctypes.c_uint]

        self.create_main_screen()

    def create_main_screen(self):
        frame_minutes = tk.Frame(self.root, bg="black")
        frame_minutes.pack()

        label_minutes = tk.Label(frame_minutes, text="Enter minutes:", font=("Helvetica", 50), fg="white", bg="black")
        label_minutes.pack(side=tk.LEFT)

        self.entry_minutes = tk.Entry(frame_minutes, font=("Helvetica", 40), width=10, justify='center', bd=5)
        self.entry_minutes.pack(side=tk.LEFT, padx=(10, 0))

        frame_seconds = tk.Frame(self.root, bg="black")
        frame_seconds.pack()

        label_seconds = tk.Label(frame_seconds, text="Enter seconds:", font=("Helvetica", 50), fg="white", bg="black")
        label_seconds.pack(side=tk.LEFT)

        self.entry_seconds = tk.Entry(frame_seconds, font=("Helvetica", 40), width=10, justify='center', bd=5)
        self.entry_seconds.pack(side=tk.LEFT, padx=(10, 0))

        display_button = tk.Button(self.root, text="Display", command=self.display_timer_screen, font=("Helvetica", 20))
        display_button.pack()

        frame_minutes.place(relx=0.5, rely=0.3, anchor='center')
        frame_seconds.place(relx=0.5, rely=0.5, anchor='center')
        display_button.place(relx=0.5, rely=0.7, anchor='center')

    def create_timer_screen(self, minutes, seconds):
        self.timer_screen = tk.Toplevel(self.root)
        self.timer_screen.title("Timer")
        self.timer_screen.configure(bg='black')
        self.timer_screen.attributes('-fullscreen', True)

        self.remaining_time_label = tk.Label(self.timer_screen, text="", font=("Helvetica", 370, "bold"), fg="white", bg="black")
        self.remaining_time_label.pack()

        total_seconds = minutes * 60 + seconds
        self.start_timer(total_seconds)
        self.remaining_time_label.place(relx=0.5, rely=0.5, anchor='center')

    def start_timer(self, total_seconds):
        self.SetThreadExecutionState(0x80000002)

        self.remaining_time_label.config(text=self.format_time(total_seconds))
        self.timer_thread = threading.Thread(target=self.countdown, args=(total_seconds,))
        self.timer_thread.start()

    def countdown(self, total_seconds):
        while total_seconds > 0:
            time_format = self.format_time(total_seconds)
            self.remaining_time_label.config(text=time_format)

            if total_seconds == 120:
                self.blink_text()

            if total_seconds <= 120 and total_seconds % 60 == 0:
                self.blink_text()

            time.sleep(1)
            total_seconds -= 1

        self.remaining_time_label.config(text="Time's up!", font=("Helvetica", 200, "bold"))

        time.sleep(1)

        for _ in range(5):
            winsound.Beep(1000, 1000)
            time.sleep(0.5)

        self.remaining_time_label.place(relx=0.5, rely=0.5, anchor='center')
        self.SetThreadExecutionState(0x80000000)

    def blink_text(self):
        self.blink_color = 'red'

        def blink():
            self.remaining_time_label.config(fg=self.blink_color)
            self.blink_color = 'white' if self.blink_color == 'red' else 'red'
            self.remaining_time_label.after(494, blink)

        blink()

    def format_time(self, total_seconds):
        minutes, seconds = divmod(total_seconds, 60)
        return "{:02d}:{:02d}".format(minutes, seconds)

    def display_timer_screen(self):
        try:
            input_minutes = int(self.entry_minutes.get())
            input_seconds = int(self.entry_seconds.get())
            self.create_timer_screen(input_minutes, input_seconds)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for minutes and seconds.")

    def cancel_timer(self):
        self.timer_screen.destroy()
        if hasattr(self, 'timer_thread') and self.timer_thread.is_alive():
            self.timer_thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = TimerApp(root)
    root.mainloop()
