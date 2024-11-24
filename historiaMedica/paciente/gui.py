import tkinter as tk
from tkinter import *
from tkinter import Button, ttk, scrolledtext, Toplevel
from modelo.pacienteDao import Persona, obtenerPacientePorRUT, guardarDatoPaciente, listarCondicion, listar, verificarRUTExistente, actualizarDatoPaciente, eliminarPaciente
from tkinter import messagebox
import tkcalendar as tc 
from tkcalendar import *
from tkcalendar import Calendar
from datetime import datetime, date
from tkinter import StringVar

class Frame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1200, height=720)
        self.root = root
        self.pack()
        self.config(bg="#CDD8FF")
        self.RUTpaciente = None
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

    def camposPaciente(self):
        #LABELS
        self.lblRUTpac = tk.Label(self, text="RUT paciente")
        self.lblRUTpac.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblRUTpac.grid(column=0,row=0, padx=10, pady=5)

        self.lblNombres = tk.Label(self, text="Nombres: ")
        self.lblNombres.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblNombres.grid(column=0, row=1, padx=10, pady=5)
    
        self.lblApPaterno = tk.Label(self, text="Apellido Paterno:")
        self.lblApPaterno.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblApPaterno.grid(column=0,row=2, padx=10, pady=5)

        self.lblApMaterno = tk.Label(self, text="Apellido Materno:")
        self.lblApMaterno.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblApMaterno.grid(column=0,row=3, padx=10, pady=5)

        self.lblSexo = tk.Label(self, text="Sexo:")
        self.lblSexo.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblSexo.grid(column=0,row=4, padx=10, pady=5)

        self.lblFN = tk.Label(self, text="Fecha nacimiento:")
        self.lblFN.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblFN.grid(column=0,row=5, padx=10, pady=5)

        
        self.lblEdad = tk.Label(self, text="Edad:")
        self.lblEdad.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblEdad.grid(column=0,row=6, padx=10, pady=5)

        self.lblEstCi = tk.Label(self, text="Estado Civil:")
        self.lblEstCi.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblEstCi.grid(column=0,row=7, padx=10, pady=5)

        self.lblDireccionac = tk.Label(self, text="Dirección actual:")
        self.lblDireccionac.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblDireccionac.grid(column=0,row=8, padx=10, pady=5)

        self.lblCreencia = tk.Label(self, text="Creencia religiosa:")
        self.lblCreencia.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblCreencia.grid(column=0,row=9, padx=10, pady=5)

        self.lblIngresad = tk.Label(self, text="Ingresa desde:")
        self.lblIngresad.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblIngresad.grid(column=0,row=10, padx=10, pady=5)

        self.lblAnt = tk.Label(self, text="Antecedentes:")
        self.lblAnt.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblAnt.grid(column=0,row=11, padx=10, pady=5)

