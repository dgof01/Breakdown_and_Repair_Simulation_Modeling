import tkinter as tk

def regresar(instrucciones,root):
    root.deiconify()
    instrucciones.destroy()

def instrucciones(root,LOGO,FUENTE):
    root.withdraw()
    instrucciones = tk.Toplevel(root)
    instrucciones.title("Instrucciones de Uso")
    instrucciones.iconbitmap(LOGO+".ico")

    canvas = tk.Canvas(instrucciones, width=400, height=600)
    canvas.grid(columnspan=3, rowspan=12)

    titulo = tk.Label(instrucciones, text="Simulador GO", fg="white")
    titulo.grid(column=1, row=2 )

    textoBTN = tk.StringVar()
    btn_Iniciar = tk.Button(instrucciones, textvariable=textoBTN, command=lambda:regresar(instrucciones,root), font=FUENTE, fg="black", height=2, width=13)
    textoBTN.set("Regresar")
    btn_Iniciar.grid(column=1, row=7)