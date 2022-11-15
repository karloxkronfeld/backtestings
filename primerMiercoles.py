import MetaTrader5 as meta
import pandas as pd
pd.set_option('display.width', None)
from pylab import *
meta.initialize()

datos=pd.DataFrame(meta.copy_rates_from_pos("EURUSD",meta.TIMEFRAME_H2,0,19900))[["time","close"]].set_index("time")
datos.index = pd.to_datetime(datos.index, unit="s")

datos["yearmonth"]=datos.index.strftime("%Y-%m")
datos["fecha"]=datos.index.strftime("%Y-%m-%d")

Fechas= sort(["2022-11-02","2022-10-05","2022-08-31","2022-08-31","2022-08-31","2022-06-02","2022-05-04","2022-03-30","2022-03-02","2022-02-02","2022-01-05","2021-12-01","2021-11-03","2021-10-06","2021-09-01","2021-08-04","2021-06-30","2021-06-03","2021-05-05","2021-03-31","2021-03-03","2021-02-03","2021-01-06","2020-12-02","2020-11-04","2020-09-30","2020-09-02","2020-08-05","2020-07-01","2020-06-03","2020-05-06","2020-04-01","2020-03-04","2020-02-05","2020-01-08","2019-12-04","2019-10-30","2019-10-02","2019-09-05","2019-07-31","2019-07-03","2019-06-05",])

# FECHAS = busday_offset([datos["yearmonth"].unique()], 0, roll='forward', weekmask='Wed')[0]
# print(FECHAS)
FECHAS=Fechas
df_=[]
for y in range(len(FECHAS)):
    df_.append(datos[datos.fecha==str(FECHAS[y])])
# print(df_)
lista_maximos, lista_minimos, lista_promedios = [], [], []

for i in range(1,41):
    maximo=df_[i].close.max()
    minimo = df_[i].close.min()
    promedio = df_[i].close.mean()

    lista_maximos.append(maximo)
    lista_minimos.append(minimo)
    lista_promedios.append(promedio)

    if df_[i].close[0] < df_[i].close[-1]:
        color_fondo = "lightgreen"
    else:
        color_fondo = "lightcoral"

    subplot(4,10,i, frameon=True, xticks=[], yticks=[], facecolor=color_fondo)
    title(pd.to_datetime(FECHAS[i]).strftime("%m-%Y"))
    plot(df_[i].close)
    hlines(maximo,df_[i].index[0],df_[i].index[-1],colors="r")
    text(df_[i].index[0], maximo, "%.3f" % maximo, color="r", ha="right")  # MAXIMO DEL DIA

    hlines(minimo, df_[i].index[0],df_[i].index[-1],colors="g")
    text(df_[i].index[0], minimo, "%.3f" % minimo, color="g", ha="right")  # MINIMO DEL DIA
    # text(0, promedio, "%.3f" % promedio, color="b", ha="right")  # PROMEDIO DEL DIA
    # hlines(promedio, 0, len(df_[i]), colors="b")
for w in lista_minimos:
    print(w)
show()

#
#
#
#
#
#
#
#


