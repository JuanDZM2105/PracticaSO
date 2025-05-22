# Test Basic

import os
import unittest
import importlib

expected_module = 'RENDEZVOUSMODULE'
default_module = 'pysyn'

if expected_module in os.environ:
    rendezvous_mdl = os.environ[expected_module]
else:
    rendezvous_mdl = 'pysync'

rendezvous_imprt = importlib.__import__(rendezvous_mdl, globals(), locals(), [], 0)

class TestProdConsTestBasic(unittest.TestCase):

    def test_create_default_size(self):
        rendezvous = rendezvous_imprt.RendezvousDEchange()
        self.assertNotEqual(rendezvous, None)
