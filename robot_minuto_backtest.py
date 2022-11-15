import tkinter as tk
from tkinter import ttk
import MetaTrader5 as mt5
from pylab import *
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

mis_simbolos_test = ["EURUSD", "AUDUSD", "AUDJPY", "EURJPY", "CHFJPY", "CADJPY", "USDJPY"]
mt5.initialize()


def backtest_consola():

    def _quit():  # para cerrar luego
        ventana.quit()
        ventana.destroy()

    ventana = tk.Tk()
    ventana.geometry("800x450")
    ventana.title("Backtest, robot_minutos")

    simbolos = []
    for x in mt5.symbols_get():
        simbolos.append(x.name)

    label_seleccione_simbolo = tk.Label(ventana, text="Seleccione un simbolo").grid(column=0, row=0)

    combo_simbolos = ttk.Combobox(ventana, values=simbolos, width=10)
    combo_simbolos.current(1)
    combo_simbolos.grid(column=0, row=1)

    label_seleccione_entrada = tk.Label(ventana, text="Minuto Entrada").grid(column=0, row=2)
    combo_min_entrada = ttk.Combobox(ventana, values=list(range(0, 60, 5)), width=2)
    combo_min_entrada.current(0)
    combo_min_entrada.grid(column=0, row=3)
    label_seleccione_salida = tk.Label(ventana, text="Minuto Cierre").grid(column=0, row=4)
    combo_min_cierre = ttk.Combobox(ventana, values=list(range(0, 60, 5)), width=2)
    combo_min_cierre.current(9)
    combo_min_cierre.grid(column=0, row=5)

    def el_boton_hace():
        data = pd.DataFrame(
            mt5.copy_rates_from_pos(combo_simbolos.get(), mt5.TIMEFRAME_M5, 0, 50000)[["time", "close"]]).set_index(
            "time")
        data.index = pd.to_datetime(data.index, unit='s')
        fechas = data.index

        minuto_entrada = str(combo_min_entrada.get())
        minuto_cierre = str(combo_min_cierre.get())

        data["signal"] = np.where(fechas.strftime("%M") == minuto_entrada, 1,  ###compra
                                  np.where(fechas.strftime("%M") == minuto_cierre, -1, 0))  ###venta

        signal = data.close * data.signal
        posicion = signal.apply(np.sign)
        retornos = data.close.apply(np.log).diff()
        mis_retornos = (posicion.shift(1) * retornos)
        plot_returns = round(mis_retornos.cumsum().apply(np.exp) * 100, 2)

        fig,ax=subplots()
        plot_returns.plot(ax=ax)
        text(data.index[-1],plot_returns.values[-1],plot_returns.values[-1])
        ax.spines['right'].set_visible(False)





        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().place(x=140, y=0)

    boton_backtest = tk.Button(ventana, text="INICIO", command=el_boton_hace).grid(column=0, row=6, pady=10)

    ventana.protocol("WM_DELETE_WINDOW", _quit)
    ventana.mainloop()


backtest_consola()


