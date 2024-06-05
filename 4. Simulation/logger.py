import time
import os
import datetime
import numpy as np
class Logger():
    def __init__(self, logging_directory):
        timestamp = time.time()
        timestamp_value = datetime.datetime.fromtimestamp(timestamp)
        self.base_directory = os.path.join(logging_directory, timestamp_value.strftime('%Y-%m-%d.%H:%M:%S'))
        print('Creating data logging session: %s' % (self.base_directory))
        self.transitions_directory = os.path.join(self.base_directory, 'transitions')
        if not os.path.exists(self.transitions_directory):
            os.makedirs(os.path.join(self.transitions_directory))
            
            
    def save_base_transition(self, transition):
        with open(os.path.join(self.transitions_directory, 'base_transition.txt'), 'a') as f:
            np.savetxt(f, transition.reshape(1, -1), delimiter=',')
            
    def save_tip_transition(self, transition):
        with open(os.path.join(self.transitions_directory, 'tip_transition.txt'), 'a') as f:
            np.savetxt(f, transition.reshape(1, -1), delimiter=',')
            
    def save_error(self, error):
        with open(os.path.join(self.transitions_directory, 'error.txt'), 'a') as f:
            np.savetxt(f, error.reshape(1, -1), delimiter=',')