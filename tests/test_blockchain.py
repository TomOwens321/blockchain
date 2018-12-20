import sys
import unittest
sys.path.append('../')
from Blockchain.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.bc = Blockchain(testing=True)
    
    def test_the_truth(self):
        self.assertTrue( True )

    def test_new_transaction(self):
        val = self.bc.new_transaction('sender','recipient','amount')
        self.assertEqual( val, 2 )

    def test_new_block(self):
        nb = self.bc.new_block(proof=4)
        self.assertEqual(nb['proof'], 4)
        self.assertEqual(nb['index'], 2)

    def test_last_block(self):
        lb = self.bc.last_block
        self.assertEqual( lb['index'], 1 )
        self.assertEqual( lb['proof'], 100 )

    def test_hash(self):
        block = {
            'f1': 1,
            'f2': 2
        }
        hash = self.bc.hash( block )
        self.assertEqual( hash, '5b1486f0e4f72e8413c26da4e967a6a43c0267e60e517cee0866084e8b484071')

    def test_valid_proof(self):
        vp = self.bc.valid_proof(1,1)
        self.assertFalse(vp)

    def test_proof_of_work(self):
        proof = self.bc.proof_of_work(100)
        self.assertEqual(proof, 888273)

    def test_register_node(self):
        node = '192.168.0.1:5000'
        self.bc.register_node( node )
        self.assertIsNotNone(self.bc.nodes)

    def test_valid_chain(self):
        nb = self.bc.new_block(proof=4)
        # self.assertTrue(self.bc.valid_chain(self.bc.chain))

if __name__ == '__main__':
    unittest.main()