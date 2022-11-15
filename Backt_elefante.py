import MetaTrader5 as meta
import pandas as pd
from pylab import *
pd.set_option('display.width', None)
meta.initialize()
symbol="EURUSD"

datos=pd.DataFrame(meta.copy_rates_from_pos(symbol,meta.TIMEFRAME_H4,0,10000))[["time",'open', 'high', 'low', 'close']].set_index("time")
datos.index=pd.to_datetime(datos.index,unit="s")

datos["dif close-open"]=datos.close-datos.open  #CUERPO, positivas son alcistas(verdes), negativas son bajistas(rojas)

top_numero_rango=500
top_verdes=datos["dif close-open"].sort_values(ascending=False)[10:10+top_numero_rango].mean()  #quitando las mas grandes y poco rrecurrentes
top_rojas=datos["dif close-open"].sort_values(ascending=True)[10:10+top_numero_rango].mean()

datos["signal"]=where(datos["dif close-open"]>top_verdes,1,
                      where(datos["dif close-open"]<top_rojas,-1,0))

print(datos[datos.signal==1])








