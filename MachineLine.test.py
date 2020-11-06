import unittest
from MachineLine import *
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
class BufferTest(unittest.TestCase):
    middle_buffer = Buffer(Buffer.Type.MIDDLE,4,"middle buffer")
    input_buffer = Buffer(Buffer.Type.INPUT,4,"input buffer")
    output_buffer = Buffer(Buffer.Type.OUTPUT,4,"output buffer")
    def test_reset(self):
        self.middle_buffer.reset()
        self.input_buffer.reset()
        self.output_buffer.reset()
        self.assertTrue(self.middle_buffer.current==0)
        self.assertFalse(hasattr(self.input_buffer,'current'))
        self.assertFalse(hasattr(self.output_buffer,'current'))

    def test_is_full(self):
        self.assertFalse(self.middle_buffer.is_full())
        for i in range(4):
            self.middle_buffer.push()
        self.assertTrue(self.middle_buffer.is_full())
        self.assertFalse(self.output_buffer.is_full())

    def test_push_pop(self):
        self.middle_buffer.reset()
        self.middle_buffer.push()
        self.assertEqual(self.middle_buffer.current,1)
        self.middle_buffer.pop()
        self.assertTrue(self.middle_buffer.is_empty())
if __name__ == '__main__':
    unittest.main()
