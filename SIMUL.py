from FORMULAE import *

def setup(seg):
    return seg.rad(), seg.indices()[0], seg.indices()[1] - seg.indices()[0]

def accelerate_from_rest(dx_list):
    v = 0

    accel_list = []
    for dx in dx_list:
        v = travel(v, accel_x(v, 0), dx)
        accel_list.append(v)
    
    return accel_list

def negotiate_turns(seg, dx_list):
    r, shift, span = setup(seg)
    v = seg.aps()

    apex_speed_list = [1000] * len(dx_list)
    v_f = v
    for i in range(shift, len(dx_list)):
        if i <= shift + span:
            apex_speed_list[i] = v
        else:
            v_f = travel(v_f, accel_x(v, 0), dx_list[i])
            apex_speed_list[i] = v_f
    
    v_b = v
    for i in range(shift - 1, -1, -1):
        v_b = travel(v_b, accel_x(v, 0), dx_list[i])
        apex_speed_list[i] = v_b
    
    return apex_speed_list
