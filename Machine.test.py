import unittest
from Machine import *
from Buffer import *
class MachineTest(unittest.TestCase):
    """Test des fonctions de la classe Machine"""
    upstream_buff = Buffer(Buffer.Type.MIDDLE,4,"upstream buffer")
    downstream_buff = Buffer(Buffer.Type.MIDDLE,4,"downstream buffer")
    machine = Machine(0.5,0.5,upstream_buff,downstream_buff,"machine")
    def test_reset(self):
        self.machine.reset()
        self.assertTrue(self.machine.is_up)

    def test_is_blocked(self):
        self.assertTrue(self.machine.is_blocked())
        """On débloque la machine en ajoutant des pièces dans les buffeurs suivant et précedents"""
        self.upstream_buff.push()
        self.assertFalse(self.machine.is_blocked())
    def test_phase_1_rand(self):
        self.machine.phase_1_rand()
        self.assertTrue(self.machine.release==self.machine.is_up)
        self.assertTrue(self.machine.work)
        
        self.machine.reset()
        self.upstream_buff.reset()
        self.machine.phase_1_rand()
        self.assertFalse(self.machine.work)
        self.assertFalse(self.machine.release)

    def test_phase_2(self):
        self.machine.reset()
        self.upstream_buff.reset()
        self.downstream_buff.reset()
        self.upstream_buff.push()
        self.machine.phase_1_rand()
        self.machine.phase_2()
        self.assertTrue(self.upstream_buff.is_empty())
        self.assertTrue(self.downstream_buff.is_empty()!=self.machine.release)

if __name__ == '__main__':
    unittest.main()
