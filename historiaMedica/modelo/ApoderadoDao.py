from .conexion import ConexionDB
from tkinter import messagebox
import sqlite3
import tkinter as tk


class ConexionDB:
    def __init__(self):
        self.conexion = sqlite3.connect('C:\\Users\\Patricia\\Desktop\\proyectoHistorial\\historiaMedica\\database\\dbhistorial1.db')  # Ajusta el path de la base de datos
        self.cursor = self.conexion.cursor()

    def cerrarConexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
# Clase modelo para representar un Apoderado
class Apoderado:
    def __init__(self, RUTapoderado, nombre, direccionActual, telefonoContacto, correoElectronico, relacionConElResidente, RUTpaciente):
        self.RUTapoderado = RUTapoderado
        self.nombre = nombre
        self.direccionActual = direccionActual
        self.telefonoContacto = telefonoContacto
        self.correoElectronico = correoElectronico
        self.relacionConElResidente = relacionConElResidente
        self.RUTpaciente = RUTpaciente

    def __str__(self):
        return f"Apoderado({self.RUTapoderado}, {self.nombre}, {self.direccionActual}, {self.telefonoContacto}, {self.correoElectronico}, {self.relacionConElResidente}, {self.RUTpaciente})"

# Función para guardar un apoderado en la base de datos
def guardarApoderado(apoderado: Apoderado):
    conexion = ConexionDB()
    sql = """INSERT INTO Apoderado (RUTapoderado, nombre, direccionActual, telefonoContacto, correoElectronico, relacionConElResidente, RUTpaciente)
             VALUES (?, ?, ?, ?, ?, ?, ?)"""
    try:
        conexion.cursor.execute(sql, (
            apoderado.RUTapoderado,
            apoderado.nombre,
            apoderado.direccionActual,
            apoderado.telefonoContacto,
            apoderado.correoElectronico,
            apoderado.relacionConElResidente,
            apoderado.RUTpaciente
        ))
        conexion.conexion.commit()
        messagebox.showinfo('Guardar Apoderado', 'Apoderado registrado exitosamente')
    except Exception as e:
        messagebox.showerror('Guardar Apoderado', f'Error al registrar apoderado: {e}')
    finally:
        conexion.cerrarConexion()


def buscarApoderadoPorPaciente(rut_paciente):
    print(f"Buscando apoderado para el paciente con RUT: {rut_paciente}")
    conexion = ConexionDB()
    sql = """
        SELECT A.RUTapoderado, A.nombre, A.direccionActual, A.telefonoContacto, 
            A.correoElectronico, A.relacionConElResidente
        FROM Apoderado A
        INNER JOIN Persona P ON A.RUTpaciente = P.RUTpaciente
        WHERE P.RUTpaciente = ?
    """
    try:
        conexion.cursor.execute(sql, (rut_paciente,))
        resultado = conexion.cursor.fetchone()
        print(f"Resultado de la consulta: {resultado}")  # Depuración
        return resultado
    except Exception as e:
        messagebox.showerror("Buscar Apoderado", f"Error: {e}")
        return None
    finally:
        conexion.cerrarConexion()
# Función para listar todos los apoderados

def buscarApoderadoPorRUT(rut_apoderado):
    print(f"Buscando apoderado con RUT: {rut_apoderado}")
    conexion = ConexionDB()
    sql = """
        SELECT RUTapoderado, nombre, direccionActual, telefonoContacto, 
               correoElectronico, relacionConElResidente
        FROM Apoderado
        WHERE RUTapoderado = ?
    """
    try:
        conexion.cursor.execute(sql, (rut_apoderado,))
        resultado = conexion.cursor.fetchone()
        print(f"Resultado de la consulta: {resultado}")
        return resultado
    except Exception as e:
        messagebox.showerror("Buscar Apoderado", f"Error: {e}")
        return None
    finally:
        conexion.cerrarConexion()


# Función para eliminar un apoderado por su RUT
def eliminarApoderado(RUTapoderado):
    conexion = ConexionDB()
    sql = "DELETE FROM Apoderado WHERE RUTapoderado = ?"
    try:
        conexion.cursor.execute(sql, (RUTapoderado,))
        conexion.conexion.commit()
        messagebox.showinfo('Eliminar Apoderado', 'Apoderado eliminado exitosamente')
    except Exception as e:
        messagebox.showerror('Eliminar Apoderado', f'Error al eliminar apoderado: {e}')
    finally:
        conexion.cerrarConexion()

# Función para actualizar los datos de un apoderado
def editarApoderado(apoderado: Apoderado):
    conexion = ConexionDB()
    sql = """
        UPDATE Apoderado 
        SET nombre = ?, direccionActual = ?, telefonoContacto = ?, 
            correoElectronico = ?, relacionConElResidente = ?, RUTpaciente = ?
        WHERE RUTapoderado = ?
    """
    valores = (
        apoderado.nombre,
        apoderado.direccionActual,
        apoderado.telefonoContacto,
        apoderado.correoElectronico,
        apoderado.relacionConElResidente,
        apoderado.RUTpaciente,
        apoderado.RUTapoderado
    )

    try:
        conexion.cursor.execute(sql, valores)
        conexion.conexion.commit()
        messagebox.showinfo('Editar Apoderado', 'Datos de apoderado actualizados exitosamente')
    except Exception as e:
        messagebox.showerror('Editar Apoderado', f'Error al actualizar apoderado: {e}')
    finally:
        conexion.cerrarConexion()

def actualizarApoderado(RUTapoderado, nombre, direccion, telefono, correo, relacion):
    conexion = ConexionDB()
    sql = '''
    UPDATE Apoderado
        SET nombre=?, direccionActual=?, telefonoContacto=?, correoElectronico=?, relacionConElResidente=?
        WHERE RUTapoderado=?
    '''
    valores = (nombre, direccion, telefono, correo, relacion, RUTapoderado)
    try:
        conexion.cursor.execute(sql, valores)
        conexion.conexion.commit()
        messagebox.showinfo('Editar Apoderado', 'Apoderado actualizado correctamente')
    except Exception as e:
        messagebox.showerror('Editar Apoderado', f'Error: {e}')
    finally:
        conexion.cerrarConexion()

def guardarCambiosApoderado(self):
    try:
        nombre = self.svNombreEditar.get()
        direccion = self.svDireccionEditar.get()
        telefono = self.svTelefonoEditar.get()
        correo = self.svCorreoEditar.get()
        relacion = self.svRelacionEditar.get()

        apoderado = Apoderado(
            RUTapoderado=self.idApoderado,
            nombre=nombre,
            direccionActual=direccion,
            telefonoContacto=telefono,
            correoElectronico=correo,
            relacionConElResidente=relacion,
            RUTpaciente=self.RUTpacienteApoderado 
            #RUTpaciente=None  # Aquí necesitas pasar el RUTpaciente si lo tienes
        )

        editarApoderado(apoderado)

        messagebox.showinfo('Éxito', 'Apoderado actualizado correctamente.')
        self.topEditarApoderado.destroy()
        self.mostrarApoderados()

    except Exception as e:
        messagebox.showerror('Error', f'No se pudo actualizar el apoderado: {str(e)}')
        actualizarApoderado(self.idApoderado, nombre, direccion, telefono, correo, relacion)

def obtenerApoderados():
    
    conexion = ConexionDB()
    try:
        conexion.cursor.execute("SELECT * FROM Apoderado")
        apoderados = conexion.cursor.fetchall()
        return apoderados
    except Exception as e:
        messagebox.showerror('Obtener Apoderados', f'Error: {e}')
        return []
    finally:
        conexion.cerrarConexion()