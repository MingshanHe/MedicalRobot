import numpy as np
import math
import torch
import collections
import random

class ReplayBuffer:
    def __init__(self, buffer_limit=int(1e6), num_envs=1):
        self.buffer=collections.deque(maxlen=buffer_limit)
        self.num_envs=num_envs
    def push(self, obs, action, reward, next_obs, done):
        if not torch.is_tensor(action):
            action = torch.tensor([[0]],device='cuda')
        self.buffer.append(tuple([obs, action, reward, next_obs, done]))
    
    def sample(self, mini_batch_size):
        obs, action, reward, next_obs, done = zip(*random.sample(self.buffer, mini_batch_size))
        rand_idx = torch.randperm(mini_batch_size*self.num_envs) #random shuffle tensors
        obs = torch.cat(obs)[rand_idx]

        action = torch.cat(action)[rand_idx]
        reward = torch.cat(reward)[rand_idx]
        next_obs = torch.cat(next_obs)[rand_idx]
        done = torch.cat(done)[rand_idx]
        return obs, action, reward, next_obs, done
    def size(self):
        return len(self.buffer)

def gen_base_traj(pointsList, x, y):
    std = 0.1
    if (not pointsList[0]) and (x >= -0.08) :
        x_values = -0.1
        # x_values = np.random.normal(-0.1, std, 1)
        y_values = np.random.normal( 0.0, std, 1)
        if x_values >= 0: x_values = -0.01
        return x_values, y_values, pointsList
    elif (not pointsList[1]) and (y >=-0.04):
        pointsList[0] = True
        x_values = np.random.normal( 0.0, std, 1)
        # y_values = np.random.normal(-0.1, std, 1)
        y_values = -0.1
        if y_values >= 0: y_values = -0.01
        return x_values, y_values, pointsList
    elif (not pointsList[2]) and (x <=0.08):
        pointsList[1] = True
        x_values = 0.1
        # x_values = np.random.normal(0.1, std, 1)
        y_values = np.random.normal(0.0, std, 1)
        if x_values <= 0: x_values = 0.01
        return x_values, y_values, pointsList
    elif (not pointsList[3]) and  (y >=-0.08):
        pointsList[2] = True
        x_values = np.random.normal( 0.0, std, 1)
        # y_values = np.random.normal(-0.1, std, 1)
        y_values = -0.1
        if y_values >= 0: y_values = -0.01
        return x_values, y_values, pointsList
    elif (not pointsList[4]) and (x >=-0.08):
        pointsList[3] = True
        x_values = -0.1
        # x_values = np.random.normal(-0.1, std, 1)
        y_values = np.random.normal( 0.0, std, 1)
        if x_values >= 0: x_values = -0.01
        return x_values, y_values, pointsList
    else:
        pointsList[4] = True
        x_values = 0
        y_values = 0
        return x_values, y_values, pointsList
    
def distance_error(pointsList, xb, yb, xt, yt, method):
    if method == "PID":
        if (not pointsList[0]) and (xb >= -0.08) :
            error_b = math.sqrt((yb-0)**2)
            error_t = math.sqrt((yt-0)**2)
            return error_b, error_t
        elif (not pointsList[1]) and (yb >=-0.04):
            error_b = math.sqrt((xb+0.08)**2)
            error_t = math.sqrt((xt+0.08)**2)
            return error_b, error_t
        elif (not pointsList[2]) and (xb <=0.08):
            error_b = math.sqrt((yb+0.04)**2)
            error_t = math.sqrt((yt+0.04)**2)
            return error_b, error_t
        elif (not pointsList[3]) and  (yb >=-0.08):
            error_b = math.sqrt((xb-0.08)**2)
            error_t = math.sqrt((xt-0.08)**2)
            return error_b, error_t
        elif (not pointsList[4]) and (xb >=-0.08):
            error_b = math.sqrt((yb+0.08)**2)
            error_t = math.sqrt((yt+0.08)**2)
            return error_b, error_t
        else:
            error_b = 0
            error_t = 0
            return error_b, error_t
    elif method == "RL":
        if (not pointsList[0]) and (xb >= -0.08) :
            error_b = math.sqrt((yb-0)**2)
            error_t = math.sqrt((yt-0)**2)# + math.sqrt((xt-xb)**2)
            return error_b, error_t
        elif (not pointsList[1]) and (yb >=-0.04):
            error_b = math.sqrt((xb+0.08)**2)
            error_t = math.sqrt((xt+0.08)**2)# + math.sqrt((yt-yb)**2)
            return error_b, error_t
        elif (not pointsList[2]) and (xb <=0.08):
            error_b = math.sqrt((yb+0.04)**2)
            error_t = math.sqrt((yt+0.04)**2)#+ math.sqrt((xt-xb)**2)
            return error_b, error_t
        elif (not pointsList[3]) and  (yb >=-0.08):
            error_b = math.sqrt((xb-0.08)**2)
            error_t = math.sqrt((xt-0.08)**2)#+ math.sqrt((yt-yb)**2)
            return error_b, error_t
        elif (not pointsList[4]) and (xb >=-0.08):
            error_b = math.sqrt((yb+0.08)**2)
            error_t = math.sqrt((yt+0.08)**2)#+ math.sqrt((xt-xb)**2)
            return error_b, error_t
        else:
            error_b = 0
            error_t = 0
            return error_b, error_t