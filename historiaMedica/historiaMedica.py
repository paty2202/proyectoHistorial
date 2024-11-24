import tkinter as tk
from paciente.gui import Frame

def main():
    root = tk.Tk()
    root.title('HISTORIA MEDICA')
    root.resizable(0,0)
    

    frame = Frame(root)
    frame.mainloop()

if __name__ == '__main__':
    main()
