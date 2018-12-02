import sys
import unittest
sys.path.append('../')
from Blockchain.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.bc = Blockchain()
    
    def test_the_truth(self):
        self.assertTrue( True )

if __name__ == '__main__':
    unittest.main()