import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk
from visage_differentiation import visage_identifier


class Application(tk.Frame):
    """A GUI for identifying unknown visages in an image."""

    def __init__(self, master=None):
        """
        Create an application instance.

        :param master: The toplevel Tk widget.
        """
        super().__init__(master)
        self.master = master
        self.master.title("Visage Differentiation")
        self.master.minsize(740, 160)
        self.master.resizable(False, False)

        self.known_visages_label = None
        self.known_visages_text = None
        self.known_visages_button = None
        self.known_visages_entry = None
        self.unknown_visages_label = None
        self.unknown_visages_text = None
        self.unknown_visages_button = None
        self.unknown_visages_entry = None
        self.div = None
        self.identified_visages_window = None
        self.identify_visages_button = None
        self.identified_visages_image = None
        self.identified_visages_image_tk = None
        self.identified_visages_label = None
        self.identified_visages_file = None
        self.save_image_button = None

        self.create_widgets()

    def create_widgets(self):
        """Create the primary widgets for this frame."""
        # Known visages
        self.known_visages_label = ttk.Label(self.master, text="Known Visage(s)", font=("bold", 12))
        self.known_visages_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=tk.W)
        self.known_visages_text = tk.StringVar()
        self.known_visages_entry = ttk.Entry(self.master, width=70, textvariable=self.known_visages_text,
                                             state="readonly")
        self.known_visages_entry.grid(row=0, column=1, padx=(25, 25))
        self.known_visages_button = ttk.Button(self.master, text="Select Directory...", width=16,
                                               command=self.known_visages_dialog)
        self.known_visages_button.grid(row=0, column=2)

        # Unknown visages
        self.unknown_visages_label = ttk.Label(self.master, text="Unknown Visage(s)", font=("bold", 12))
        self.unknown_visages_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky=tk.W)
        self.unknown_visages_text = tk.StringVar()
        self.unknown_visages_entry = ttk.Entry(self.master, width=70, textvariable=self.unknown_visages_text,
                                               state="readonly")
        self.unknown_visages_entry.grid(row=1, column=1, padx=(25, 25))
        self.unknown_visages_button = ttk.Button(self.master, text="Select Image...", width=16,
                                                 command=self.unknown_visages_dialog)
        self.unknown_visages_button.grid(row=1, column=2)

        # Divider
        self.div = ttk.Separator(self.master, orient=tk.HORIZONTAL)
        self.div.grid(row=2, column=0, columnspan=3, padx=(10, 0), pady=15, sticky=tk.EW)

        # Identify visages
        self.identify_visages_button = ttk.Button(self.master, text="Identify Visages", width=14,
                                                  command=self.identify_visages)
        self.identify_visages_button.grid(row=3, column=1)

    def known_visages_dialog(self):
        """Prompt the user for a directory containing images of known visages."""
        self.known_visages_text.set(filedialog.askdirectory(initialdir="/", title="Select a Directory"))

    def unknown_visages_dialog(self):
        """Prompt the user for an image of unknown visages."""
        file_types = (("Image files", "*.jpg *.jpeg *.png"),
                      ("All files", "*.*"))
        self.unknown_visages_text.set(filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                                                 filetypes=file_types))

    def save_image_dialog(self):
        """Prompt the user to save the image of identified visages."""
        file_types = (("Image files", "*.jpg *.jpeg *.png"),
                      ("All files", "*.*"))
        self.identified_visages_file = filedialog.asksaveasfile(filetypes=file_types, initialfile="identified_visages",
                                                                defaultextension=".jpg")

        try:
            self.identified_visages_image.save(self.identified_visages_file.name)
        except AttributeError:
            return

    def identify_visages(self):
        """Identifies unknown visages and displays an image with the visages outlined and labeled."""
        if self.identified_visages_window is None or not self.identified_visages_window.winfo_exists():
            self.identified_visages_window = tk.Toplevel(self.master)
            self.identified_visages_window.minsize(100, 100)
            self.identified_visages_window.maxsize(1280, 720)
            self.identified_visages_window.resizable(False, False)

        # Save image
        self.save_image_button = ttk.Button(self.identified_visages_window, width=15, text="Save Image",
                                            command=self.save_image_dialog)
        self.save_image_button.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=tk.W)

        # Identified visages
        try:
            self.identified_visages_image = visage_identifier.identify(self.known_visages_text.get(),
                                                                       self.unknown_visages_text.get())
        except (FileNotFoundError, TypeError, AttributeError):
            self.identified_visages_window.destroy()
            return

        self.identified_visages_image_tk = ImageTk.PhotoImage(self.identified_visages_image)
        self.identified_visages_label = tk.Label(self.identified_visages_window, image=self.identified_visages_image_tk)
        self.identified_visages_label.image = self.identified_visages_image_tk
        self.identified_visages_label.grid(row=1, column=0)

        self.identified_visages_window.geometry(f"{self.identified_visages_image.width}x"
                                                f"{self.identified_visages_image.height}")
        self.identified_visages_window.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
