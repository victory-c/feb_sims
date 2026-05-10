from FORMULAE import *
from VEHICLE import *

class Segment:
    length = 0
    radius = 0
    direction = 0

    start_index = 0
    end_index = 0

    apex_speed = 0

    def __init__(self, l, r):
        self.length = l
        if r < 0:
            self.direction = -1
        elif r > 0:
            self.direction = 1
        self.radius = abs(r)
        if self.radius != 0:
            self.apex_speed = find_apex_speed(self.radius)
    
    def __len__(self):
        return self.length
    
    def rad(self):
        return self.radius

    def is_turn(self):
        return bool(self.radius)
    
    def aps(self):
        return self.apex_speed
    
    def indices(self):
        return self.start_index, self.end_index

    def set_start_index(self, i):
        self.start_index = i

    def set_end_index(self, i):
        self.end_index = i

# CLOSED = True 
# TODO: Implement logic for open tracks 



NODE_LEN = 1

# Helper Methods
def split_nodes(track): # Separating velocity tracking nodes for distance-based velocity tracking
    nodes = [0]
    track_len = 0
    for seg in track:
        seg_len = 0
        
        seg.set_start_index(len(nodes))
        
        while (seg_len < len(seg)):
            seg_len += NODE_LEN
            if (seg_len >= len(seg)):
                nodes.extend([track_len + len(seg)] * 2)
            else:
                nodes.append(track_len + seg_len)
        
        seg.set_end_index(len(nodes) - 2)
        
        track_len += len(seg)
    nodes = nodes[:-1]

    dx_list = [0]
    for i in range(1, len(nodes)):
        dx_list.append(nodes[i] - nodes[i-1])

    return nodes, dx_list