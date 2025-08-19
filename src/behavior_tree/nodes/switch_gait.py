import math
import time
from interbotix_xs_modules.hexapod import InterbotixHexapodXS

def switch_gait(x_stride=0.06, num_cycles=1, gait_type='tripod'):

    bot = InterbotixHexapodXS('pxmark4', init_node =False)

    bot.hex.move_in_world(x_stride = x_stride, num_cycles = num_cycles, gait_type = gait_type)
    time.sleep(0.04)
    
    bot.hex.reset_hexapod('sleep')

if __name__=='__main__':
    switch_gait()