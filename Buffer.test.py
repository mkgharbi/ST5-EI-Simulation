import unittest
from Buffer import *
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
