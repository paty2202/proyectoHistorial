import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))




import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Button, ttk, scrolledtext, Toplevel, LabelFrame #LABELFRAME
from modelo.pacienteDao import Persona, obtenerPacientePorRUT, guardarDatoPaciente, listarCondicion, listar, verificarRUTExistente, actualizarDatoPaciente, eliminarPaciente
#from historiaMedica.modelo.pacienteDao import obtenerPacientePorRUT, guardarDatoPaciente, listarCondicion, listar, verificarRUTExistente, actualizarDatoPaciente, eliminarPaciente
from modelo.historiaMedicaDao import historiaMedica, guardarHistoria, listarHistoria, eliminarHistoria, actualizarHistoriaMedica
from modelo.ApoderadoDao import  guardarApoderado, eliminarApoderado, editarApoderado, buscarApoderadoPorPaciente, actualizarApoderado,Apoderado, buscarApoderadoPorRUT, obtenerApoderados

from tkinter import messagebox
import tkcalendar as tc 
from tkcalendar import *
from tkcalendar import Calendar
from datetime import datetime, date
from tkinter import StringVar





class Frame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill=tk.BOTH, expand=True)
        self.config(bg="#CDD8FF")
        
        # Crear un Canvas
        self.canvas = tk.Canvas(self, bg="#CDD8FF")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Agregar Scrollbar vertical
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar Canvas para trabajar con Scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Crear un Frame dentro del Canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg="#CDD8FF")

        # Agregar ese Frame al Canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.RUTpaciente = None
        self.idHistoriaMedica = None
        self.RUTpacienteHistoria = None
        self.camposPaciente()
        self.deshabilitar()
        self.tablaPaciente()
       
       
        #self.camposPaciente()
        #self.deshabilitar()
        #self.tablaPaciente()
      

    def mostrar_mensaje(self, titulo, mensaje, tipo):
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)

    def cargarDatosPaciente(self, RUTpaciente):
    # Guarda el ID del paciente actual
        print(f"Cargando datos para el paciente con RUT: {RUTpaciente}")
        paciente = obtenerPacientePorRUT(RUTpaciente)
    # Resto de la lógica  # Mensaje de depuración
    # Resto de la lógica # Necesitas definir esta función
    
        if paciente:
        # Rellena los campos de entrada con los datos del paciente
            self.svRUTpac.set(paciente['RUTpaciente'])
            self.svNombres.set(paciente['Nombres'])
            self.svApPaterno.set(paciente['ApellidoPaterno'])
            self.svApMaterno.set(paciente['ApellidoMaterno'])
            self.svSexo.set(paciente['Sexo'])
            self.svFN.set(paciente['Fechanacimiento'])
            self.svEdad.set(paciente['Edad'])
            self.svEstCi.set(paciente['EstadoCivil'])
            self.svDireccionac.set(paciente['Direccionactual'])
            self.svCreencia.set(paciente['Creenciareligiosa'])
            self.svIngresad.set(paciente['IngresaDesde'])
            self.svAnt.set(paciente['Antecedentes'])

    def guardarPaciente(self):
        datos = {
            'RUTpaciente': self.svRUTpac.get(),
            'Nombres': self.svNombres.get(),
            'ApellidoPaterno': self.svApPaterno.get(),
            'ApellidoMaterno': self.svApMaterno.get(),
            'Sexo': self.svSexo.get(),
            'Fechanacimiento': self.svFN.get(),
            'Edad': self.svEdad.get(),
            'EstadoCivil': self.svEstCi.get(),
            'Direccionactual': self.svDireccionac.get(),
            'Creenciareligiosa': self.svCreencia.get(),
            'IngresaDesde': self.svIngresad.get(),
            'Antecedentes': self.svAnt.get(),
            'activo': 1
        }

        persona = Persona(datos)
        print(f"Intentando guardar/actualizar paciente con RUT: {persona.RUTpaciente}")

        # Verificamos si el RUT ya existe en la base de datos
        if not verificarRUTExistente(persona.RUTpaciente):
            # Insertar un nuevo paciente si no existe
            resultado = guardarDatoPaciente(persona)  # Esta función debe insertar el paciente
            if resultado:
                self.mostrar_mensaje("Registrar Paciente", "Paciente registrado exitosamente", "info")
            else:
                self.mostrar_mensaje("Registrar Paciente", "Error al registrar paciente", "error")
        else:
            # Si el RUT ya existe, actualizamos el paciente con los nuevos datos
            resultado = actualizarDatoPaciente(persona, persona.RUTpaciente)  # Esta función debe actualizar el paciente
            if resultado:
                self.mostrar_mensaje("Actualizar Paciente", "Paciente actualizado exitosamente", "info")
            else:
                self.mostrar_mensaje("Actualizar Paciente", "Error al actualizar paciente", "error")

        # Deshabilitar los campos y actualizar la tabla
        self.deshabilitar()
        self.tablaPaciente()
        #self.topcalendario.destroy()

    def camposPaciente(self):
        #LABELS
        self.lblRUTpac = tk.Label(self.scrollable_frame, text="RUT paciente")
        self.lblRUTpac.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblRUTpac.grid(column=0,row=0, padx=5, pady=5)

        self.lblNombres = tk.Label(self.scrollable_frame, text="Nombres: ")
        self.lblNombres.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblNombres.grid(column=0, row=1, padx=5, pady=5)
    
        self.lblApPaterno = tk.Label(self.scrollable_frame, text="Apellido Paterno:")
        self.lblApPaterno.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblApPaterno.grid(column=0,row=2, padx=5, pady=5)

        self.lblApMaterno = tk.Label(self.scrollable_frame, text="Apellido Materno:")
        self.lblApMaterno.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblApMaterno.grid(column=0,row=3, padx=5, pady=5)

        self.lblSexo = tk.Label(self.scrollable_frame, text="Sexo:")
        self.lblSexo.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblSexo.grid(column=0,row=4, padx=5, pady=5)

        self.lblFN = tk.Label(self.scrollable_frame, text="Fecha nacimiento:")
        self.lblFN.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblFN.grid(column=0,row=5, padx=5, pady=5)

        
        self.lblEdad = tk.Label(self.scrollable_frame, text="Edad:")
        self.lblEdad.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblEdad.grid(column=0,row=6, padx=5, pady=5)

        self.lblEstCi = tk.Label(self.scrollable_frame, text="Estado Civil:")
        self.lblEstCi.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblEstCi.grid(column=0,row=7, padx=5, pady=5)

        self.lblDireccionac = tk.Label(self.scrollable_frame, text="Dirección actual:")
        self.lblDireccionac.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblDireccionac.grid(column=0,row=8, padx=5, pady=5)

        self.lblCreencia = tk.Label(self.scrollable_frame, text="Creencia religiosa:")
        self.lblCreencia.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblCreencia.grid(column=0,row=9, padx=5, pady=5)

        self.lblIngresad = tk.Label(self.scrollable_frame, text="Ingresa desde:")
        self.lblIngresad.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblIngresad.grid(column=0,row=10, padx=5, pady=5)

        self.lblAnt = tk.Label(self.scrollable_frame, text="Antecedentes:")
        self.lblAnt.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblAnt.grid(column=0,row=11, padx=2, pady=5)

