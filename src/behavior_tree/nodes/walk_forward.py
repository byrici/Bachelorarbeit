import math
import time
from interbotix_xs_modules.hexapod import InterbotixHexapodXS

class HexapodWrapper:
    def __init__(self, robot_name='pxmark4', init_node=False):
        self.bot = InterbotixHexapodXS(robot_name, init_node=init_node)
        self.bot.hex.move_in_place(z=0.1)
        self.bot.hex.modify_stance(-0.02)

    def move_forward(self, x_stride=0.06, num_cycles=1, gait_type='tripod'):
        self.bot.hex.move_in_world(x_stride = x_stride, num_cycles = num_cycles, gait_type = gait_type)
        time.sleep(0.04)

    def rotate(self, yaw_stride=0.1):
        self.bot.hex.move_in_world(yaw_stride = yaw_stride, num_cycles = 1, gait_type = 'tripod')
        time.sleep(0.04)
    
    def shutdown(self):
        self.bot.hex.reset_hexapod('sleep')
