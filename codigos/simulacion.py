import tkinter as tk
import numpy as np
import pandas as pd
from tkinter import font
from tkinter.constants import CENTER
from tkinter import *
from tkinter import messagebox
from pandastable import Table, TableModel, data

def regresar(simulacion,root):
    root.deiconify()
    simulacion.destroy()

def advertencia():
    messagebox.showwarning("Advertencia","Las series deben ser diferentes entre sí")

def HorasDescompostura(variables,posicion):
    horas = 0
    for i in range(0,posicion):
        horas = horas + variables[i]
    return horas

def CompararHoraMayor(descompostura, reparacion):
    return max(descompostura,reparacion)

def asignarOperarios():
    indicaciones = { "Inicio Reparacion": 0, "Reparacion Finalizada" : 0, "Ocupado" : False}
    return indicaciones

def obteniendoDatos(datos, operador):
    return datos[operador]["Inicio Reparacion"]

def tiempoDescompostura(S1,NIte, TiempoDescompostura):
    print("Generando")
    Uniformes=pd.read_csv("./series/numerosAleatoriosSeries.csv")
    Serie1=Uniformes["serie{}".format(S1)]
    Aleatorios1=Serie1[0:NIte]
    TDescompostura=["7±1","9±1","11±1","13±1","17±1","19±1"]
    ProbDescompos=[0.1,0.15,0.24,0.26,0.18,0.07]
    ProbAcum=np.cumsum(ProbDescompos)
    for i in Aleatorios1:
        if i>=0 and i<=ProbAcum[0]: #Rango 1
            TiempoDescompostura.append(7)
        elif i>ProbAcum[0] and i<=ProbAcum[1]: #Rango 2
            TiempoDescompostura.append(9)
        elif i>ProbAcum[1] and i<=ProbAcum[2]: #Rango 3
            TiempoDescompostura.append(11)
        elif i>ProbAcum[2] and i<=ProbAcum[3]: #Rango 4
            TiempoDescompostura.append(13)
        elif i>ProbAcum[3] and i<=ProbAcum[4]: #Rango 5
            TiempoDescompostura.append(17)
        elif i>ProbAcum[4] and i<=ProbAcum[5]: #Rango 6
            TiempoDescompostura.append(19)
    return TiempoDescompostura

def tiempoReparación(S2,NIte, TiempoReparacion):
    print("Generando")
    Uniformes=pd.read_csv("./series/numerosAleatoriosSeries.csv")
    Serie2=Uniformes["serie{}".format(S2)]
    Aleatorios2=Serie2[0:NIte]
    TReparacion=["3±1","5±1","7±1","9±1","11±1"]
    ProbReparacion=[0.15,0.25,0.3,0.2,0.1]
    ProbAcum2=np.cumsum(ProbReparacion)
    for i in Aleatorios2:
        if i>=0 and i<=ProbAcum2[0]: #Rango 1
            TiempoReparacion.append(3)
        elif i>ProbAcum2[0] and i<=ProbAcum2[1]: #Rango 2
            TiempoReparacion.append(5)
        elif i>ProbAcum2[1] and i<=ProbAcum2[2]: #Rango 3
            TiempoReparacion.append(7)
        elif i>ProbAcum2[2] and i<=ProbAcum2[3]: #Rango 4
            TiempoReparacion.append(9)
        elif i>ProbAcum2[3] and i<=ProbAcum2[4]: #Rango 5
            TiempoReparacion.append(11)
    return TiempoReparacion

def error2():
    messagebox.showerror("Error","Ha ocurrido un error en la visualización")
    
class DataFrameTable(tk.Frame):
    def __init__(self, parent=None, df=pd.DataFrame()):
        super().__init__()
        self.parent = parent
        self.grid(row=8,column=2,pady=10)
        # self.pack(fill=tk.BOTH, expand=True)
        self.table = Table(
            self, dataframe=df,
            showtoolbar=False,
            showstatusbar=True,
            editable=False)
        self.table.show()

