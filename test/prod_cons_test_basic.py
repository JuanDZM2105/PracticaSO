# Test Basic

import os
import unittest
import importlib

expected_module = 'PRODCONSMODULE'
default_module = 'pysyn'

if expected_module in os.environ:
    prod_cons_mdl = os.environ[expected_module]
else:
    prod_cons_mdl = 'pysync'

prod_cons_imprt = importlib.__import__(prod_cons_mdl, globals(), locals(), [], 0)

class TestProdConsTestBasic(unittest.TestCase):

    def test_create_default_size(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        self.assertEqual(prod_cons.size, 10)

    def test_create_specific_size_with_name(self):
        prod_cons = prod_cons_imprt.GenProdCons(size=50)
        self.assertEqual(prod_cons.size, 50)

    def test_create_specific_without_name(self):
        prod_cons = prod_cons_imprt.GenProdCons(250)
        self.assertEqual(prod_cons.size, 250)

    def test_no_put_element_get_size(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        self.assertEqual(len(prod_cons), 0)

    def test_put_one_element_get_size(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        prod_cons.put([1,2,3])
        self.assertEqual(len(prod_cons), 1)
        
    def test_put_one_element_get_it(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        element = [1,2,3]
        prod_cons.put(element)
        element_provide = prod_cons.get()
        self.assertEqual(element, element_provide)

    def test_put_several_elements_and_get_all(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        elements = [1,2,3,4,5,6,7,8,9,10]

        for e in elements:
            prod_cons.put(e)
        self.assertEqual(len(prod_cons), len(elements))

        for i in range(0,len(prod_cons)):
            e = prod_cons.get()

        self.assertEqual(len(prod_cons), 0)

