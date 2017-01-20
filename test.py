# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 09:45:45 2017

@author: joostbloom
"""

import unittest
import doctest
import random
import subset_count

from subset_count import load_transactions, load_outputfile
from subset_count import count_subsets_single_n, count_subsets_iterate

class TestTransaction(unittest.TestCase):
    
    def test_count_subsets_single_n(self):
        
        test_transactions = [{1,2,3,4}, {1,2,3,4}, {1,2,3,4}, {1,2,3,4}]
        outcome = {(1, 2, 3): 4, (1, 2, 4): 4, (1, 3, 4): 4, (2, 3, 4): 4}
        self.assertEqual(count_subsets_single_n(test_transactions, 2, 3), outcome)
        self.assertEqual(count_subsets_single_n(test_transactions, 3, 3), outcome)
        self.assertEqual(count_subsets_single_n(test_transactions, 5, 3), {})
        self.assertEqual(count_subsets_single_n(test_transactions, 4, 4), {(1, 2, 3, 4): 4})
        self.assertEqual(count_subsets_single_n(test_transactions, 4, 5), {})
        
        test_transactions = [{1,2,3,4}, {1,2,3,4}, {1,2,3,4}, {1,2,3}]
        outcome = {(1, 2, 3): 4, (1, 2, 4): 3, (1, 3, 4): 3, (2, 3, 4): 3}
        self.assertEqual(count_subsets_single_n(test_transactions, 2, 3), outcome)
        self.assertEqual(count_subsets_single_n(test_transactions, 3, 3), outcome)
        self.assertEqual(count_subsets_single_n(test_transactions, 5, 3), {})
        self.assertEqual(count_subsets_single_n(test_transactions, 4, 2), {(1, 2): 4, (1, 3): 4, (2, 3): 4})
        self.assertEqual(count_subsets_single_n(test_transactions, 4, 3), {(1, 2, 3): 4})
        self.assertEqual(count_subsets_single_n(test_transactions, 4, 4), {})
        self.assertEqual(count_subsets_single_n(test_transactions, 4, 5), {})
        
        test_transactions = [{1,2,3,4}, {1,2,3,0}, {1,2,4,6}, {1,2,3,4,5,6}]
        self.assertEqual(count_subsets_single_n(test_transactions, 2, 3), {(1, 2, 3): 3,
                                                                      (1, 2, 4): 3,
                                                                      (1, 2, 6): 2,
                                                                      (1, 3, 4): 2,
                                                                      (1, 4, 6): 2,
                                                                      (2, 3, 4): 2,
                                                                      (2, 4, 6): 2})
        self.assertEqual(count_subsets_single_n(test_transactions, 3, 3), {(1, 2, 3): 3, (1, 2, 4): 3})
        self.assertEqual(count_subsets_single_n(test_transactions, 4, 3), {})
        self.assertEqual(count_subsets_single_n(test_transactions, 4, 2), {(1, 2): 4})
        
    def test_iterate_combination_count(self):
        
        test_transactions = [{2,3,4}, {2,3,0,4}, {2,6,3}, {2,3,4,5,6}]
        self.assertEqual(count_subsets_iterate(test_transactions, 3, 2), 
                         {(2, 3): 4, (2, 3, 4): 3, (2, 4): 3, (3, 4): 3})
        self.assertEqual(count_subsets_iterate(test_transactions, 3, 3), 
                         {(2, 3, 4): 3})
        self.assertEqual(count_subsets_iterate(test_transactions, 3, 4), 
                         {})
        self.assertEqual(count_subsets_iterate(test_transactions, 4, 2), 
                         {(2, 3): 4})
        
    def test_output(self):
        n_tests = 25
        transactions = load_transactions('retail_25k.dat')
        subsets = load_outputfile('output.txt')
        
        n=0
        while n<n_tests:
            test_subset = random.choice(subsets.keys())

            cnt = 0
            for transaction in transactions:
                if set(test_subset).issubset(transaction):
                    cnt += 1

            self.assertEqual(cnt, subsets[test_subset])
            n+=1
            
if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTransaction)
    suite.addTest(doctest.DocTestSuite(subset_count))
    unittest.TextTestRunner(verbosity=3).run(suite)