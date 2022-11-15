import MetaTrader5 as meta
import pandas as pd
from pylab import *

meta.initialize()

simbolo="XAUUSD"
datos=pd.DataFrame(meta.copy_rates_from_pos(simbolo,meta.TIMEFRAME_H4,0,1000))[["time","close"]].set_index("time")
datos.index=pd.to_datetime(datos.index,unit="s")
prices=datos

rs = prices.apply(np.log).diff(1)
w1 = 5 # short-term moving average window
w2 = 22 # long-term moving average window
ma_x = prices.rolling(w1).mean() - prices.rolling(w2).mean()

pos = ma_x.apply(np.sign) # +1 if long, -1 if short
print(pos)

fig, ax = plt.subplots(2,1)
ma_x.plot(ax=ax[0], title='Moving Average Cross-Over')
pos.plot(ax=ax[1], title='Position')

my_rs = pos.shift(1)*rs
my_rs.cumsum().apply(np.exp).plot(title="Strategy Performance")
show()

