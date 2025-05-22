# Test Basic

import os
import unittest
from parameterized import parameterized
import importlib
from queue import Queue
from threading import Thread

expected_module = 'RENDEZVOUSMODULE'
default_module = 'pysyn'

if expected_module in os.environ:
    rendezvous_mdl = os.environ[expected_module]
else:
    rendezvous_mdl = 'pysync'

rendezvous_imprt = importlib.__import__(rendezvous_mdl, globals(), locals(), [], 0)

def thread(rdvs, q, val):
    q.put(rdvs.echanger(val))

class TestProdConsTestSync(unittest.TestCase):

    @parameterized.expand([1,2,3,4,5,6,7,8,9,10])
    def test_set_pair_threads(self, times):
        
        rdvs_array = [None] * times
        for i in range(0, times):
            rdvs_array[i] = rendezvous_imprt.RendezvousDEchange()
        
        thread_info = [ None ] * times * 2
        for i in range(0, times * 2):
            thread_info[i] = { 'thread' : None, 'queue' : None, 'val' : None}
            thread_info[i]['queue'] = Queue()
            thread_info[i]['val'] = i
            thread_info[i]['thread'] = Thread(target=thread, args=(rdvs_array[i // 2], thread_info[i]['queue'], thread_info[i]['val']))

        for i in range(0, times * 2):
            thread_info[i]['thread'].start()

        for i in range(0, times * 2):
            thread_info[i]['thread'].join(10)
            if thread_info[i]['thread'].is_alive():
                self.fail(f"Thread: {i} has a timeout")

        for i in range(0, times):
            thr_val_1 = thread_info[i * 2]['queue'].get()
            thr_val_2 = thread_info[i * 2 + 1]['queue'].get()
            self.assertNotEqual(thr_val_1, thread_info[i * 2]['val'])
            self.assertNotEqual(thr_val_2, thread_info[i * 2 + 1]['val'])

    @parameterized.expand([1,2,3,4,5,6,7,8,9,10])
    def test_set_pair_swap_values(self, times):
        
        rdvs_array = [None] * times
        for i in range(0, times):
            rdvs_array[i] = rendezvous_imprt.RendezvousDEchange()
        
        thread_info = [ None ] * times * 2
        for i in range(0, times * 2):
            thread_info[i] = { 'thread' : None, 'queue' : None, 'val' : None}
            thread_info[i]['queue'] = Queue()
            thread_info[i]['val'] = i
            thread_info[i]['thread'] = Thread(target=thread, args=(rdvs_array[i // 2], thread_info[i]['queue'], thread_info[i]['val']))

        for i in range(0, times * 2):
            thread_info[i]['thread'].start()

        for i in range(0, times * 2):
            thread_info[i]['thread'].join(10)
            if thread_info[i]['thread'].is_alive():
                self.fail(f"Thread: {i} has a timeout")

        for i in range(0, times):
            thr_val_1 = thread_info[i * 2]['queue'].get()
            thr_val_2 = thread_info[i * 2 + 1]['queue'].get()
            self.assertEqual(thr_val_1, thread_info[i * 2 + 1]['val'])
            self.assertEqual(thr_val_2, thread_info[i * 2]['val'])
    
