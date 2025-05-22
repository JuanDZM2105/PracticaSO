import os
from threading import Thread
import importlib
import time

expected_module = 'PRODCONSMODULE'
default_module = 'pysync'

if expected_module in os.environ:
    prod_cons_mdl = os.environ[expected_module]
else:
    prod_cons_mdl = default_module

prod_cons_imprt = importlib.__import__(prod_cons_mdl, globals(), locals(), [], 0)
GenProdCons = prod_cons_imprt.GenProdCons
RendezvousDEchange = prod_cons_imprt.RendezvousDEchange

def producer(prod_cons, producer_id=0, sleep_time=0.5):
    i = 0
    while i < 10:
        print(f"[Producer {producer_id}] Produciendo valor: {i}")
        prod_cons.put(i)
        i += 1
        time.sleep(sleep_time)

def consumer(prod_cons, rendezvous, number_mod, log, consumer_id=0, sleep_time=1.0):
    for _ in range(10):
        value = prod_cons.get()
        log.append(f"[Consumer {consumer_id}] Consumió valor: {value}")

        exchanged = rendezvous.echanger(value)

        # Condición: solo intercambiar si uno es múltiplo del otro (y ninguno es cero para evitar división por cero)
        can_exchange = False
        if value != 0 and exchanged % value == 0:
            can_exchange = True
        elif exchanged != 0 and value % exchanged == 0:
            can_exchange = True

        if can_exchange:
            log.append(f"[Consumer {consumer_id}] Condición cumplida, intercambio hecho: recibió {exchanged}")
            final_value = exchanged
        else:
            log.append(f"[Consumer {consumer_id}] Condición no cumplida, mantiene valor original: {value}")
            final_value = value

        if final_value % number_mod == 0:
            log.append(f"[Consumer {consumer_id}] Valor {final_value} es múltiplo de {number_mod}")

        time.sleep(sleep_time)

if __name__ == "__main__":
    log = []

    prod_cons_1 = GenProdCons()
    prod_cons_2 = GenProdCons()
    rendezvous = RendezvousDEchange()

    thr_prod_1 = Thread(target=producer, args=(prod_cons_1, 1))
    thr_prod_2 = Thread(target=producer, args=(prod_cons_2, 2))
    thr_cons_1 = Thread(target=consumer, args=(prod_cons_1, rendezvous, 5000, log, 1))
    thr_cons_2 = Thread(target=consumer, args=(prod_cons_2, rendezvous, 3000, log, 2))

    thr_prod_1.start()
    thr_prod_2.start()
    thr_cons_1.start()
    thr_cons_2.start()

    thr_prod_1.join()
    thr_prod_2.join()
    thr_cons_1.join()
    thr_cons_2.join()

    print("\n--- Registro de eventos (log) ---")
    for entry in log:
        print(entry)