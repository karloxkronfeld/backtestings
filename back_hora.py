import MetaTrader5 as meta
import pandas as pd
from pylab import *

meta.initialize()

simbolo="XAUUSD"
datos=pd.DataFrame(meta.copy_rates_from_pos(simbolo,meta.TIMEFRAME_H4,0,10000))[["time","close"]].set_index("time")
datos.index=pd.to_datetime(datos.index,unit="s")

datos["signal"]=where(datos.index.hour==0,1,
                where(datos.index.hour==8,-1,0))

datos["retornos"]=log(datos.close).diff()
datos["mis_retornos"]=datos.signal.shift(1)*datos.retornos
datos["acum"]=exp(datos.mis_retornos.cumsum())
datos.acum.plot()
show()
