from .conexion import ConexionDB
from tkinter import messagebox
import sqlite3



def verificarRUTExistente(RUTpaciente):
    conexion = ConexionDB()
    sql = "SELECT COUNT(*) FROM Persona WHERE RUTpaciente = ?"
    cursor = conexion.cursor.execute(sql, (RUTpaciente,))
    existe = cursor.fetchone()[0] > 0
    conexion.cerrarConexion()
    return existe
    

def obtenerPacientePorRUT(RUTpaciente):
    conexion = ConexionDB()
    sql = "SELECT * FROM Persona WHERE RUTpaciente = ?"
    
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, (RUTpaciente,))
        paciente = cursor.fetchone()
        
        if paciente:
        # Convertir la tupla en un diccionario si es necesario
            return {
                'RUTpaciente': paciente[0],  # RUTpaciente es el primer campo ahora
                'Nombres': paciente[1],
                'ApellidoPaterno': paciente[2],
                'ApellidoMaterno': paciente[3],
                'Sexo': paciente[4],
                'Fechanacimiento': paciente[5],
                'Edad': paciente[6],
                'EstadoCivil': paciente[7],
                'Direccionactual': paciente[8],
                'Creenciareligiosa': paciente[9],
                'IngresaDesde': paciente[10],
                'Antecedentes': paciente[11],
                'activo': paciente[12],
        }
        return None
    except Exception as e:
        print(f"Error al obtener los datos del paciente: {e}")
        return None
    finally:
        conexion.cerrarConexion()  # 
    

def actualizarDatoPaciente(persona, RUTpaciente):
    try: 
        conexion = ConexionDB()
        sql = """
        UPDATE Persona 
        SET 
            Nombres = ?,
            ApellidoPaterno = ?,
            ApellidoMaterno = ?,
            Sexo = ?,
            Fechanacimiento = ?,
            Edad = ?,
            EstadoCivil = ?,
            Direccionactual = ?,
            Creenciareligiosa = ?,
            IngresaDesde = ?,
            Antecedentes = ?,
            activo = ?
        WHERE RUTpaciente = ?"""

        cursor = conexion.cursor
        cursor = conexion.cursor.execute(sql, (
            persona.Nombres,
            persona.ApellidoPaterno,
            persona.ApellidoMaterno,
            persona.Sexo,
            persona.Fechanacimiento,
            persona.Edad,
            persona.EstadoCivil,
            persona.Direccionactual,
            persona.Creenciareligiosa,
            persona.IngresaDesde,
            persona.Antecedentes,
            persona.activo,
            RUTpaciente  # Usamos RUTpaciente como identificador
        ))
    
        conexion.commit()
        return cursor.rowcount > 0  # Retorna True si se actualizó al menos
    except Exception as e:
        print(f"Error al actualizar el paciente: {e}")
        return False  # Retorna False si ocurre un error

    finally:
        conexion.cerrarConexion()

def guardarDatoPaciente(persona, RUTpaciente=None):
    conexion = ConexionDB()
    
    if RUTpaciente is None:
        # Inserción
        sql = """
            INSERT INTO Persona (
                RUTpaciente, Nombres, ApellidoPaterno, ApellidoMaterno, Sexo,
                Fechanacimiento, Edad, EstadoCivil, Direccionactual, Creenciareligiosa,
                IngresaDesde, Antecedentes, activo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            persona.RUTpaciente,
            persona.Nombres,
            persona.ApellidoPaterno,
            persona.ApellidoMaterno,
            persona.Sexo,
            persona.Fechanacimiento,
            persona.Edad,
            persona.EstadoCivil,
            persona.Direccionactual,
            persona.Creenciareligiosa,
            persona.IngresaDesde,
            persona.Antecedentes,
            persona.activo
        )
    else:
        # Actualización
        sql = """
            UPDATE Persona SET 
                Nombres = ?, ApellidoPaterno = ?, ApellidoMaterno = ?, Sexo = ?,
                Fechanacimiento = ?, Edad = ?, EstadoCivil = ?, Direccionactual = ?,
                Creenciareligiosa = ?, IngresaDesde = ?, Antecedentes = ?, activo = ?
            WHERE RUTpaciente = ?
        """
        params = (
            persona.Nombres,
            persona.ApellidoPaterno,
            persona.ApellidoMaterno,
            persona.Sexo,
            persona.Fechanacimiento,
            persona.Edad,
            persona.EstadoCivil,
            persona.Direccionactual,
            persona.Creenciareligiosa,
            persona.IngresaDesde,
            persona.Antecedentes,
            persona.activo,
            persona.RUTpaciente  # Usamos RUTpaciente como identificador
        )

    try:
        conexion.cursor.execute(sql, params)
        conexion.conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar/actualizar datos: {e}")
        return False
    finally:
        conexion.cerrarConexion()

def listar():
    conexion = ConexionDB()

    listaPersona = []
    sql = 'SELECT * FROM Persona Where activo = 1'

    try:
        conexion.cursor.execute(sql)
        listaPersona = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except:
        title = 'Datos'
        mensaje = 'registros no existen'
        messagebox.showwarning(title, mensaje)
    return listaPersona

def listarCondicion(where):
    conexion = ConexionDB()
    listaPersona = []
    sql = f'SELECT * FROM Persona {where}'

    try:
        conexion.cursor.execute(sql)
        listaPersona = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except: 
        title = 'Datos'
        mensaje = 'registros no existen'
        messagebox.showwarning(title, mensaje)
    return listaPersona

def eliminarPaciente(RUTpaciente):
    conexion = ConexionDB()
    sql = f"""UPDATE Persona SET activo = 0 WHERE RUTpaciente = {RUTpaciente}""" 
    try:
        conexion.cursor.execute(sql)
        # Realizar el commit para guardar los cambios
        conexion.conexion.commit()

        # Verificar si la consulta afectó alguna fila
        if conexion.cursor.rowcount > 0:
            title = 'Eliminar Paciente'
            mensaje = 'Paciente eliminado exitosamente'
            messagebox.showwarning(title, mensaje)
        else:
            title = 'Eliminar Paciente'
            mensaje = 'No se encontró el paciente con ese RUT.'
            messagebox.showwarning(title, mensaje)
    
    except sqlite3.Error as e:
        # Si ocurre un error con la base de datos
            title = 'Eliminar Paciente'
            mensaje = f'Error al eliminar paciente: {e}'
            messagebox.showwarning(title, mensaje)
    
    except Exception as e:
        # Capturar cualquier otro error inesperado
            title = 'Eliminar Paciente'
            mensaje = f'Error inesperado: {e}'
            messagebox.showwarning(title, mensaje)
    
    finally:
        # Cerrar la conexión para liberar recursos
            conexion.cerrarConexion()
        #conexion.cerrarConexion()
            #title = 'Eliminar Paciente'
        #mensaje = 'Paciente eliminado exitosamente'
        # except: 
        #title = 'Eliminar Paciente'
        #mensaje = 'Error al eliminar paciente'
        #messagebox.showwarning(title, mensaje)


class Persona:
    def __init__(self, datos):
        self.__dict__.update(datos)

        

