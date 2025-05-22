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
    while True:
        print(f"[Producer {producer_id}] Producing value: {i}")
        prod_cons.put(i)
        i += 1
        time.sleep(sleep_time)

def consumer(prod_cons, rendezvous, number_mod, consumer_id=0, sleep_time=1.0):
    while True:
        value = prod_cons.get()
        print(f"  [Consumer {consumer_id}] Consumed: {value}")

        exchanged = rendezvous.echanger(value)
        print(f"  [Consumer {consumer_id}] After rendezvous, got: {exchanged}")

        if exchanged % number_mod == 0:
            print(f"  [Consumer {consumer_id}] Value {exchanged} is multiple of {number_mod}")

        time.sleep(sleep_time)

if __name__ == "_main_":
    prod_cons_1 = GenProdCons()
    prod_cons_2 = GenProdCons()
    rendezvous = RendezvousDEchange()

    thr_prod_1 = Thread(target=producer, args=(prod_cons_1, 1))
    thr_prod_2 = Thread(target=producer, args=(prod_cons_2, 2))

    thr_cons_1 = Thread(target=consumer, args=(prod_cons_1, rendezvous, 5000, 1))
    thr_cons_2 = Thread(target=consumer, args=(prod_cons_2, rendezvous, 3000, 2))

    thr_prod_1.start()
    thr_prod_2.start()
    thr_cons_1.start()
    thr_cons_2.start()

    thr_prod_1.join()
    thr_prod_2.join()
    thr_cons_1.join()
    thr_cons_2.join()
