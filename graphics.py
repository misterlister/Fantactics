from tkinter import BOTH, Canvas

bg_col = '#d9d9d9'
window_width = 1200
window_height = 900

class Window:
    def __init__(self, width_val, height_val, root) -> None:
        self.__root = root
        self.__root.title("Fantactics")
        self.__root.geometry(f"{width_val}x{height_val}")
        self.__root.configure(background=bg_col)
        self.canvas = Canvas(self.__root)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(background=bg_col)
        self.running = True
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()
        
    def close(self):
        self.running = False