def simular(simulacionFrame, NOpe, NMaq, NIte, S1, S2, txtOperarios, txtMaquinas, txtIteraciones, SpinSerie1, SpinSerie2, TiempD, TiempR, IniRep, FinRep, HoraD, TiemM):
    # frame2=Toplevel(simulacionFrame)
    # frame2.title("Gráficas")
    NOpe = int(txtOperarios.get())
    NMaq = int(txtMaquinas.get())
    NIte = int(txtIteraciones.get())
    S1 = int(SpinSerie1.get())
    S2 = int(SpinSerie2.get())
    if S1 == S2:
        advertencia()
    else:
        TiempD = tiempoDescompostura(S1,NIte, TiempD)
        TiempR = tiempoReparación(S2,NIte, TiempR)
        OP = Operario(TiempD, TiempR, NOpe, NMaq)
        OP.simular(NIte, TiempD, TiempR)
        IniRep = OP.IniRep
        FinRep = OP.FinRep
        TiemM = OP.TMuerto
        HoraD = OP.HDesc
        datos = {
            "Tiempo Descomposturas":TiempD,
            "Hora Descompostura":HoraD,
            "Tiempo Reparación":TiempR,
            "Inicio Reparación":IniRep,
            "Finaliza Reparación":FinRep,
            "Tiempo Muerto":TiemM
        }
        filas=[]
        for i in range(1,len(TiempD)+1):
            filas.append(i)
        dataframe = pd.DataFrame(datos,filas)
        pd.set_option('display.max_rows', None)
        tabla = tk.Text(simulacionFrame,width=140, bg="#272727",fg="white")
        tabla.insert(tk.INSERT, dataframe)
        tabla.pack()

        if OP.NOP == 2:
            infoOperarios = {
            "Operador #1": OP.InicioOp1,
            "Operador #2": OP.InicioOp2
            }
        elif OP.NOP == 3:
            infoOperarios = {
            "Operador #1": OP.InicioOp1,
            "Operador #2": OP.InicioOp2,
            "Operador #3": OP.InicioOp3
            }
        elif OP.NOP == 4:
            infoOperarios = {
            "Operador #1": OP.InicioOp1,
            "Operador #2": OP.InicioOp2,
            "Operador #3": OP.InicioOp3,
            "Operador #4": OP.InicioOp4
            }
        elif OP.NOP == 5:
            infoOperarios = {
            "Operador #1": OP.InicioOp1,
            "Operador #2": OP.InicioOp2,
            "Operador #3": OP.InicioOp3,
            "Operador #4": OP.InicioOp4,
            "Operador #5": OP.InicioOp5
            }
        if OP.NOP > 1:
            infoOperarios = pd.DataFrame(infoOperarios, index=filas)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            print(infoOperarios)
        # tabla = DataFrameTable(simulacionFrame,dataframe)
        # print(dataframe)
        # print(filas)
        # print(datos)
        # print(IniRep)
        # print(FinRep)

