import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
from codigos.instrucciones import instrucciones
from codigos.simulacion import simulacion

def crearInterfaz(BG_COLOR, PRIMARY_COLOR, LOGO):
    root = tk.Tk()
    root.title("Descompostura y Reparación")
    root.iconbitmap(LOGO+".ico")
    root.resizable(False,False)
    TITULO = Font(family="Museo Slab 500", size=15)
    FUENTE = Font(family="Museo Slab 500", size=12)

    canvas = tk.Canvas(root, width=400, height=600, bg=BG_COLOR)
    canvas.grid(columnspan=3, rowspan=12)

    titulo = tk.Label(root, text="Simulador GO", font=TITULO, bg=BG_COLOR, fg="white")
    titulo.grid(column=1, row=2 )

    logo = Image.open(LOGO+".png")
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo, bg=BG_COLOR)
    logo_label.image = logo
    logo_label.grid(columnspan=3, column=0, row=3)

    textoBTN = tk.StringVar()
    btn_Iniciar = tk.Button(root, textvariable=textoBTN, command=lambda:simulacion(root,LOGO,FUENTE,BG_COLOR,PRIMARY_COLOR), font=FUENTE, bg=PRIMARY_COLOR, fg="white", height=2, width=12)
    textoBTN.set("Iniciar")
    btn_Iniciar.grid(column=1, row=5)

    textoBTN = tk.StringVar()
    btn_Iniciar = tk.Button(root, textvariable=textoBTN,command=lambda:instrucciones(root,LOGO,FUENTE), font=FUENTE, bg=PRIMARY_COLOR, fg="white", height=2, width=13)
    textoBTN.set("Instrucciones")
    btn_Iniciar.grid(column=1, row=7)

    root.mainloop()