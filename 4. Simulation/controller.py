# from cancellor import Cancellor
from utils import ReplayBuffer

import torch.distributions
import torch.nn as nn
import torch.nn.functional as F

import autograd.numpy as anp
import pymanopt
import pymanopt.manifolds
import pymanopt.optimizers

class PIDcontroller():
    def __init__(self):
        self.P = 1
        self.I = 0
        self.D = 0
        
    def compute(self, pointsList, xb, yb):
        if (not pointsList[0]) and (xb >= -0.08) :
            error = -(yb-0)
            return 0, self.P*error
        elif (not pointsList[1]) and (yb >=-0.04):
            error = -(xb+0.08)
            return self.P*error, 0
        elif (not pointsList[2]) and (xb <=0.08):
            error = -(yb+0.04)
            return 0, self.P*error
        elif (not pointsList[3]) and  (yb >=-0.08):
            error = -(xb-0.08)
            return self.P*error, 0
        elif (not pointsList[4]) and (xb >=-0.08):
            error = -(yb+0.08)
            return 0, self.P*error
        else:
            return 0,0

class Manifold():
    def __init__(self):
        dim = 2
        self.manifold = pymanopt.manifolds.Sphere(dim)
    def compute(self, pointsList, xb, yb, xt, yt):
        x0 = 0
        y0 = 0
        if (not pointsList[0]) and (xb >= -0.08) :
            x0 = xb
            y0 = 0
        elif (not pointsList[1]) and (yb >=-0.04):
            x0 = -0.08
            y0 = yb
        elif (not pointsList[2]) and (xb <=0.08):
            x0 = xb
            y0 = -0.04
        elif (not pointsList[3]) and  (yb >=-0.08):
            x0 = 0.08
            y0 = yb
        elif (not pointsList[4]) and (xb >=-0.08):
            x0 = xb
            y0 = -0.08
        else:
            return 0,0
        # matrix = anp.array([[xb,yb,0],[xt,yt,0],[x0,y0,0]])
        matrix = anp.array([[xt,x0],[yb,y0]])

        matrix = 0.5 * (matrix + matrix.T)

        @pymanopt.function.autograd(self.manifold)
        def cost(point):
            return -point @ matrix @ point

        problem = pymanopt.Problem(self.manifold, cost)
        optimizer = pymanopt.optimizers.SteepestDescent()
        result = optimizer.run(problem)
        mapto = 0.02
        if xt > x0:
            x = -abs(result.point[0]*mapto)
        else:
            x= abs(result.point[0]*mapto)
        if yt > y0:
            y = -abs(result.point[1]*mapto)
        else:
            y = abs(result.point[1]*mapto)
        return x, y
class Net(nn.Module):
    def __init__(self, num_obs = 6, num_act = 4):
        super(Net, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(num_obs, 256),
            nn.LeakyReLU(),
            nn.Linear(256,256),
            nn.LeakyReLU(),
            nn.Linear(256, num_act)
        )
    def forward(self, x):
        return self.net(x)
    
def soft_update(net, net_target, tau):
    for param_target, param in zip(net_target.parameters(), net.parameters()):
        param_target.data.copy_(param_target.data*tau+param.data*(1.0-tau))
        
        
class DQN():
    def __init__(self, args):
        self.args = args
        self.replay = ReplayBuffer(num_envs=args.num_envs)
        
        
        self.act_space = 4  # we discretise the action space into multiple bins (should be at least 2)
        self.discount = 0.99
        self.mini_batch_size = 1
        self.batch_size = self.args.num_envs * self.mini_batch_size
        self.tau = 0.995
        self.num_eval_freq = 100
        self.lr = 3e-4

        self.run_step = 1
        self.score = 0

        # define Q-network
        self.q        = Net(num_act=self.act_space).to(self.args.sim_device)
        self.q_target = Net(num_act=self.act_space).to(self.args.sim_device)
        soft_update(self.q, self.q_target, tau=0.0)
        self.q_target.eval()
        self.optimizer = torch.optim.Adam(self.q.parameters(), lr=self.lr)
        
    def update(self):
        #policy update using TD loss
        self.optimizer.zero_grad()
        
        obs, act, reward, next_obs, done_mask = self.replay.sample(self.mini_batch_size)
        q_table = self.q(obs)
        
        act = torch.round((0.5 * (act + 1)) * (self.act_space - 1))  # maps back to the prediction space
        q_val = q_table[torch.arange(self.batch_size), act.long()]

        with torch.no_grad():
            q_val_next = self.q_target(next_obs).reshape(self.batch_size, -1).max(1)[0]

        target = reward #+ self.discount * q_val_next * done_mask
        loss = F.smooth_l1_loss(q_val, target)

        loss.backward()
        self.optimizer.step()

        # soft update target networks
        soft_update(self.q, self.q_target, self.tau)
        return loss

    def act(self, obs, epsilon=0.0):
        coin = torch.rand(self.args.num_envs, device=self.args.sim_device) < epsilon
        rand_act = torch.rand(self.args.num_envs, device=self.args.sim_device)
        with torch.no_grad():
            q_table = self.q(obs)
            true_act = torch.cat([(q_table[b] == q_table[b].max()).nonzero(as_tuple=False)[0] for b in range(self.args.num_envs)])
            true_act = true_act / (self.act_space - 1)
        act = coin.float() * rand_act + (1 - coin.float()) * true_act
        return 2 * (act - 0.5)  # maps to -1 to 1
    def compute(self, pointsList, xb, yb, obs, epsilon=0.0):
        coin = torch.rand(self.args.num_envs, device=self.args.sim_device) < epsilon
        rand_act = torch.rand(self.args.num_envs, device=self.args.sim_device)
        with torch.no_grad():
            q_table = self.q(obs)
            true_act = torch.cat([(q_table[b] == q_table[b].max()).nonzero(as_tuple=False)[0] for b in range(self.args.num_envs)])
            true_act = true_act / (self.act_space - 1)
        act = coin.float() * rand_act + (1 - coin.float()) * true_act
        mapto = 0.1
        # return 0,1
        if (not pointsList[0]) and (xb >= -0.08) :
            return 0, mapto * (act - 0.5) 
        elif (not pointsList[1]) and (yb >=-0.04):
            return mapto * (act - 0.5) , 0
        elif (not pointsList[2]) and (xb <=0.08):
            return 0, mapto * (act - 0.5) 
        elif (not pointsList[3]) and  (yb >=-0.08):
            return mapto * (act - 0.5) , 0
        elif (not pointsList[4]) and (xb >=-0.08):
            return 0, mapto * (act - 0.5) 
        else:
            return 0,0
        
    def push(self, obs, action, reward, next_obs, done):
        self.replay.push(obs, action, reward, next_obs, done)