#Entrys: valores
    
        self.svRUTpac = tk.StringVar()
        self.entryRUTpac = tk.Entry(self, textvariable=self.svRUTpac)
        self.entryRUTpac.config(width=50, font=("ARIAL", 15))
        self.entryRUTpac.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombres = tk.StringVar()
        self.entryNombres = tk.Entry(self, textvariable=self.svNombres)
        self.entryNombres.config(width=50, font=("ARIAL", 15))
        self.entryNombres.grid(column=1, row=1, padx=10, pady=5, columnspan=2)
        
        self.svApPaterno = tk.StringVar()
        self.entryApPaterno = tk.Entry(self, textvariable=self.svApPaterno)
        self.entryApPaterno.config(width=50, font=("ARIAL", 15))
        self.entryApPaterno.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svApMaterno = tk.StringVar()
        self.entryApMaterno = tk.Entry(self, textvariable=self.svApMaterno)
        self.entryApMaterno.config(width=50, font=("ARIAL", 15))
        self.entryApMaterno.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svSexo = tk.StringVar()
        self.entrySexo = tk.Entry(self, textvariable=self.svSexo)
        self.entrySexo.config(width=50, font=("ARIAL", 15))
        self.entrySexo.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svFN = tk.StringVar()
        self.entryFN = tk.Entry(self, textvariable=self.svFN)
        self.entryFN.config(width=50, font=("ARIAL", 15))
        self.entryFN.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        self.svEdad = tk.StringVar()
        self.entryEdad = tk.Entry(self, textvariable=self.svEdad)
        self.entryEdad.config(width=50, font=("ARIAL", 15)) #state='disabled')
        self.entryEdad.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

        self.svEstCi = tk.StringVar()
        self.entryEstCi = tk.Entry(self, textvariable=self.svEstCi)
        self.entryEstCi.config(width=50, font=("ARIAL", 15))
        self.entryEstCi.grid(column=1, row=7, padx=10, pady=5, columnspan=2)

        self.svDireccionac = tk.StringVar()
        self.entryDireccionac = tk.Entry(self, textvariable=self.svDireccionac)
        self.entryDireccionac.config(width=50, font=("ARIAL", 15))
        self.entryDireccionac.grid(column=1, row=8, padx=10, pady=5, columnspan=2)

        self.svCreencia = tk.StringVar()
        self.entryCreencia = tk.Entry(self, textvariable=self.svCreencia)
        self.entryCreencia.config(width=50, font=("ARIAL", 15))
        self.entryCreencia.grid(column=1, row=9, padx=10, pady=5, columnspan=2)

        self.svIngresad = tk.StringVar()
        self.entryIngresad = tk.Entry(self, textvariable=self.svIngresad)
        self.entryIngresad.config(width=50, font=("ARIAL", 15))
        self.entryIngresad.grid(column=1, row=10, padx=10, pady=5, columnspan=2)

        self.svAnt = tk.StringVar()
        self.entryAnt = tk.Entry(self, textvariable=self.svAnt)
        self.entryAnt.config(width=50, font=("ARIAL", 15))
        self.entryAnt.grid(column=1, row=11, padx=10, pady=5, columnspan=2)

