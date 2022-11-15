import MetaTrader5 as mt5
import numpy as np
import pandas as pd
from pylab import *

mt5.initialize()

symbol=[]
get_simbolos=mt5.symbols_get()
for los_simbo in get_simbolos:
    symbol.append(los_simbo.name)

symbol=symbol[:20]


data = []
top_rojas=[]
top_verdes=[]


df_close=pd.DataFrame()
df_signal=pd.DataFrame()
for x in range(len(symbol)):

    # print(symbol[x])
    data.append(pd.DataFrame(mt5.copy_rates_from_pos(symbol[x], mt5.TIMEFRAME_H4, 0, 5000)).set_index("time")[["open","close"]])
    data[x].index = pd.to_datetime(data[x].index, unit='s')
    data[x]["body"] = data[x].close - data[x].open

    top_rojas.append(data[x].body.sort_values()[100:200].mean())
    top_verdes.append(data[x].body.sort_values()[-200:-100].mean())

    data[x]["signal"]=where(data[x].body>top_verdes[x],1,
                            where(data[x].body<top_rojas[x],-1,0))
    df_close[symbol[x]]=data[x].close
    df_signal[symbol[x]]=data[x].signal

signal=df_signal*df_close
retornos_simbolos = df_close[symbol].apply(np.log).diff()
retornos_simbolos_acum= retornos_simbolos.cumsum().apply(np.exp)

mis_retornos = signal.shift(1) * retornos_simbolos
mis_retornos_acum= mis_retornos.cumsum().apply(np.exp)*100

# fig, (ax1,ax2) = plt.subplots(2, 1)
# mis_retornos_acum.plot(ax=ax1)
# retornos_simbolos_acum.plot(ax=ax2)

mis_retornos_acum.plot()
show()


