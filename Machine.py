from MachineLine import MachineLineNode
from random import random

P = lambda x: random() < x

class Machine (MachineLineNode):
    
    def __init__ (self, breakdown_prob, repair_prob, upstream_buf, downstream_buf, name):
        self.up_to_down, self.down_to_up = breakdown_prob, repair_prob
        self.upstream, self.downstream = upstream_buf, downstream_buf
        super(Machine, self).__init__(name)
        
        self.reset()
    
    def reset (self):
        self.is_up = True

    def switchIs_Up(self):
        self.is_up = not self.is_up    
    def setIs_Up(self, value):
        self.is_up = value
    def getIs_Up(self):
        return self.is_up

    def is_blocked (self):
        return self.downstream.is_full() or self.upstream.is_empty()
    
    def phase_1_rand (self):
        self.work = False       # States if machine will work on time slot
        self.release = False    # States if machine will release its object on time slot
        
        if self.is_up and not self.is_blocked():
            self.is_up = not P(self.up_to_down)
            self.work = True
            self.release = self.is_up
            
        elif not self.is_up:
            self.is_up = P(self.down_to_up)
            self.work = False
            self.release = self.is_up
    
    def phase_1_manu (self):
        if self.is_up and not self.is_blocked():
            pass # Break machine?
        elif not self.is_up:
            pass # Repair machine?
    
    def phase_2 (self):
        if self.work:
            self.upstream.pop()
        if self.release:
            self.downstream.push()
    
    def setBreakdownProbability(self, value):
        self.up_to_down = value
    
    def setRepairProbability(self, value):
        self.down_to_up = value
    
    def __str__ (self):
        return f'{self.name}' + f' - {"UP" if self.is_up else "DOWN"}'
 