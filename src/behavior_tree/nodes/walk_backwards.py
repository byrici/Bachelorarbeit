import math
import time
from interbotix_xs_modules.hexapod import InterbotixHexapodXS

def move_forward(x_stride=-0.06, num_cycles=1, gait_type='tripod'):

    bot = InterbotixHexapodXS('pxmark4', init_node =False)
    #bot.hex.move_in_place(z=0.1)
    #bot.hex.modify_stance(-0.02)

    bot.hex.move_in_world(x_stride = x_stride, num_cycles = num_cycles, gait_type = gait_type)
    time.sleep(0.04)
    
   

if __name__=='__main__':
    move_forward()