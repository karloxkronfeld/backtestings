import MetaTrader5 as meta
import pandas as pd

from pylab import *
pd.set_option('display.max_rows', None  )
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
meta.initialize()

simbolo= "EURUSD"
datos=pd.DataFrame(meta.copy_rates_from_pos(simbolo,meta.TIMEFRAME_H4,0,12000))[["time","close"]].set_index("time")
datos.index=pd.to_datetime(datos.index,unit="s")



