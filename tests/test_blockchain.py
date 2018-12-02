import sys
import unittest
sys.path.append('../')
from Blockchain.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.bc = Blockchain()
    
    def test_the_truth(self):
        self.assertTrue( True )

    def test_new_transaction(self):
        val = self.bc.new_transaction('sender','recipient','amount')
        self.assertGreater( val, 0 )

if __name__ == '__main__':
    unittest.main()