#Entrys: valores
    
        self.svRUTpac = tk.StringVar()
        self.entryRUTpac = tk.Entry(self.scrollable_frame, textvariable=self.svRUTpac)
        self.entryRUTpac.config(width=40, font=("ARIAL", 15))
        self.entryRUTpac.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombres = tk.StringVar()
        self.entryNombres = tk.Entry(self.scrollable_frame, textvariable=self.svNombres)
        self.entryNombres.config(width=40, font=("ARIAL", 15))
        self.entryNombres.grid(column=1, row=1, padx=10, pady=5, columnspan=2)
        
        self.svApPaterno = tk.StringVar()
        self.entryApPaterno = tk.Entry(self.scrollable_frame, textvariable=self.svApPaterno)
        self.entryApPaterno.config(width=40, font=("ARIAL", 15))
        self.entryApPaterno.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svApMaterno = tk.StringVar()
        self.entryApMaterno = tk.Entry(self.scrollable_frame, textvariable=self.svApMaterno)
        self.entryApMaterno.config(width=40, font=("ARIAL", 15))
        self.entryApMaterno.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svSexo = tk.StringVar()
        self.entrySexo = tk.Entry(self.scrollable_frame, textvariable=self.svSexo)
        self.entrySexo.config(width=40, font=("ARIAL", 15))
        self.entrySexo.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svFN = tk.StringVar()
        self.entryFN = tk.Entry(self.scrollable_frame, textvariable=self.svFN)
        self.entryFN.config(width=40, font=("ARIAL", 15))
        self.entryFN.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        self.svEdad = tk.StringVar()
        self.entryEdad = tk.Entry(self.scrollable_frame, textvariable=self.svEdad)
        self.entryEdad.config(width=40, font=("ARIAL", 15)) #state='disabled')
        self.entryEdad.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

        self.svEstCi = tk.StringVar()
        self.entryEstCi = tk.Entry(self.scrollable_frame, textvariable=self.svEstCi)
        self.entryEstCi.config(width=40, font=("ARIAL", 15))
        self.entryEstCi.grid(column=1, row=7, padx=10, pady=5, columnspan=2)

        self.svDireccionac = tk.StringVar()
        self.entryDireccionac = tk.Entry(self.scrollable_frame, textvariable=self.svDireccionac)
        self.entryDireccionac.config(width=40, font=("ARIAL", 15))
        self.entryDireccionac.grid(column=1, row=8, padx=10, pady=5, columnspan=2)

        self.svCreencia = tk.StringVar()
        self.entryCreencia = tk.Entry(self.scrollable_frame, textvariable=self.svCreencia)
        self.entryCreencia.config(width=40, font=("ARIAL", 15))
        self.entryCreencia.grid(column=1, row=9, padx=10, pady=5, columnspan=2)

        self.svIngresad = tk.StringVar()
        self.entryIngresad = tk.Entry(self.scrollable_frame, textvariable=self.svIngresad)
        self.entryIngresad.config(width=40, font=("ARIAL", 15))
        self.entryIngresad.grid(column=1, row=10, padx=10, pady=5, columnspan=2)

        self.svAnt = tk.StringVar()
        self.entryAnt = tk.Entry(self.scrollable_frame, textvariable=self.svAnt)
        self.entryAnt.config(width=40, font=("ARIAL", 15))
        self.entryAnt.grid(column=1, row=11, padx=10, pady=5, columnspan=2)

