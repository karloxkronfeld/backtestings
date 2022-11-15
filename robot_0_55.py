import MetaTrader5 as meta
import pandas as pd
import datetime
import time


meta.initialize()
mis_simbolos=["EURUSD","XAUUSD"]

def Abrir_operaciones():

    for x in mis_simbolos:
        symbol = x
        request = {
            "action": meta.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "type": meta.ORDER_TYPE_BUY,
            "volume": 0.01,
            "price": meta.symbol_info_tick(symbol).ask,
            "comment": "robot_minuto",
            "type_filling": meta.ORDER_FILLING_IOC
        }

        result = meta.order_send(request)

        print("Orden Compra en {}".format(symbol))
        if result.retcode != meta.TRADE_RETCODE_DONE:
            print("ERROR: {} ".format(result.comment))

def Cerrar_operaciones():
    posiciones_abiertas = pd.DataFrame(list(meta.positions_get()),
                                       columns=meta.positions_get()[0]._asdict().keys()).set_index("symbol",
                                                                                                  drop=False)
    para_cerrar = posiciones_abiertas[posiciones_abiertas.comment == "robot_minuto"]

    for nro_ in range(len(para_cerrar)):
        symbol = para_cerrar.symbol[nro_]
        position_id = int(para_cerrar.ticket[nro_])
        request = {
            "action": meta.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,
            "type": meta.ORDER_TYPE_SELL,
            "position": position_id,
            "price": meta.symbol_info_tick(symbol).bid,
            "comment": "python script close",
            "type_filling": meta.ORDER_FILLING_IOC,
        }

        # enviamos la solicitud comercial
        result = meta.order_send(request)
        print("Se cerro la posicion #{} en {} ".format(position_id, symbol))
        if result.retcode != meta.TRADE_RETCODE_DONE:
            print("ERROR: {} ".format(result.comment))

def robot_handler( minuto_entrada=40, minuto_salida=45):

    while True:
        ahora = int(datetime.datetime.now().strftime("%M"))
        print("Ahora es el minuto:", ahora)

        if ahora == minuto_entrada:
            print("\u2663" * 20)
            print("BUENA SUERTE!!!!")
            print("\u2663" * 20)
            Abrir_operaciones()
        else:
            if minuto_entrada - ahora < 0:
                minutos_que_faltan = 60 + minuto_entrada - ahora
            else:
                minutos_que_faltan = minuto_entrada - ahora
            print("""     
          |    |    |                 
         )_)  )_)  )_)              
        )___))___))___)\            
       )____)____)_____)\\
     _____|____|____|____\\\>
-------\ Faltan {} minutos /-----------------------------------------------------------
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

""".format(minutos_que_faltan))
        if ahora == minuto_salida:
            try:

                Cerrar_operaciones()

            except:
                exit()
        time.sleep(60)

robot_handler()