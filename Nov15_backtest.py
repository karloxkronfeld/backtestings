import MetaTrader5 as meta
import pandas as pd
from pylab import *

meta.initialize()

simbolo= "XAUUSD"
datos=pd.DataFrame(meta.copy_rates_from_pos(simbolo,meta.TIMEFRAME_M5,0,90000))[["time","close"]].set_index("time")
datos.index=pd.to_datetime(datos.index,unit="s")



datos["signal"] = np.where(datos.index.strftime("%M")==str(45),1,
                           np.where(datos.index.strftime("%M")== str(20),-1,0))
#
# fig, ax = subplots(2,1)
# datos.close.plot(ax=ax[0])
# datos.signal.plot(ax=ax[1])


rs = datos.close.apply(np.log).diff(1)
my_rs = datos.signal.shift(1)*rs
my_rs.cumsum().apply(np.exp).plot(title="Strategy Performance")
show()



print(datos)