import MetaTrader5 as meta
import matplotlib.pyplot as plt
import pandas as pd
from pylab import *
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



meta.initialize()


ventana= tk.Tk()
ventana.geometry("700x450")
ventana.title("-Backtest- compra (0:00), vende (8:00)")

simbolos = []
for x in meta.symbols_get():
    simbolos.append(x.name)

label_seleccione_simbolo = tk.Label(ventana,text="Seleccione un simbolo", font=("Constantia", 15)).grid(column=0,row=0)
combo_simbolos = ttk.Combobox(ventana, values=simbolos, width=10)
combo_simbolos.current(1)
combo_simbolos.grid(column=0, row=1)

def el_boton_hace():
    datos = pd.DataFrame(meta.copy_rates_from_pos(combo_simbolos.get(), meta.TIMEFRAME_H4, 0, 10000))[["time", "close"]].set_index("time")
    datos.index = pd.to_datetime(datos.index, unit="s")

    datos["signal"] = where(datos.index.hour == 0, 1,
                            where(datos.index.hour == 8, -1, 0))

    datos["retornos"] = log(datos.close).diff()
    datos["mis_retornos"] = datos.signal.shift(1) * datos.retornos
    datos["acum"] = exp(datos.mis_retornos.cumsum())

    fig = Figure(figsize=(10, 8),dpi=50)
    plot_backtest = fig.add_subplot(111)
    plot_backtest.plot(datos.acum)
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=220, y=0)

boton_backtest=tk.Button(ventana,text="INICIO",command=el_boton_hace).grid(column=0,row=6,pady=10)
ventana.mainloop()



