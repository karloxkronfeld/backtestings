import MetaTrader5 as meta
import pandas as pd
from pylab import *
# pd.set_option('display.max_rows', None  )
# pd.set_option('display.max_columns', 500)
pd.set_option('display.width', None)
meta.initialize()

simbolo="USDJPY"
datos=pd.DataFrame(meta.copy_rates_from_pos(simbolo,meta.TIMEFRAME_H1,0,90000)).set_index("time")
datos.index=pd.to_datetime(datos.index,unit="s")


datos["body"]=datos.close-datos.open
datos["mecha_inferior"]=where(datos.body>0,datos.open-datos.low,datos.close-datos.low)
datos["mecha_superior"]=where(datos.body>0,datos.high-datos.close,datos.high-datos.open)

top10_rojas=datos.body.sort_values()[50:100].mean()
top10_verdes=datos.body.sort_values()[-100:-50].mean()

datos["signal"]=where(datos.body>top10_verdes,1,
                      where(datos.body<top10_rojas,-1,0))


rs = datos.close.apply(np.log).diff(1)

my_rs = datos.signal.shift(1)*rs
my_rs.cumsum().apply(np.exp).plot(title="Strategy Performance")
show()