#Buttons

        self.btnNuevo = tk.Button(self, text="Nuevo", command=self.habilitar)
        self.btnNuevo.config(width=20, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#1658A2", cursor="hand2",activebackground="#35BD6F") # color verde es 158645
        self.btnNuevo.grid(column=0,row=12, padx=10, pady=5 )

        self.btnGuardar = tk.Button(self, text="Guardar", command=self.guardarPaciente)
        self.btnGuardar.config(width=20, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#1658A2", cursor="hand2",activebackground="#35BD6F") # color verde es 158645
        self.btnGuardar.grid(column=1,row=12, padx=10, pady=5 )
#


        self.btnCancelar = tk.Button(self, text="Cancelar", command=self.deshabilitar)
        self.btnCancelar.config(width=20, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#1658A2", cursor="hand2",activebackground="#35BD6F") # color verde es 158645
        self.btnCancelar.grid(column=2,row=12, padx=10, pady=5 )


        self.lblBuscarRUTpaciente = tk.Label(self, text='Buscar RUT paciente:')
        self.lblBuscarRUTpaciente.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblBuscarRUTpaciente.grid(column=3,row=0, padx=10, pady=5 )

        self.lblBuscarApellido = tk.Label(self, text='Buscar Apellido:')
        self.lblBuscarApellido.config(font=("ARIAL", 15, "bold"), bg="#CDD8FF")
        self.lblBuscarApellido.grid(column=3,row=1, padx=10, pady=5 )

# ENTRYS BUSCADOR
        self.svBuscarRUTpaciente = tk.StringVar()
        self.entryBuscarRUTpaciente = tk.Entry(self, textvariable=self.svBuscarRUTpaciente)
        self.entryBuscarRUTpaciente.config(width=20, font=("ARIAL", 15))
        self.entryBuscarRUTpaciente.grid(column=4, row=0, padx=10, pady=5, columnspan=2)

        self.svBuscarApellido = tk.StringVar()
        self.entryBuscarApellido = tk.Entry(self, textvariable=self.svBuscarApellido)
        self.entryBuscarApellido.config(width=20, font=("ARIAL", 15))
        self.entryBuscarApellido.grid(column=4, row=1, padx=10, pady=5, columnspan=2)

#botones buscador
        

        self.btnBuscarCondicion = tk.Button(self, text="Buscar", command = self.buscarCondicion)
        self.btnBuscarCondicion.config(width=20, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#00396F", cursor="hand2",activebackground="#5B8D8D") # color verde es 158645
        self.btnBuscarCondicion.grid(column=3,row=2, padx=10, pady=5, columnspan = 1 )

        self.btnLimpiarBuscador = tk.Button(self, text="Limpiar", command = self.limpiarBuscador)
        self.btnLimpiarBuscador.config(width=20, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#120061", cursor="hand2",activebackground="#7C6DC1") # color verde es 158645
        self.btnLimpiarBuscador.grid(column=4,row=2, padx=10, pady=5, columnspan = 1 )

        
        self.btnCalendario = tk.Button(self, text="Calendario", command = self.vistaCalendario)
        self.btnCalendario.config(width=12, font=("ARIAL",12,"bold"), fg="#DAD5D6",
                                bg="#53005B", cursor="hand2",activebackground="#C774CF") # color verde es 158645
        self.btnCalendario.grid(column=3,row=4, padx=10, pady=5, columnspan = 1 )

    def vistaCalendario(self):
        # Crear ventana emergente para el calendario
        self.calendario = Toplevel(self.master)
        self.calendario.title("FECHA NACIMIENTO")
        self.calendario.resizable(0, 0)
        self.calendario.config(bg="#CDD8FF")

        # Variable StringVar para almacenar la fecha seleccionada
        self.svCalendario = StringVar(value='01-01-1990')

        # Crear el calendario
        self.calendar = tc.Calendar(self.calendario, selectmode='day', year=1990, month=1, day=1, locale='es_ES',
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

    def buscarCondicion(self):
        if len(self.svBuscarRUTpaciente.get()) > 0 or len(self.svBuscarApellido.get()) > 0:
            where = "WHERE 1=1"
            if(len(self.svBuscarRUTpaciente.get())) > 0:
                where = "WHERE RUTpaciente = " + self.svBuscarRUTpaciente.get() + "" #WHERE RUTpaciente = 5678
            if (len(self.svBuscarApellido.get())) > 0:
                where = "WHERE ApellidoPaterno LIKE'" + self.svBuscarApellido.get()+"%' AND activo = 1"

            self.tablaPaciente(where)
        else:
            self.tablaPaciente()
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

        self.tabla = ttk.Treeview(self, columns=['RUTpac', 'Nombres', 'ApPaterno', 'ApMaterno', 'Sexo', 'FN', 'Edad', 'EstCi', 'Direccionac', 'Creencia', 'Ingresad', 'Ant'])
        self.tabla.grid(column= 0, row=14, columnspan=11, sticky='nse')
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
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

        self.btnEditarpaciente = tk.Button(self, text='Editar Paciente', command=self.editarPaciente)
        self.btnEditarpaciente.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#1E0075', activebackground='#9379E0', cursor='hand2')
        self.btnEditarpaciente.grid(row=13, column=0, padx=10, pady=5)

        self.btnEliminarpaciente = tk.Button(self, text='Eliminar paciente', command=self.eliminarDatoPaciente)
        self.btnEliminarpaciente.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#8A0000', activebackground='#D58A8A', cursor='hand2')
        self.btnEliminarpaciente.grid(row=13, column=1, padx=10, pady=5)

        self.btnHistorialpaciente = tk.Button(self, text='Historial paciente')
        self.btnHistorialpaciente.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#007C79', activebackground='#99F2F0', cursor='hand2')
        self.btnHistorialpaciente.grid(row=13, column=2, padx=10, pady=5)

        self.btnSalir = tk.Button(self, text='Salir', command=self.root.destroy) #para que cierre el raiz, la raiz es la ingterfaz principal comando
        self.btnSalir.config(width=20, font=('ARIAL', 12, 'bold'), fg='#DAD5D6', bg='#000000', activebackground='#5E5E5E', cursor='hand2')
        self.btnSalir.grid(row=13, column=4, padx=10, pady=5)

     
    
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
    
       