class Operario:
    def __init__(self,TiempoDescompostura,TiempoReparacion,NumOperarios,NumMaquinas):
        self.TDesc = TiempoDescompostura
        self.TRep = TiempoReparacion
        self.NOP = NumOperarios
        self.NM = NumMaquinas
        self.Ocupado = np.empty(self.NOP,dtype=bool)
        self.Ocioso = np.empty(self.NOP,dtype=int)
        self.Cont = 0
        self.IniRep = []
        self.FinRep = []
        self.TMuerto=[]
        self.HDesc=[]
        self.Estados = []
        self.Informacion = []
        self.MRep = np.empty(self.NOP,dtype=int)
        for i in range(0,self.NOP):
            self.Ocupado[i] = False
            self.Ocioso[i] = 0
            self.MRep[i] = 0
        for i in range(0,self.NOP):
            self.Ocupado[i] = False
            self.Ocioso[i] = 0
            self.MRep[i] = 0
        if NumOperarios == 2:
            self.InicioOp1 = []
            self.InicioOp2 = []
        elif NumOperarios == 3:
            self.InicioOp1 = []
            self.InicioOp2 = []
            self.InicioOp3 = []
        elif NumOperarios == 4:
            self.InicioOp1 = []
            self.InicioOp2 = []
            self.InicioOp3 = []
            self.InicioOp4 = []
        elif NumOperarios == 5:
            self.InicioOp1 = []
            self.InicioOp2 = []
            self.InicioOp3 = []
            self.InicioOp4 = []
            self.InicioOp5 = []
            
    def simular(self,iteraciones, variables1, variables2):
        for i in range(0,iteraciones):
            if self.NOP > 0 and self.NOP < 2:
                if i==0:
                    self.HDesc.append(variables1[i])
                    self.IniRep.append(variables1[i])
                    self.FinRep.append(self.IniRep[i]+variables2[i])
                    self.TMuerto.append(self.IniRep[i]-variables1[i])
                else:
                    self.HDesc.append(HorasDescompostura(variables1,i+1))
                    if(self.HDesc[i]>self.FinRep[i-1]):
                        self.FinRep.append(self.HDesc[i]+variables2[i])   
                    else:
                        self.FinRep.append(CompararHoraMayor(self.HDesc[i],self.FinRep[i-1])+variables2[i])        
                    self.IniRep.append(CompararHoraMayor(self.HDesc[i],self.FinRep[i-1]))
                    TM = abs(self.HDesc[i]-self.IniRep[i])
                    self.TMuerto.append(TM)
                    if TM > 0:
                        self.Ocupado = True
                    else:
                        self.Ocupado = False
            else:
                # print("Mas de un operario")
                IniReparacion = []
                numOperador = 0
                ocupados = 0
                ocupado = False
                operadores = {operador:asignarOperarios() for operador in range(0,self.NOP)}
                if i==0:
                    self.HDesc.append(variables1[i])
                    operadores[numOperador].update({"Inicio Reparacion":variables1[i], "Ocupado":ocupado})
                    self.Estados.append(ocupado)
                    self.IniRep.append(variables1[i])
                    self.FinRep.append(self.IniRep[i]+variables2[i])
                    operadores[numOperador].update({"Reparacion Finalizada":self.IniRep[i]+variables2[i]})
                    self.TMuerto.append(self.IniRep[i]-variables1[i])
                    # print(reparacionFinalizadaAnterior(operadores,numOperador))
                else:
                    self.HDesc.append(HorasDescompostura(variables1,i+1))
                    if self.HDesc[i]>=self.FinRep[i-1]:
                        ocupados = ocupados - 1
                        ocupado = False
                        self.Estados.append(ocupado)
                        operadores[numOperador].update({"Ocupado":ocupado})
                        self.FinRep.append(self.HDesc[i]+variables2[i])
                        operadores[numOperador].update({"Reparacion Finalizada":self.HDesc[i]+variables2[i]})
                        # print(reparacionFinalizadaAnterior(operadores,numOperador))
                    else:
                        ocupado = True
                        ocupados = ocupados + 1
                        self.Estados.append(ocupado)
                        operadores[numOperador].update({"Ocupado":ocupado})
                        numOperador = ocupados
                        self.FinRep.append(self.HDesc[i]+variables2[i])
                        operadores[numOperador].update({"Reparacion Finalizada":self.HDesc[i]+variables2[i]})
                    operadores[numOperador].update({"Inicio Reparacion":self.HDesc[i],"Ocupado":ocupado})
                    self.Estados.append(ocupado)        
                    self.IniRep.append(self.HDesc[i])
                    TM = abs(self.HDesc[i]-self.IniRep[i])
                    self.TMuerto.append(TM)
                    numOperador = ocupados
                # self.Informacion.append( obteniendoDatos(operadores,0) )
                if self.NOP == 2:
                    self.InicioOp1.append( obteniendoDatos(operadores,0) )
                    self.InicioOp2.append( obteniendoDatos(operadores,1) )
                elif self.NOP == 3:
                    self.InicioOp1.append( obteniendoDatos(operadores,0) )
                    self.InicioOp2.append( obteniendoDatos(operadores,1) )
                    self.InicioOp3.append( obteniendoDatos(operadores,2) )
                elif self.NOP == 4:
                    self.InicioOp1.append( obteniendoDatos(operadores,0) )
                    self.InicioOp2.append( obteniendoDatos(operadores,1) )
                    self.InicioOp3.append( obteniendoDatos(operadores,2) )
                    self.InicioOp4.append( obteniendoDatos(operadores,3) )
                elif self.NOP == 5:
                    self.InicioOp1.append( obteniendoDatos(operadores,0) )
                    self.InicioOp2.append( obteniendoDatos(operadores,1) )
                    self.InicioOp3.append( obteniendoDatos(operadores,2) )
                    self.InicioOp4.append( obteniendoDatos(operadores,3) )
                    self.InicioOp5.append( obteniendoDatos(operadores,4) )
                # for j, operario in enumerate(operadores):
                #     print(operadores[operario])
        # for i in range(0,len(self.TDesc)):
        #     if(i==0):
        #         self.HDesc.append(self.TDesc[i])
        #         self.IniRep.append(self.TDesc[i])
        #         self.FinRep.append(self.IniRep[i]+self.TRep[i])
        #         self.TMuerto.append(self.IniRep[i]-self.TDesc[i])
        #     else:
        #         self.HDesc.append(HorasDescompostura(self.TDesc,i+1))
        #         if(self.HDesc[i]>self.FinRep[i-1]):
        #             self.FinRep.append(self.HDesc[i]+self.TRep[i])   
        #         else:
        #             self.FinRep.append(CompararHoraMayor(self.HDesc[i],self.FinRep[i-1])+self.TRep[i])    
        #         self.IniRep.append(CompararHoraMayor(self.HDesc[i],self.FinRep[i-1]))
        #         TM = abs(self.HDesc[i]-self.IniRep[i])
        #         self.TMuerto.append(TM)

