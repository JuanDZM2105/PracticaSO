# Test Basic

import os
import unittest
from queue import Queue
from threading import Thread
import importlib

expected_module = 'PRODCONSMODULE'
default_module = 'pysyn'

if expected_module in os.environ:
    prod_cons_mdl = os.environ[expected_module]
else:
    prod_cons_mdl = 'pysync'

prod_cons_imprt = importlib.__import__(prod_cons_mdl, globals(), locals(), [], 0)

def basic_producer(prod_cons, q, times=100):
    prod_values = []
    for i in range(0,times):
        prod_cons.put(i)
        prod_values.append(i)

    q.put(prod_values)
        
def basic_consumer(prod_cons, q, times=100):
    cons_values = []
    for i in range(0,times):
        cons_values.append(prod_cons.get())
        
    q.put(cons_values)

def generic_producer(prod_cons, q, times=100):
    values = [ 'Hola', 1.2, True, False, 2, (True, False), { 'uno' : 1 } ]
    prod_values = []
    idx = 0
    for i in range(0,times):
        prod_cons.put(values[idx])
        prod_values.append(values[idx])
        idx = (idx + 1) % len(values)

    q.put(prod_values)

class TestProdConsTestSync(unittest.TestCase):

    def test_prod_cons_all(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=basic_producer,args=(prod_cons, prod_q, 100))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 100))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join()
        cons_thr.join()
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(prod_values,cons_values)

    def test_prod_cons_size_one_hundred(self):
        prod_cons = prod_cons_imprt.GenProdCons(100)
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=basic_producer,args=(prod_cons, prod_q, 100))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 100))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join()
        cons_thr.join()
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(prod_values,cons_values)

    def test_prod_cons_size_50(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=basic_producer,args=(prod_cons, prod_q, 50))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 50))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join()
        cons_thr.join()
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(prod_values,cons_values)

    def test_prod_cons_size_50(self):
        prod_cons = prod_cons_imprt.GenProdCons(1)
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=basic_producer,args=(prod_cons, prod_q, 50))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 50))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join()
        cons_thr.join()
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(prod_values,cons_values)

    def test_prod_cons_two(self):
        prod_cons = prod_cons_imprt.GenProdCons(1)
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=basic_producer,args=(prod_cons, prod_q, 2))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 2))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join()
        cons_thr.join()
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(prod_values,cons_values)

    def test_prod_cons_generic_producer_100(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=generic_producer,args=(prod_cons, prod_q, 100))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 100))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join()
        cons_thr.join()
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(prod_values,cons_values)

    def test_prod_cons_generic_producer_100(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=generic_producer,args=(prod_cons, prod_q, 100))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 100))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join()
        cons_thr.join()
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(prod_values,cons_values)

    def test_prod_cons_generic_producer_one(self):
        prod_cons = prod_cons_imprt.GenProdCons(1)
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=generic_producer,args=(prod_cons, prod_q, 100))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 100))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join()
        cons_thr.join()
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(prod_values,cons_values)

    def test_prod_100_cons_50(self):
        prod_cons = prod_cons_imprt.GenProdCons(50)
        prod_q = Queue()
        cons_q = Queue()
        prod_thr = Thread(target=basic_producer,args=(prod_cons, prod_q, 100))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons, cons_q, 50))
        prod_thr.start()
        cons_thr.start()
        prod_thr.join(10)
        cons_thr.join(10)
        if prod_thr.is_alive():
            self.fail(msg="Producer fail")
        if cons_thr.is_alive():
            self.fail(msg="Consumer fail")
        prod_values = prod_q.get()
        cons_values = cons_q.get()
        self.assertEqual(len(prod_values),100)
        self.assertEqual(len(cons_values), 50)