#Buttons

        self.btnNuevo = tk.Button(self.scrollable_frame, text="Nuevo", command=self.habilitar)
        self.btnNuevo.config(width=20, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#1658A2", cursor="hand2",activebackground="#35BD6F") # color verde es 158645
        self.btnNuevo.grid(column=0,row=12, padx=10, pady=5 )

        self.btnGuardar = tk.Button(self.scrollable_frame, text="Guardar", command=self.guardarPaciente)
        self.btnGuardar.config(width=20, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#1658A2", cursor="hand2",activebackground="#35BD6F") # color verde es 158645
        self.btnGuardar.grid(column=1,row=12, padx=10, pady=5 )
#


        self.btnCancelar = tk.Button(self.scrollable_frame, text="Cancelar", command=self.deshabilitar)
        self.btnCancelar.config(width=20, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#1658A2", cursor="hand2",activebackground="#35BD6F") # color verde es 158645
        self.btnCancelar.grid(column=2,row=12, padx=10, pady=5 )


        self.lblBuscarRUTpaciente = tk.Label(self.scrollable_frame, text='Buscar RUT paciente:')
        self.lblBuscarRUTpaciente.config(width=20, font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblBuscarRUTpaciente.grid(column=3,row=0, padx=10, pady=5 )

        self.lblBuscarApellido = tk.Label(self.scrollable_frame, text='Buscar Apellido:')
        self.lblBuscarApellido.config(width=20, font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblBuscarApellido.grid(column=3,row=1, padx=10, pady=5 )

# ENTRYS BUSCADOR
        self.svBuscarRUTpaciente = tk.StringVar()
        self.entryBuscarRUTpaciente = tk.Entry(self.scrollable_frame, textvariable=self.svBuscarRUTpaciente, width=7)
        self.entryBuscarRUTpaciente.config(width=20, font=("ARIAL", 15))
        self.entryBuscarRUTpaciente.grid(column=4, row=0, padx=10, pady=5, columnspan=2)

        self.svBuscarApellido = tk.StringVar()
        self.entryBuscarApellido = tk.Entry(self.scrollable_frame, textvariable=self.svBuscarApellido)
        self.entryBuscarApellido.config(width=20, font=("ARIAL", 15))
        self.entryBuscarApellido.grid(column=4, row=1, padx=10, pady=5, columnspan=2)

        # Combobox para Estado
        self.svEstado = tk.StringVar()
        self.comboEstado = ttk.Combobox(self.scrollable_frame, textvariable=self.svEstado, state="readonly")
        self.comboEstado['values'] = ("Todos los pacientes", "Activos", "Inactivos")
        self.comboEstado.current(0)  # "Todos" por defecto
        self.comboEstado.config(font=("ARIAL", 12),width=25)
        self.comboEstado.grid(column=3, row=2, padx=10, pady=5, columnspan=2)

#botones buscador
        

        self.btnBuscarCondicion = tk.Button(self.scrollable_frame, text="Buscar", command = self.buscarCondicion)
        self.btnBuscarCondicion.config(width=25, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#00396F", cursor="hand2",activebackground="#5B8D8D") # color verde es 158645
        self.btnBuscarCondicion.grid(column=3,row=3, padx=10, pady=5, columnspan = 1 )

        self.btnLimpiarBuscador = tk.Button(self.scrollable_frame, text="Limpiar", command = self.limpiarBuscador)
        self.btnLimpiarBuscador.config(width=25, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#120061", cursor="hand2",activebackground="#7C6DC1") # color verde es 158645
        self.btnLimpiarBuscador.grid(column=4,row=3, padx=10, pady=5, columnspan = 1 )

        
        self.btnCalendario = tk.Button(self.scrollable_frame, text="Calendario", command = self.vistaCalendario)
        self.btnCalendario.config(width=25, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#53005B", cursor="hand2",activebackground="#C774CF") # color verde es 158645
        self.btnCalendario.grid(column=3,row=5, padx=10, pady=5, columnspan = 1 )

    def vistaCalendario(self):
        # Crear ventana emergente para el calendario
        self.topcalendario = Toplevel(self.master)
        self.topcalendario.title("FECHA NACIMIENTO")
        self.topcalendario.resizable(0, 0)
        self.topcalendario.config(bg="#CDD8FF")

        # Variable StringVar para almacenar la fecha seleccionada
        self.svCalendario = StringVar(value='01-01-1990')

        # Crear el calendario
        self.calendar = tc.Calendar(self.topcalendario, selectmode='day', year=1990, month=1, day=1, locale='es_ES',
                                    bg='#777777', fg='#FFFFFF', headersbackground='#B6DDFE', textvariable=self.svCalendario,
                                    cursor='hand2', date_pattern='dd-mm-yyyy')
        self.calendar.pack(pady=22)

        # Configurar el trace para detectar cambios en la fecha seleccionada
        self.svCalendario.trace('w', self.enviarFecha)

    def enviarFecha(self, *args):
        # Actualizar la variable svFN con la fecha seleccionada
        self.svFN.set(self.svCalendario.get())

        # Si hay una fecha seleccionada, se calcula la edad
        if len(self.calendar.get_date()) > 1:
            self.calcularEdad()

    def calcularEdad(self, *args):
        # Obtener la fecha actual
        self.fechaActual = date.today()

        # Obtener la fecha seleccionada del calendario
        self.date1 = self.calendar.get_date()

        # Convertir la fecha seleccionada en un objeto datetime
        self.conver = datetime.strptime(self.date1, "%d-%m-%Y")

        # Calcular la edad
        self.resul = self.fechaActual.year - self.conver.year
        self.resul -= ((self.fechaActual.month, self.fechaActual.day) < (self.conver.month, self.conver.day))

        # Asignar el resultado a la variable de edad
        self.svEdad.set(self.resul)



#BUTTON CALENDARIO
    def limpiarBuscador(self):
        self.svBuscarApellido.set('')  # Esto está bien porque svBuscarApellido es un StringVar
        self.svBuscarRUTpaciente.set('')  # Lo mismo para svBuscarRUTpaciente
        self.tablaPaciente()

    #def buscarCondicion(self):
       # if len(self.svBuscarRUTpaciente.get()) > 0 or len(self.svBuscarApellido.get()) > 0:
          #  where = "WHERE 1=1"
           # if(len(self.svBuscarRUTpaciente.get())) > 0:
            #    where = "WHERE RUTpaciente = " + self.svBuscarRUTpaciente.get() + "" #WHERE RUTpaciente = 5678
           # if (len(self.svBuscarApellido.get())) > 0:
              #  where = "WHERE ApellidoPaterno LIKE'" + self.svBuscarApellido.get()+"%' AND activo = 1"

           # self.tablaPaciente(where)
       # else:
         #   self.tablaPaciente()




    def buscarCondicion(self):
        estado = self.svEstado.get()  # Nuevo: Estado seleccionado en el Combobox
        where = "WHERE 1=1"  # Empezamos siempre así para agregar condiciones después

        rut = self.svBuscarRUTpaciente.get()
        apellido = self.svBuscarApellido.get()

        if estado == "Activos":
            where += " AND activo = 1"
        elif estado == "Inactivos":
            where += " AND activo = 0"
    # Si es "Todos", no ponemos condición de activo

        if len(rut) > 0:
            if len(rut) >= 3:
                where += f" AND RUTpaciente LIKE '{rut[:3]}%'"
            else:
                where += f" AND RUTpaciente LIKE '{rut}%'"

        if len(apellido) > 0:
            where += f" AND (ApellidoPaterno LIKE '{apellido}%' OR ApellidoMaterno LIKE '{apellido}%')"

        consulta = f"SELECT * FROM Paciente {where}"

    # Aquí ejecutarías la consulta
        print("Consulta generada:", consulta)

    # Ejemplo real de ejecución:
    # conexion = ConexionDB()
    # cursor = conexion.cursor
    # cursor.execute(consulta)
    # resultados = cursor.fetchall()

        self.tablaPaciente(where)
    def habilitar(self):
        #self.idPersona = None
        self.svRUTpac.set('')
        self.svNombres.set('')
        self.svApPaterno.set('')
        self.svApMaterno.set('')
        self.svSexo.set('')
        self.svFN.set('')
        self.svEdad.set('')
        self.svEstCi.set('')
        self.svDireccionac.set('')
        self.svCreencia.set('')
        self.svIngresad.set('')
        self.svAnt.set('')

        self.entryRUTpac.config(state='normal')
        self.entryNombres.config(state='normal')
        self.entryApPaterno.config(state='normal')
        self.entryApMaterno.config(state='normal')
        self.entrySexo.config(state='normal')
        self.entryFN.config(state='normal')
        self.entryEdad.config(state='normal')
        self.entryEstCi.config(state='normal')
        self.entryDireccionac.config(state='normal')
        self.entryCreencia.config(state='normal')
        self.entryIngresad.config(state='normal')
        self.entryAnt.config(state='normal')

        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')
        self.btnCalendario.config(state='normal')
    
    def deshabilitar(self):
        #self.idPersona = None
        self.svRUTpac.set('')
        self.svNombres.set('')
        self.svApPaterno.set('')
        self.svApMaterno.set('')
        self.svSexo.set('')
        self.svFN.set('')
        self.svEdad.set('')
        self.svEstCi.set('')
        self.svDireccionac.set('')
        self.svCreencia.set('')
        self.svIngresad.set('')
        self.svAnt.set('')

        self.entryRUTpac.config(state='disable')
        self.entryNombres.config(state='disable')
        self.entryApPaterno.config(state='disable')
        self.entryApMaterno.config(state='disable')
        self.entrySexo.config(state='disable')
        self.entryFN.config(state='disable')
        self.entryEdad.config(state='disable')
        self.entryEstCi.config(state='disable')
        self.entryDireccionac.config(state='disable')
        self.entryCreencia.config(state='disable')
        self.entryIngresad.config(state='disable')
        self.entryAnt.config(state='disable')

        self.btnGuardar.config(state='disable')
        self.btnCancelar.config(state='disable')
        self.btnCalendario.config(state='disable')

    def tablaPaciente(self, where=""):

        if len(where) > 0:
            self.listaPersona = listarCondicion(where)
        else:
            self.listaPersona =listar()
            #self.listaPersona.reverse()

        self.tabla = ttk.Treeview(self.scrollable_frame, columns=['RUTpac', 'Nombres', 'ApPaterno', 'ApMaterno', 'Sexo', 'FN', 'Edad', 'EstCi', 'Direccionac', 'Creencia', 'Ingresad', 'Ant'], height=5)
        self.tabla.grid(column= 0, row=14, columnspan=11, sticky='nse')
        self.scroll = ttk.Scrollbar(self.scrollable_frame, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=10, column=14, sticky='nse') #olumn 12 porque son 11 datos se suma 1
        
        self.tabla.configure(yscrollcommand=self.scroll.set)
        
        self.tabla.tag_configure('evenrow', background='#C5EAFE') # c
        
        self.tabla.heading('#0', text= 'RUTpac')
        self.tabla.heading('#1', text= 'Nombres')
        self.tabla.heading('#2', text= 'ApPaterno')
        self.tabla.heading('#3', text= 'ApMaterno')
        self.tabla.heading('#4', text= 'Sexo')
        self.tabla.heading('#5', text= 'FN')
        self.tabla.heading('#6', text= 'Edad')
        self.tabla.heading('#7', text= 'EstCi')
        self.tabla.heading('#8', text= 'Direccionact')
        self.tabla.heading('#9', text= 'Creencia')
        self.tabla.heading('#10', text= 'Ingresad')
        self.tabla.heading('#11', text= 'Ant')

        self.tabla.column("#0", anchor=W, width=150)
        self.tabla.column("#1", anchor=W, width=150)
        self.tabla.column("#2", anchor=W, width=75)
        self.tabla.column("#3", anchor=W, width=75)
        self.tabla.column("#4", anchor=W, width=50)
        self.tabla.column("#5", anchor=W, width=100)
        self.tabla.column("#6", anchor=W, width=100)
        self.tabla.column("#7", anchor=W, width=100)
        self.tabla.column("#8", anchor=W, width=100)
        self.tabla.column("#9", anchor=W, width=100)
        self.tabla.column("#10", anchor=W, width=200)
        self.tabla.column("#11", anchor=W, width=100)

        for p in self.listaPersona:
            self.tabla.insert('', 0,text=p[0], values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11]), tags=('evenrow', ))

        self.btnEditarpaciente = tk.Button(self.scrollable_frame, text='Editar Paciente', command=self.editarPaciente)
        self.btnEditarpaciente.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#1E0075', activebackground='#9379E0', cursor='hand2')
        self.btnEditarpaciente.grid(row=15, column=0, padx=10, pady=5)

        self.btnEliminarpaciente = tk.Button(self.scrollable_frame, text='Eliminar paciente', command=self.eliminarDatoPaciente)
        self.btnEliminarpaciente.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#8A0000', activebackground='#D58A8A', cursor='hand2')
        self.btnEliminarpaciente.grid(row=15, column=1, padx=10, pady=5)

        self.btnHistorialpaciente = tk.Button(self.scrollable_frame, text='Historial paciente', command=self.historiaMedica)
        self.btnHistorialpaciente.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#007C79', activebackground='#99F2F0', cursor='hand2')
        self.btnHistorialpaciente.grid(row=15, column=2, padx=10, pady=5)

        self.btnDatosApoderado = tk.Button(self.scrollable_frame, text='Datos Apoderado', command=self.datosApoderado)#, command=self.historiaMedica)
        self.btnDatosApoderado.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#007C79', activebackground='#99F2F0', cursor='hand2')
        self.btnDatosApoderado.grid(row=15, column=3, padx=10, pady=5)

        


        self.btnSalir = tk.Button(self.scrollable_frame, text='Salir', command=self.root.destroy) #para que cierre el raiz, la raiz es la ingterfaz principal comando
        self.btnSalir.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#000000', activebackground='#5E5E5E', cursor='hand2')
        self.btnSalir.grid(row=12, column=3, padx=10, pady=5)


    def historiaMedica(self):
        try:
        # 1) Validar que haya una fila seleccionada
            selection = self.tabla.selection()
            if not selection:
                messagebox.showerror("Error", "Por favor, selecciona un paciente.")
                return  # <— ahora sí está dentro del if

        # 2) Extraer y asignar el RUT del paciente
            self.RUTpaciente = self.tabla.item(selection, 'text')
            self.RUTpacienteHistoria = self.RUTpaciente

        # 3) Crear la ventana de historial
            self.topHistoriaMedica = Toplevel()
            self.topHistoriaMedica.title('HISTORIAL MEDICO')
            self.topHistoriaMedica.resizable(0, 0)
            self.topHistoriaMedica.config(bg='#CDD8FF')
               
        
            self.listaHistoria = listarHistoria(self.RUTpaciente)
            if not self.listaHistoria:
                print(f"No se encontraron historias médicas para el RUT: {self.RUTpaciente}")

    

            self.tablaHistoria = ttk.Treeview(self.topHistoriaMedica, column=('Apellidos', 'Fecha Historia', 'Diagnostico', 'Examenes', 'Tratamiento Farmacologico', 'Observaciones'))
            self.tablaHistoria.grid(row=0, column=0, columnspan=7, sticky='nse')

            self.scrollHistoria = ttk.Scrollbar(self.topHistoriaMedica, orient='vertical', command=self.tablaHistoria.yview)
            self.scrollHistoria.grid(row=0, column=8, sticky='nse')

            self.tablaHistoria.configure(yscrollcommand=self.scrollHistoria.set)
            self.tablaHistoria.tag_configure('evenrow', background='#C5EAFE')

            self.topHistoriaMedica.grid_rowconfigure(0, weight=1)  # Asegura que la fila 0 se expanda
            self.topHistoriaMedica.grid_columnconfigure(0, weight=1) 

            self.topHistoriaMedica.grid_rowconfigure(0, weight=1) 

            self.tablaHistoria.heading('#0', text='ID') 
            self.tablaHistoria.heading('#1', text='Apellidos')
            self.tablaHistoria.heading('#2', text='Fecha y hora')
            self.tablaHistoria.heading('#3', text='Diagnostico')
            self.tablaHistoria.heading('#4', text='Examenes')
            self.tablaHistoria.heading('#5', text='Tratamiento Farmacologico')
            self.tablaHistoria.heading('#6', text='Observaciones')

            self.tablaHistoria.column('#0', anchor=W, width=50)
            self.tablaHistoria.column('#1', anchor=W, width=100)
            self.tablaHistoria.column('#2', anchor=W, width=120)
            self.tablaHistoria.column('#3', anchor=W, width=100)
            self.tablaHistoria.column('#4', anchor=W, width=250)
            self.tablaHistoria.column('#5', anchor=W, width=250)
            self.tablaHistoria.column('#6', anchor=W, width=500)
            
            for p in self.listaHistoria: 
                self.tablaHistoria.insert('','0',text=p[0], values=(p[1], p[2], p[3], p[4], p[5],p[6]))

            self.btnGuardarHistoria = tk.Button(self.topHistoriaMedica, text='Agregar Historia', command=self.topAgregarHistoria)
            self.btnGuardarHistoria.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', 
                                        bg='#002771', cursor='hand2', activebackground='#C70039')
            self.btnGuardarHistoria.grid(row=2, column=0, padx=10, pady=5)

            
            self.btnEditarHistoria = tk.Button(self.topHistoriaMedica, text='Editar Historia', command=self.topEditarHistorialMedico)
            self.btnEditarHistoria.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', 
                                        bg='#002771', cursor='hand2', activebackground='#B47CD6')
            self.btnEditarHistoria.grid(row=2, column=1, padx=10, pady=5)

            self.btnEliminarHistoria = tk.Button(self.topHistoriaMedica, text='Eliminar Historia', command=self.eliminarHistorialMedico)
            self.btnEliminarHistoria.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD506', 
                                        bg='#002771', cursor='hand2', activebackground='#D8939C')
            self.btnEliminarHistoria.grid(row=2, column=2, padx=10, pady=5)

            
            self.btnSalirHistoria = tk.Button(self.topHistoriaMedica, text='Salir', command=self.salirTop)
            self.btnSalirHistoria.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD506', 
                                        bg='#000000', cursor='hand2', activebackground='#6F6F6F')
            self.btnSalirHistoria.grid(row=2, column=4, padx=10, pady=5)

        except Exception as e:
            title = 'Historia Medica'
            mensaje = f'Error al mostrar Historial: {str(e)}'
            messagebox.showerror(title, mensaje)

    def topAgregarHistoria(self):
        self.topAHistoria = Toplevel()
        self.topAHistoria.title('AGREGAR HISTORIA')
        self.topAHistoria.resizable(0,0)
        self.topAHistoria.config(bg='#CDD8FF')
        #self.topAHistoria.geometry("800x600")


        self.frameDatosHistoria = tk.LabelFrame(self.topAHistoria, bg='#CDD8FF')
        self.frameDatosHistoria.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")


        self.lblDiagnostico = tk.Label(self.frameDatosHistoria, text='Diagnóstico paciente', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF')
        self.lblDiagnostico.grid(row=0, column=0, padx=5, pady=3)   


        self.lblExamenes = tk.Label(self.frameDatosHistoria, text='Examenes paciente', width=20, font=('ARIAL', 15, 'bold'), bg='#CDD8FF')
        self.lblExamenes.grid(row=2, column=0, padx=5, pady=3)

        self.lblTratamientoFarmacologico = tk.Label(self.frameDatosHistoria, text='Tratamiento farmacologico', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF')
        self.lblTratamientoFarmacologico.grid(row=4, column=0, padx=5, pady=3)

        self.lblObservaciones = tk.Label(self.frameDatosHistoria, text='Observaciones Historia', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF')
        self.lblObservaciones.grid(row=6, column=0, padx=5, pady=3)

        #ENTRYS AGREGAR HISTORIA MEDICA
        self.svDiagnostico = tk.StringVar()
        self.Diagnostico = tk.Entry(self.frameDatosHistoria, textvariable=self.svDiagnostico, width=64, font=('ARIAL', 15))
        self.Diagnostico.grid(row=1, column=0, padx=5, pady=3, columnspan=2)

    

        self.svExamenes = tk.StringVar()
        self.Examenes = tk.Entry(self.frameDatosHistoria, textvariable=self.svExamenes, width=64, font=('ARIAL', 15))
        self.Examenes.grid(row=3, column=0, padx=5, pady=3, columnspan=2)
   
        self.svTratamientoFarmacologico = tk.StringVar()
        self.TratamientoFarmacologico = tk.Entry(self.frameDatosHistoria, textvariable=self.svTratamientoFarmacologico, width=64, font=('ARIAL', 15))
        self.TratamientoFarmacologico.grid(row=5, column=0, padx=5, pady=3, columnspan=2)

        self.svObservaciones = tk.StringVar()
        self.Observaciones = tk.Entry(self.frameDatosHistoria, textvariable=self.svObservaciones, width=64, font=('ARIAL', 15))
        self.Observaciones.grid(row=7, column=0, padx=5, pady=3, columnspan=2)
        
        

        #FRAME2
# FRAME2
        # FRAME2
        self.frameFechaHistoria = tk.LabelFrame(self.topAHistoria, bg='#CDD8FF', font=('ARIAL', 14, 'bold'))
        self.frameFechaHistoria.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

# Label de "Fecha y Hora"
        self.lblFechaHistoria = tk.Label(self.frameFechaHistoria, text='Fecha y Hora', width=20, font=('ARIAL', 15, 'bold'), bg='#CDD8FF')
        self.lblFechaHistoria.grid(row=0, column=0, padx=5, pady=3)

# Entry para la fecha y hora
        self.svFechaHistoria = tk.StringVar()
        self.entryFechaHistoria = tk.Entry(self.frameFechaHistoria, textvariable=self.svFechaHistoria, width=20, font=('ARIAL', 15))
        self.entryFechaHistoria.grid(row=0, column=1, padx=5, pady=3)

# TRAER fecha y hora actual
        self.svFechaHistoria.set(datetime.today().strftime('%d-%m-%Y %H:%M'))  # Establecer la fecha y hora actual

# Botón "Agregar Historia"

        self.btnAgregarHistoria = tk.Button(self.frameFechaHistoria, text='Agregar Historia', command=self.agregarHistorialMedico) # width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#000992', cursor='hand2', activebackground='#4E56C6')
        self.btnAgregarHistoria.grid(row=1, column=0, padx=10, pady=5)

# Botón "Salir"
        self.btnSalirAgregarHistoria = tk.Button(self.frameFechaHistoria, text='Salir', command=self.topAHistoria.destroy, width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#000000', cursor='hand2', activebackground='#646464')
        self.btnSalirAgregarHistoria.grid(row=1, column=1, padx=10, pady=5)

# Configurar las filas y columnas para que los elementos se expandan correctamente
        self.topAHistoria.grid_rowconfigure(0, weight=1)
        self.topAHistoria.grid_columnconfigure(0, weight=1)
        self.frameFechaHistoria.grid_rowconfigure(0, weight=1)
        self.frameFechaHistoria.grid_rowconfigure(1, weight=1)
        

    def agregarHistorialMedico(self):
        try: 
            if self.idHistoriaMedica is None:
            # Asegúrate de que RUTpacienteHistoria tenga un valor válido
                print(f"Guardando historia médica para RUT: {self.RUTpacienteHistoria}")
                guardarHistoria(self.RUTpacienteHistoria, self.svFechaHistoria.get(), 
                            self.svDiagnostico.get(), self.svExamenes.get(),
                            self.svTratamientoFarmacologico.get(), self.svObservaciones.get())
            self.topAHistoria.destroy()    
            self.topHistoriaMedica.destroy()
        except Exception as e:
            title = 'Agregar Historia'
            mensaje = f'Error al agregar historia médica: {str(e)}'
    



    def eliminarHistorialMedico(self):
        try:
            self.idHistoriaMedica = self.tablaHistoria.item(self.tablaHistoria.selection())['text']
            eliminarHistoria(self.idHistoriaMedica)

            self.idHistoriaMedica = None
            self.topHistoriaMedica.destroy()

        except:
            title = 'Eliminar Historia'
            mensaje = 'Error al eliminar'
            messagebox.showerror(title, mensaje)

    def topEditarHistorialMedico(self):
        try:
            seleccion = self.tablaHistoria.selection()
            if not seleccion:
                messagebox.showwarning('Editar Historia', 'Seleccione una historia médica para editar.')
                return

            self.idHistoriaMedica = self.tablaHistoria.item(seleccion)['text']
            valores = self.tablaHistoria.item(seleccion)['values']

            self.fechaHistoriaEditar = valores[1]
            self.DiagnosticoHistoriaEditar = valores[2]
            self.ExamenesHistoriaEditar = valores[3]
            self.TratamientoFarmacologicoHistoriaEditar = valores[4]
            self.ObservacionesHistoriaEditar = valores[5]

            self.topEditarHistoria = Toplevel()
            self.topEditarHistoria.title('EDITAR HISTORIA MÉDICA')
            self.topEditarHistoria.resizable(0, 0)
            self.topEditarHistoria.config(bg='#CDD8FF')

        # FRAME PRINCIPAL
            self.frameEditarHistoria = tk.LabelFrame(self.topEditarHistoria, bg='#CDD8FF')
            self.frameEditarHistoria.pack(fill='both', expand='yes', padx=20, pady=10)

        # LABELS
            tk.Label(self.frameEditarHistoria, text='Diagnóstico paciente', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF').grid(row=0, column=0, padx=5, pady=3)
            tk.Label(self.frameEditarHistoria, text='Exámenes paciente', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF').grid(row=2, column=0, padx=5, pady=3)
            tk.Label(self.frameEditarHistoria, text='Tratamiento farmacológico', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF').grid(row=4, column=0, padx=5, pady=3)
            tk.Label(self.frameEditarHistoria, text='Observaciones', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF').grid(row=6, column=0, padx=5, pady=3)

        # ENTRYS
            self.svDiagnosticopacienteEditar = tk.StringVar()
            self.entryDiagnosticopacienteEditar = tk.Entry(self.frameEditarHistoria, textvariable=self.svDiagnosticopacienteEditar, width=65, font=('ARIAL', 15))
            self.entryDiagnosticopacienteEditar.grid(row=1, column=0, padx=5, pady=3, columnspan=2)

            self.svExamenespacienteEditar = tk.StringVar()
            self.entryExamenespacienteEditar = tk.Entry(self.frameEditarHistoria, textvariable=self.svExamenespacienteEditar, width=65, font=('ARIAL', 15))
            self.entryExamenespacienteEditar.grid(row=3, column=0, padx=5, pady=3, columnspan=2)

            self.svTratamientofarmacologicoEditar = tk.StringVar()
            self.entryTratamientofarmacologicoEditar = tk.Entry(self.frameEditarHistoria, textvariable=self.svTratamientofarmacologicoEditar, width=65, font=('ARIAL', 15))
            self.entryTratamientofarmacologicoEditar.grid(row=5, column=0, padx=5, pady=3, columnspan=2)

            self.svObservacionesEditar = tk.StringVar()
            self.entryObservacionesEditar = tk.Entry(self.frameEditarHistoria, textvariable=self.svObservacionesEditar, width=65, font=('ARIAL', 15))
            self.entryObservacionesEditar.grid(row=7, column=0, padx=5, pady=3, columnspan=2)

        # FRAME FECHA
            self.frameFechaEditar = tk.LabelFrame(self.topEditarHistoria, bg='#CDD8FF')
            self.frameFechaEditar.pack(fill="both", expand="yes", padx=20, pady=10)

            tk.Label(self.frameFechaEditar, text='Fecha y hora', width=30, font=('ARIAL', 15, 'bold'), bg='#CDD8FF').grid(row=0, column=0, padx=5, pady=3)

            self.svFechaHistoriaEditar = tk.StringVar()
            self.entryFechaHistoriaEditar = tk.Entry(self.frameFechaEditar, textvariable=self.svFechaHistoriaEditar, width=30, font=('ARIAL', 15))
            self.entryFechaHistoriaEditar.grid(row=0, column=1, padx=5, pady=3)

        # ASIGNAR VALORES A LOS ENTRY
            self.svDiagnosticopacienteEditar.set(self.DiagnosticoHistoriaEditar)
            self.svExamenespacienteEditar.set(self.ExamenesHistoriaEditar)
            self.svTratamientofarmacologicoEditar.set(self.TratamientoFarmacologicoHistoriaEditar)
            self.svObservacionesEditar.set(self.ObservacionesHistoriaEditar)
            self.svFechaHistoriaEditar.set(self.fechaHistoriaEditar)

        # BOTONES
            self.btnEditarHistoriaMedica = tk.Button(self.frameFechaEditar, text='Editar Historia', command=self.editarHistoriaMedica)
            self.btnEditarHistoriaMedica.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#03005B', cursor='hand2', activebackground='#8986DA')
            self.btnEditarHistoriaMedica.grid(row=1, column=0, pady=5, padx=10)

            self.btnSalirHistoriaMedica = tk.Button(self.frameFechaEditar, text='Salir', command=self.topEditarHistoria.destroy)
            self.btnSalirHistoriaMedica.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#000000', cursor='hand2', activebackground='#676767')
            self.btnSalirHistoriaMedica.grid(row=1, column=1, pady=5, padx=10)

        except Exception as e:
            title = 'Editar Historia'
            mensaje = f'Error al editar historia: {str(e)}'
            messagebox.showerror(title, mensaje)

    def editarHistoriaMedica(self):
        try:
        # Obtener valores del formulario
            nuevo_diagnostico = self.svDiagnosticopacienteEditar.get()
            nuevos_examenes = self.svExamenespacienteEditar.get()
            nuevo_tratamiento = self.svTratamientofarmacologicoEditar.get()
            nuevas_observaciones = self.svObservacionesEditar.get()
            nueva_fecha = self.svFechaHistoriaEditar.get()

            exito = actualizarHistoriaMedica(
                self.idHistoriaMedica,
                nueva_fecha,
                nuevo_diagnostico,
                nuevos_examenes,
                nuevo_tratamiento,
                nuevas_observaciones
            )

            if exito:
                messagebox.showinfo("Editar Historia", "Cambios guardados exitosamente.")
                self.topEditarHistoria.destroy()
                self.tablaHistoriaMedica()  # refresca la tabla
            else:
                messagebox.showerror("Error", "No se pudo guardar la historia médica.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la historia médica: {e}")
    def salirTop(self):
        self.topHistoriaMedica.destroy()        


    def editarPaciente(self):
        try:
            self.RUTpaciente = self.tabla.item(self.tabla.selection())['text'] #trae el RUT
            self.Nombres = self.tabla.item(self.tabla.selection())['values'][0]
            self.ApellidoPaternoPaciente = self.tabla.item(self.tabla.selection())['values'][1]
            self.ApellidoMaternoPaciente= self.tabla.item(self.tabla.selection())['values'][2]
            self.Sexo = self.tabla.item(self.tabla.selection())['values'][3]
            self.FechanacimientoPaciente = self.tabla.item(self.tabla.selection())['values'][4]
            self.EdadPaciente = self.tabla.item(self.tabla.selection())['values'][5]
            self.Estadocivil = self.tabla.item(self.tabla.selection())['values'][6]
            self.DireccionactualPaciente = self.tabla.item(self.tabla.selection())['values'][7]
            self.Creenciareligiosa = self.tabla.item(self.tabla.selection())['values'][8]
            self.Ingresadesde = self.tabla.item(self.tabla.selection())['values'][9]
            self.AntecedentesPaciente= self.tabla.item(self.tabla.selection())['values'][10]

            self.habilitar()

            self.entryRUTpac.insert(0, self.RUTpaciente)
            self.entryNombres.insert(0, self.Nombres)
            self.entryApPaterno.insert(0, self.ApellidoPaternoPaciente)
            self.entryApMaterno.insert(0, self.ApellidoMaternoPaciente)
            self.entrySexo.insert(0, self.Sexo)
            self.entryFN.insert(0, self.FechanacimientoPaciente)
            self.entryEdad.insert(0, self.EdadPaciente)
            self.entryEstCi.insert(0, self.Estadocivil)
            self.entryDireccionac.insert(0, self.DireccionactualPaciente)
            self.entryCreencia.insert(0, self.Creenciareligiosa)
            self.entryIngresad.insert(0, self.Ingresadesde)
            self.entryAnt.insert(0, self.AntecedentesPaciente)
    
        except:
            title = 'Editar Paciente'
            mensaje = 'Error al editar paciente'
            messagebox.showerror(title, mensaje)

    def tablaHistoriaMedica(self):
        try:
        # Elimina todas las filas existentes de la tabla
            for fila in self.tablaHistoria.get_children():
                self.tablaHistoria.delete(fila)

        # Consulta actualizada a la base de datos
            self.listaHistoria = listarHistoria(self.RUTpaciente)

        # Vuelve a insertar todas las filas en la tabla
            for p in self.listaHistoria:
                self.tablaHistoria.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6]))

        except Exception as e:
            title = 'Actualizar Tabla Historia Médica'
            mensaje = f'Error al actualizar la tabla: {str(e)}'
            messagebox.showerror(title, mensaje)


    def eliminarDatoPaciente(self):
        try:
            self.RUTpaciente = self.tabla.item(self.tabla.selection())['text']
            eliminarPaciente(self.RUTpaciente)

            self.tablaPaciente()
            #self.RUTpaciente

            
        except Exception as e:
            title = 'Eliminar Paciente'
            mensaje = f'No se pudo eliminar paciente: {e}'
            messagebox.showinfo(title, mensaje)
    
    def datosApoderado(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                messagebox.showerror("Error", "Por favor, selecciona un paciente.")
                return

            self.RUTpaciente = self.tabla.item(seleccion, 'text')
            self.RUTpacienteApoderado = self.RUTpaciente

            datos_apoderado = buscarApoderadoPorPaciente(self.RUTpacienteApoderado)

            self.topApoderado = Toplevel()
            self.topApoderado.title('Apoderado')
            self.topApoderado.resizable(0, 0)
            self.topApoderado.config(bg='#F0F8FF')

            tk.Label(self.topApoderado, text="Datos del Apoderado", font=('ARIAL', 16, 'bold'), bg='#F0F8FF').grid(row=0, column=0, columnspan=2, pady=10)

            if datos_apoderado:
            # Si ya existe apoderado, mostrar tabla
                columnas = ['RUT Apoderado', 'Nombre', 'Dirección', 'Teléfono', 'Correo', 'Relación con residente']
                
                self.tablaApoderados = ttk.Treeview(self.topApoderado, columns=columnas, show='headings')
                self.tablaApoderados.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
                #tabla = ttk.Treeview(self.topApoderado, columns=columnas, show='headings')
                #tabla.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
                for col in columnas:
                    self.tablaApoderados.heading(col, text=col)
                    self.tablaApoderados.column(col, width=140, anchor='w')
                #for col in columnas:
                   # tabla.heading(col, text=col)
                   # tabla.column(col, width=140, anchor='w')
                #self.tablaApoderados.insert('', 'end', values=datos_apoderado[0:6])
                #self.tablaApoderados.insert('', 'end', text=datos_apoderado[0], values=datos_apoderado[1:7])       # Insertar los datos del apoderado
                #tabla.insert('', 'end', text=datos_apoderado[0], values=datos_apoderado[1:6])
                #self.tablaApoderados.insert('', 'end', text=datos_apoderado[0], values=datos_apoderado[0:6])
                self.tablaApoderados.insert('', 'end', text=datos_apoderado[0], values=datos_apoderado[0:])
                #self.tablaApoderados.insert('', 'end', values=datos_apoderado)
                
            # Botón para editar apoderado
                btnEditar = tk.Button(self.topApoderado, text="Editar Apoderado", command=self.editarApoderado,
                                    font=('Arial', 12), bg='#FFA500', fg='white', activebackground='#FFCC80', width=20)
                btnEditar.grid(row=2, column=0, columnspan=2, pady=10)
                #tabla.insert('', 'end', values=datos_apoderado[:6])
            else:
            # Si NO hay apoderado, mostrar formulario para agregar
                etiquetas = ['RUT Apoderado', 'Nombre', 'Dirección', 'Teléfono', 'Correo', 'Relación con residente']
                self.entriesApoderado = []

                for i, campo in enumerate(etiquetas):
                    tk.Label(self.topApoderado, text=campo + ':', font=('ARIAL', 12), bg='#F0F8FF').grid(row=i+1, column=0, sticky='e', padx=10, pady=5)
                    entry = tk.Entry(self.topApoderado, font=('ARIAL', 12), width=35)
                    entry.grid(row=i+1, column=1, padx=10, pady=5)
                    self.entriesApoderado.append(entry)

            # Botón para guardar
            btnGuardar = tk.Button(self.topApoderado, text='Guardar Apoderado', command=self.guardarNuevoApoderado,
                            font=('ARIAL', 12, 'bold'), bg='#007C79', fg='white',
                            activebackground='#5FDDE1', width=20)
            btnGuardar.grid(row=8, column=0, columnspan=2, pady=10)

        # Botón cerrar
            btnCerrar = tk.Button(self.topApoderado, text='Cerrar', command=self.topApoderado.destroy,
                            font=('ARIAL', 12, 'bold'), bg='#002771', fg='white',
                            activebackground='#4458A1', width=20)
            btnCerrar.grid(row=9, column=0, columnspan=2, pady=10)

           # btnEditar = tk.Button(self.root, text="Editar Apoderado", command=self.editarApoderado,
                           # font=('Arial', 12), bg='#FFA500', fg='white',
                      #      activebackground='#FFCC80', width=20)
            #btnEditar.grid(row=3, column=1, padx=10, pady=10)  # Ajustá posición según tu diseño

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al mostrar los datos del apoderado:\n{e}")
    
    def guardarNuevoApoderado(self):
        try:
        # Obtener datos de los campos de entrada
            datos = [entry.get().strip() for entry in self.entriesApoderado]

        # Verificar que todos los campos están completos
            if not all(datos):
                messagebox.showerror("Error", "Por favor, completa todos los campos.")
                return

        # Convertir campos numéricos
            datos[0] = int(datos[0])  # RUT apoderado
            datos[3] = int(datos[3])  # Teléfono

        # Agregar el RUT del paciente (usado previamente)
            rut_paciente = self.RUTpacienteApoderado

        # Llamar al DAO para insertar los datos en la base de datos
          

            from modelo.ApoderadoDao import guardarApoderado, Apoderado
            nuevo_apoderado = Apoderado(*datos, rut_paciente)
            guardarApoderado(nuevo_apoderado)
        # Mensaje de éxito
            messagebox.showinfo("Éxito", "Apoderado guardado correctamente.")
            self.topApoderado.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el apoderado:\n{e}")
    
    def agregarApoderado(self):
        try:
        # Asegúrate de que RUTpaciente tenga un valor válido
            print(f"Guardando apoderado para RUT: {self.RUTpacienteApoderado}")
            guardarApoderado(self.RUTpacienteApoderado, 
                            self.svNombre.get(), 
                            self.svDireccion.get(), 
                            self.svTelefono.get(), 
                            self.svCorreo.get(), 
                            self.svRelacion.get())
            self.topAgregarApoderado.destroy()    
        except Exception as e:
                title = 'Agregar Apoderado'
                mensaje = f'Error al agregar apoderado: {str(e)}'
                messagebox.showerror(title, mensaje)

 


    def guardarCambiosApoderado(self):
        try:
            RUTapoderado = self.svRUTapoderado.get()
            nombre = self.svNombreEditar.get()
            direccion = self.svDireccionEditar.get()
            telefono = self.svTelefonoEditar.get()
            correo = self.svCorreoEditar.get()
            relacion = self.svRelacionEditar.get()

        # Llamada al DAO para actualizar
              # Asegúrate de tener esto correctamente importado
            actualizarApoderado(self.idApoderado, nombre, direccion, telefono, correo, relacion)

            messagebox.showinfo('Éxito', 'Apoderado actualizado correctamente.')
            self.topEditarApoderado.destroy()
            self.mostrarApoderados()  # Refresca la tabla

        except Exception as e:
            messagebox.showerror('Error', f'No se pudo actualizar el apoderado: {str(e)}')


    def eliminarApoderado(self):
        try:
            seleccion = self.tablaApoderados.selection()
            if not seleccion:
                messagebox.showwarning('Eliminar Apoderado', 'Seleccione un apoderado para eliminar.')
                return

            self.idApoderado = self.tablaApoderados.item(seleccion)['text']

            confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar al apoderado con RUT {self.idApoderado}?")
            if confirmacion:
               eliminarApoderado(self.idApoderado)

            messagebox.showinfo("Eliminado", "Apoderado eliminado correctamente.")
            self.mostrarApoderados()

        except Exception as e:
            messagebox.showerror('Error', f'No se pudo eliminar apoderado: {str(e)}')

    def editarApoderado(self):
        try:
            seleccion = self.tablaApoderados.selection()
            if not seleccion:
                messagebox.showerror("Error", "Por favor, selecciona un apoderado para editar.")
                return

            self.idApoderado = self.tablaApoderados.item(seleccion)['text']
            datos_apoderado = buscarApoderadoPorRUT(self.idApoderado)

            if not datos_apoderado:
                messagebox.showerror("Error", "No se encontraron datos del apoderado.")
                return

            self.topEditarApoderado = Toplevel()
            self.topEditarApoderado.title("Editar")
            self.topEditarApoderado.resizable(False, False)
            self.topEditarApoderado.config(bg='#F0F8FF')

            labels = ['RUT_apoderado', 'Nombre', 'Dirección', 'Teléfono', 'Correo', 'Relación']
            variables = []

            for i, label in enumerate(labels):
                tk.Label(self.topEditarApoderado, text=label + ':', bg='#F0F8FF', font=('Arial', 12)).grid(row=i, column=0, sticky='e', padx=10, pady=5)
                var = tk.StringVar(value=datos_apoderado[i])  # Index desde 0
                entry = tk.Entry(self.topEditarApoderado, textvariable=var, font=('Arial', 12), width=30)
                entry.grid(row=i, column=1, padx=10, pady=5)
                variables.append(var)

            self.svRUTapoderado, self.svNombreEditar, self.svDireccionEditar, self.svTelefonoEditar, self.svCorreoEditar, self.svRelacionEditar = variables

            btnGuardar = tk.Button(self.topEditarApoderado, text='Guardar', command=self.guardarCambiosApoderado)
            btnGuardar.grid(row=6, column=0, columnspan=2, pady=10)

            btnSalir = tk.Button(self.topEditarApoderado, text='Salir', command=self.topEditarApoderado.destroy)
            btnSalir.grid(row=7, column=0, columnspan=2, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de edición:\n{e}")

    def mostrarApoderados(self):
    # Eliminar filas existentes en la tabla
        for fila in self.tablaApoderados.get_children():
            self.tablaApoderados.delete(fila)

    # Obtener los apoderados desde la base de datos
        apoderados = obtenerApoderados()  # Esta función debe estar definida en tu ApoderadoDao.py

    # Insertar los apoderados en la tabla
        for apoderado in apoderados:
            self.tablaApoderados.insert('', 'end', text=apoderado[0], values=apoderado[0:])
            #self.tablaApoderados.insert('', 'end', values=apoderado[0:6])