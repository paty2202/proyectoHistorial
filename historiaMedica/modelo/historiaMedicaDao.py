from .conexion import ConexionDB
from tkinter import messagebox
import tkinter as tk
import sqlite3

# Clase para manejar la conexión con la base de datos
class ConexionDB:
    def __init__(self):
        self.conexion = sqlite3.connect('C:\\Users\\Patricia\\Desktop\\proyectoHistorial\\historiaMedica\\database\\dbhistorial1.db')  # Ajusta el path de la base de datos
        self.cursor = self.conexion.cursor()

    def cerrarConexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()


# Función para listar historias médicas
def listarHistoria(RUTpaciente):
    conexion = ConexionDB()
    listaHistoria = []

      # Imprime el tipo y el valor de RUTpaciente antes de ejecutar la consulta
    print(f"Tipo de RUTpaciente: {type(RUTpaciente)}")
    print(f"Valor de RUTpaciente: {RUTpaciente}")

    RUTpaciente_str = str(RUTpaciente).replace('.', '').replace('-', '')

    # Consulta con parámetros para evitar inyección SQL
    sql = '''SELECT h.idhistoriaMedica, p.apellidoPaterno || " " || p.apellidoMaterno AS Apellidos, 
             h.fechaHistoria, h.diagnostico, h.examenes, h.tratamientofarmacologico, h.observaciones 
             FROM historiaMedica h 
             INNER JOIN Persona p ON p.RUTpaciente = h.RUTpaciente 
             WHERE p.RUTpaciente = ?'''  # Usamos el parámetro "?"

       # Verificar si el RUTpaciente es entero o texto, y luego ejecutar la consulta
    if isinstance(RUTpaciente, int):
        # Si RUTpaciente es un número entero
        conexion.cursor.execute(sql, (RUTpaciente,))
    else:
        # Si RUTpaciente es un texto (por ejemplo, cadena con guiones)
        conexion.cursor.execute(sql, (str(RUTpaciente),))

    try:
        listaHistoria = conexion.cursor.fetchall()
        print(f"Resultado de la consulta: {listaHistoria}")
    except Exception as e:
        title = 'LISTAR HISTORIA'
        mensaje = f'Error al listar historia médica: {str(e)}'
        messagebox.showerror(title, mensaje)

    return listaHistoria
    

# Función para guardar historias médicas
def guardarHistoria(RUTpaciente, fechaHistoria, diagnostico, examenes, tratamientofarmacologico, observaciones):
    conexion = ConexionDB()
    sql_insert = """INSERT INTO historiaMedica (RUTpaciente, fechaHistoria, diagnostico, examenes, tratamientofarmacologico, observaciones) 
                    VALUES (?, ?, ?, ?, ?, ?)"""

    try:
        conexion.cursor.execute(sql_insert, (RUTpaciente, fechaHistoria, diagnostico, examenes, tratamientofarmacologico, observaciones))
        conexion.conexion.commit()  # Confirmar los cambios en la base de datos

        # Mensaje de éxito
        title = 'Registro Historia Medica'
        mensaje = 'Historia registrada exitosamente'
        messagebox.showinfo(title, mensaje)

    except Exception as e:
        title = 'Registro Historia Medica'
        mensaje = f'Error al registrar historia: {str(e)}'
        messagebox.showerror(title, mensaje)

    finally:
        conexion.cerrarConexion()


# Función para mostrar el historial médico
def mostrar_historial_medico(RUTpaciente):
    historial = listarHistoria(RUTpaciente)
    
    # Si no se obtienen historias médicas, muestra un mensaje de error
    if not historial:
        messagebox.showwarning("Advertencia", "No se encontraron historias médicas para este paciente.")
        return

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Historial Médico")

    # Crear el Listbox para mostrar los resultados
    listbox = tk.Listbox(root, width=100, height=20)

    # Crear el Scrollbar y asociarlo con el Listbox
    scrollbar = tk.Scrollbar(root, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)

    # Llenar el Listbox con los datos del historial médico
    for historia in historial:
        # Inserta los datos en formato Apellidos | Fecha | Diagnóstico
        listbox.insert(tk.END, f"{historia[1]} | {historia[2]} | {historia[3]}")

    # Colocar el Listbox y el Scrollbar en la interfaz
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Ejecutar la aplicación
    root.mainloop()

def eliminarHistoria(idHistoriaMedica):
    conexion = ConexionDB()
    sql = 'DELETE FROM historiaMedica WHERE idhistoriaMedica = ?'
    try:
        # Ejecutamos la eliminación usando un parámetro
        conexion.cursor.execute(sql, (idHistoriaMedica,))
        conexion.conexion.commit()  # Confirmar los cambios
        messagebox.showinfo('Eliminar Historia', 'Historia médica eliminada exitosamente')
    except Exception as e:
        messagebox.showerror('Eliminar Historia', f'Error al eliminar historia médica: {e}')
    finally:
        conexion.cerrarConexion()

def editarHistoria(idhistoriaMedica, fechaHistoria, diagnostico, examenes, tratamientofarmacologico, observaciones):
    conexion = ConexionDB()
    sql_update = """
        UPDATE historiaMedica
        SET fechaHistoria           = ?,
            diagnostico             = ?,
            examenes                = ?,
            tratamientofarmacologico = ?,
            observaciones           = ?
        WHERE idhistoriaMedica = ?
    """
    try:
        conexion.cursor.execute(sql_update, (
            fechaHistoria,
            diagnostico,
            examenes,
            tratamientofarmacologico,
            observaciones,
            idhistoriaMedica
        ))
        conexion.conexion.commit()

        messagebox.showinfo('Editar Historia Médica', 'Historia médica actualizada exitosamente')
    except Exception as e:
        messagebox.showerror('Editar Historia Médica', f'Error al editar historia médica: {e}')
    finally:
        conexion.cerrarConexion()

        

# Clase para representar una historia médica (opcional)
class historiaMedica:
    def __init__(self, RUTpaciente, fechaHistoria, diagnostico, examenes, tratamientofarmacologico, observaciones):
        self.idhistoriaMedica = None
        self.RUTpaciente = RUTpaciente
        self.fechaHistoria = fechaHistoria
        self.diagnostico = diagnostico
        self.examenes = examenes
        self.tratamientofarmacologico = tratamientofarmacologico
        self.observaciones = observaciones

    def __str__(self):
        return f'''historiaMedica[
    {self.RUTpaciente}, 
    {self.fechaHistoria}, 
    {self.diagnostico},
    {self.examenes}, 
    {self.tratamientofarmacologico}, 
    {self.observaciones}
]'''


# Llamada para mostrar el historial médico de un paciente específico
##RUTpaciente = 42353  # Cambia por el RUT del paciente real
#mostrar_historial_medico(RUTpaciente)

def actualizarHistoriaMedica(id_historia, fecha, diagnostico, examenes, tratamiento, observaciones):
    try:
        conexion = ConexionDB()
        sql = '''UPDATE historiaMedica 
            SET fechaHistoria = ?, diagnostico = ?, examenes = ?, 
                tratamientofarmacologico = ?, observaciones = ?
            WHERE idhistoriaMedica = ?'''
        valores = (fecha, diagnostico, examenes, tratamiento, observaciones, id_historia)
        conexion.cursor.execute(sql, valores)
        conexion.conexion.commit()
        conexion.conexion.close()
        return True
    except Exception as e:
        print(f"Error al actualizar historia médica: {e}")
        return False