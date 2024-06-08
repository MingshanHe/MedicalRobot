from cancellor import Cancellor
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', default=None, type=str)
parser.add_argument('--port', default=None, type=int)

parser.add_argument('--sim_device', type=str, default="cuda:0", help='Physics Device in PyTorch-like syntax')
parser.add_argument('--num_envs', default=1, type=int)
parser.add_argument('--save_data', default=True)
parser.add_argument('--method', default='RL', type=str)
args = parser.parse_args()



def main():
    cancellor = Cancellor(_save_data_=True,_method_="MANIFOLD",args=args)
    cancellor.loopfunc()

        
if __name__ == '__main__':
    main()
