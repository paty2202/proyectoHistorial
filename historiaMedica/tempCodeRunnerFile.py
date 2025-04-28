import tkinter as tk
from paciente.gui import Frame

def main():
    root = tk.Tk()
    root.title('HISTORIA MEDICA')
    
    # Permitir que la ventana sea redimensionable
    root.resizable(True, True)  # Se puede redimensionar tanto en ancho como en alto
    
    # Ajustar el tamaño inicial de la ventana
    root.state('zoomed')   # Puedes cambiar el tamaño inicial si lo deseas
    #root.geometry('1200x600')

    frame = Frame(root)
    frame.mainloop()

if __name__ == '__main__':
    main()