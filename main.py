from threading import Thread
import importlib
import os

expected_module = 'PRODCONSMODULE'
default_module = 'pysyn'

if expected_module in os.environ:
    prod_cons_mdl = os.environ[expected_module]
else:
    prod_cons_mdl = 'pysync'

prod_cons_imprt = importlib.__import__(prod_cons_mdl, globals(), locals(), [], 0)

def producer(prod_cons):
    i = 0
    while True:
        prod_cons.put(i)
        i = i + 1

def consumer(prod_cons,rendevouz,number_mod):
    while True:
        i = prod_cons.get(i)

if __main__ == "main":
    prod_cons_1 = GenProdCons()
    prod_cons_2 = GenProdCons()
    rendezvous  = RendezvousDEchange
    thr_prod_1 = Thread(target = producer, args=(prod_cons_1))
    thr_prod_2 = Thread(target = producer, args=(prod_cons_2))
    thr_cons_1 = Thread(target = consumer, args=(prod_cons_1, rendezvous, 5000))
    thr_cons_2 = Thread(target = consumer, args=(prod_cons_2, rendezvous, 3000))
    thr_prod_1.join()
    thr_prod_2.join()
    thr_cons_1.join()
    thr_cons_2.join()
