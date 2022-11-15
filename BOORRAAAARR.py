import MetaTrader5 as meta
import pandas as pd
from pylab import *
pd.set_option('display.width', None)
meta.initialize()

simbolo="EURUSD"
datos=pd.DataFrame(meta.copy_rates_from_pos(simbolo,meta.TIMEFRAME_H4,0,10000))[["time","close"]].set_index("time")
datos.index=pd.to_datetime(datos.index,unit="s")

mensual = figure(figsize=(20, 20))
lista_maximos, lista_minimos, lista_promedios = [], [], []
for i in range(0, 28):
    maximo = max(dia[i].ask)
    minimo = min(dia[i].bid)
    promedio = dia[i].values.mean()

    lista_maximos.append(maximo)
    lista_minimos.append(minimo)
    lista_promedios.append(promedio)

    if dia[i].precio[0] < dia[i].precio[-1]:
        color_fondo = "lightgreen"
    else:
        color_fondo = "lightcoral"

    subplot(6, 5, i + 1, frameon=True, xticks=[], yticks=[], facecolor=color_fondo)
    title(pd.to_datetime(lista_dias[i]).strftime("%d-%a"))

    plot(dia[i].values, color="k")

    text(0, maximo, "%.3f" % maximo, color="r", ha="right")  # MAXIMO DEL DIA
    hlines(maximo, 0, len(dia[i]), colors="r")
    text(0, minimo, "%.3f" % minimo, color="g", ha="right")  # MINIMO DEL DIA
    hlines(minimo, 0, len(dia[i]), colors="g")
    text(0, promedio, "%.3f" % promedio, color="b", ha="right")  # PROMEDIO DEL DIA
    hlines(promedio, 0, len(dia[i]), colors="b")

    # hlines(moda,0,len(dia[i]),colors="white",ls=":")

    text(0, dia[i].precio[0], "%.3f" % dia[i].precio[0], ha="right")  # PRECIO APERTURA
    text(len(dia[i]), dia[i].precio[-1], "%.3f" % dia[i].precio[-1], ha="left")  # PRECIO CIERRE