def simulacion(root,LOGO,FUENTE,BG_COLOR,PRIMARY_COLOR):
    NOpe=0
    NMaq=0
    NIte=0
    S1=0
    S2=0
    TiempoDescompostura=[]
    TiempoReparacion=[]
    InicioReparacion=[]
    FinalizaReparacion=[]
    HoraDescompostura = []
    TiempoMuerto = []
    root.withdraw()
    simulacionFrame = tk.Toplevel(root)
    simulacionFrame.title("Simulación")
    simulacionFrame.iconbitmap(LOGO+".ico")
    simulacionFrame.resizable(False,False) 
    
    frame1 = tk.Frame(simulacionFrame, width=200, height=200, bg=BG_COLOR)
    frame1.pack()

    canvas = tk.Canvas(frame1, width=700, height=300, bg=BG_COLOR)
    canvas.grid(columnspan = 6, rowspan = 24)

    txtOperarios=tk.Entry(frame1, fg="white", font=FUENTE, bg=BG_COLOR, width=5, justify=CENTER)
    txtOperarios.grid(row=0,column=3,padx=10,pady=10)

    txtMaquinas = tk.Entry(frame1, fg="white", font=FUENTE, bg=BG_COLOR, width=5, justify=CENTER)
    txtMaquinas.grid(row=1,column=3,padx=10,pady=10)

    txtIteraciones = tk.Entry(frame1, fg="white", font=FUENTE, bg=BG_COLOR, width=5, justify=CENTER)
    txtIteraciones.grid(row=2,column=3,padx=10,pady=10)

    SpinSerie1 = tk.Spinbox(frame1,from_=1,to=10,increment=1,state="readonly", font=FUENTE, bg=PRIMARY_COLOR, width=5, justify=CENTER)
    SpinSerie1.grid(row=3,column=3,padx=10,pady=10)

    SpinSerie2 = tk.Spinbox(frame1,from_=1,to=10,increment=1,state="readonly", font=FUENTE, bg=PRIMARY_COLOR, width=5, justify=CENTER)
    SpinSerie2.grid(row=4,column=3,padx=10,pady=10)

    lblOperarios = tk.Label(frame1,text="Número de operarios:", fg="white", font=FUENTE, bg=BG_COLOR)
    lblOperarios.grid(row=0,column=2,padx=10,pady=10)

    lblMaquinas = tk.Label(frame1,text="Número de máquinas:", fg="white", font=FUENTE, bg=BG_COLOR)
    lblMaquinas.grid(row=1,column=2,padx=10,pady=10)

    lbliteraciones = tk.Label(frame1,text="Número de iteraciones:", fg="white", font=FUENTE, bg=BG_COLOR)
    lbliteraciones.grid(row=2,column=2,padx=10,pady=10)

    lblSerie1 = tk.Label(frame1,text="# de serie para Descomposturas:", fg="white", font=FUENTE, bg=BG_COLOR)
    lblSerie1.grid(row=3,column=2,padx=10,pady=10)

    lblSerie2 = tk.Label(frame1,text="# de serie para Reparaciones", fg="white", font=FUENTE, bg=BG_COLOR)
    lblSerie2.grid(row=4,column=2,padx=10,pady=10)

    btnSimular = tk.Button(frame1,text="Simular",command=lambda:simular(simulacionFrame, NOpe, NMaq, NIte, S1, S2, txtOperarios, txtMaquinas, txtIteraciones, SpinSerie1, SpinSerie2, TiempoDescompostura, TiempoReparacion, InicioReparacion, FinalizaReparacion, HoraDescompostura, TiempoMuerto),fg="white", font=FUENTE, bg=PRIMARY_COLOR, width=8)
    btnSimular.grid(row=5,column=3,pady=10)

    btnRegresar = tk.Button(frame1,text="Regresar",command=lambda:regresar(simulacionFrame,root),fg="white", font=FUENTE, bg=PRIMARY_COLOR, width=8)
    btnRegresar.grid(row=5,column=2,pady=10)