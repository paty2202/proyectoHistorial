import sqlite3
import os
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO)

class ConexionDB:
    def __init__(self):
        self.baseDatos = "C:\\Users\\Patricia\\Desktop\\proyectoHistorial\\historiaMedica\\database\\dbhistorial1.db"
        os.makedirs(os.path.dirname(self.baseDatos), exist_ok=True)
        self.conexion = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        """Establece la conexión a la base de datos"""
        try:
            # Conecta a la base de datos SQLite
            self.conexion = sqlite3.connect(self.baseDatos)
            self.cursor = self.conexion.cursor()
            logging.info(f"Conectado a la base de datos: {self.baseDatos}")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            raise

    def ejecutar(self, sql, params=()):
        """Ejecuta una consulta SQL con parámetros"""
        try:
            self.cursor.execute(sql, params)
        except sqlite3.Error as e:
            logging.error(f"Error al ejecutar SQL: {e}")
            self.conexion.rollback()

    def commit(self):
        """Confirma los cambios en la base de datos"""
        if self.conexion:
            try:
                self.conexion.commit()
                logging.info("Cambios confirmados en la base de datos")
            except sqlite3.Error as e:
                logging.error(f"Error al hacer commit: {e}")
                self.conexion.rollback()
        else:
            logging.error("No hay conexión abierta para hacer commit.")

    def cerrarConexion(self):
        """Cierra la conexión y el cursor"""
        if self.cursor:
            self.cursor.close()
            logging.info("Cursor cerrado.")
        if self.conexion:
            self.conexion.close()
            logging.info("Conexión cerrada.")