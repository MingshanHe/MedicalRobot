import math
from isaacgym import gymapi
from isaacgym import gymutil
from base import Base
from logger import Logger
from utils import *
from controller import PIDcontroller
from controller import DQN
from controller import Manifold
import os
import numpy as np
class Cancellor(Base):
    def __init__(self, _save_data_, _method_, args):
        # self.gym = None
        # self.sim = None
        # self.viewer = None
        super().__init__(_method_)
        self.save_data = _save_data_
        self.method = _method_
        self.score = 0
        self.run_scene = 0

        print(self.method)
        if self.save_data:
            self.logger = Logger(os.path.abspath('logs'))
        # np.random.seed(42)
        if self.method == "PID":
            self.controller = PIDcontroller()
        elif self.method == "RL":
            self.args = args
            self.controller = DQN(args)

            # task-specific parameters
            self.num_obs = 6  # pole_angle + pole_vel + cart_vel + cart_pos
            self.num_act = 2  # force applied on the pole (-1 to 1)
            self.reset_dist = 3.0  # when to reset
            self.max_push_effort = 400.0  # the range of force applied to the cartpole
            self.max_episode_length = 500  # maximum episode length
            # allocate buffers
            self.obs_buf = torch.zeros((self.args.num_envs, self.num_obs), device=self.args.sim_device)
            self.reward_buf = torch.zeros(self.args.num_envs, device=self.args.sim_device)
            self.reset_buf = torch.ones(self.args.num_envs, device=self.args.sim_device, dtype=torch.long)
            self.progress_buf = torch.zeros(self.args.num_envs, device=self.args.sim_device, dtype=torch.long)
        elif self.method == "MANIFOLD":
            self.controller = Manifold()
        self.points = [False, False, False, False, False]

    def create_scene(self):
        # add ground plane
        plane_params = gymapi.PlaneParams()
        self.gym.add_ground(self.sim, gymapi.PlaneParams())
        # set up the env grid
        num_envs = 1
        spacing = 1.5
        env_lower = gymapi.Vec3(-spacing, 0.0, -spacing)
        env_upper = gymapi.Vec3(spacing, 0.0, spacing)
        # add urdf asset
        asset_root = "assets"
        asset_file = "cancellor/urdf/cancellor.urdf"
        # Load asset with default control type of position for all joints
        asset_options = gymapi.AssetOptions()
        asset_options.fix_base_link = True
        asset_options.default_dof_drive_mode = gymapi.DOF_MODE_POS
        print("Loading asset '%s' from '%s'" % (asset_file, asset_root))
        cancellor_asset = self.gym.load_asset(self.sim, asset_root, asset_file, asset_options)
        
        # initial root pose for cartpole actors
        initial_pose = gymapi.Transform()
        initial_pose.p = gymapi.Vec3(0.0, 0.1, 0.0)
        initial_pose.r = gymapi.Quat(-0.707107, 0.0, 0.0, 0.707107)
        
        self.env0 = self.gym.create_env(self.sim, env_lower, env_upper, 2)
        cancellor = self.gym.create_actor(self.env0, cancellor_asset, initial_pose, 'cancellor', 0, 1)
        # Configure DOF properties
        if self.method == "PID":
            props = self.gym.get_actor_dof_properties(self.env0, cancellor)
            props["driveMode"] = (gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_POS, gymapi.DOF_MODE_POS)
            props["stiffness"] = (0.0, 0.0, 5000.0, 5000.0)
            props["damping"] = (200.0, 200.0, 100.0, 100.0)
            self.gym.set_actor_dof_properties(self.env0, cancellor, props)
        elif self.method == "RL":
            props = self.gym.get_actor_dof_properties(self.env0, cancellor)
            props["driveMode"] = (gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_VEL)
            props["stiffness"] = (0.0, 0.0, 0.0, 0.0)
            props["damping"] = (200.0, 200.0, 200.0, 200.0)
            self.gym.set_actor_dof_properties(self.env0, cancellor, props)
        elif self.method == "MANIFOLD":
            props = self.gym.get_actor_dof_properties(self.env0, cancellor)
            props["driveMode"] = (gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_VEL)
            props["stiffness"] = (0.0, 0.0, 0.0, 0.0)
            props["damping"] = (200.0, 200.0, 200.0, 200.0)
            self.gym.set_actor_dof_properties(self.env0, cancellor, props)
        # Set DOF drive targets
        self.Base_X_handle = self.gym.find_actor_dof_handle(self.env0, cancellor, 'move_x')
        self.Base_Y_handle = self.gym.find_actor_dof_handle(self.env0, cancellor, 'move_y')
        self.Tip_X_handle = self.gym.find_actor_dof_handle(self.env0, cancellor, 'tip_x')
        self.Tip_Y_handle = self.gym.find_actor_dof_handle(self.env0, cancellor, 'tip_y')

    
    def actuate_Base(self, x, y):
        self.gym.set_dof_target_velocity(self.env0, self.Base_X_handle, x)
        self.gym.set_dof_target_velocity(self.env0, self.Base_Y_handle, y)
        
    def actuate_Tip(self, x, y):
        if self.method == "PID":
            self.gym.set_dof_target_position(self.env0, self.Tip_X_handle, x) #0.003
            self.gym.set_dof_target_position(self.env0, self.Tip_Y_handle, y)
        elif self.method == "RL":
            self.gym.set_dof_target_velocity(self.env0, self.Tip_X_handle, x)
            self.gym.set_dof_target_velocity(self.env0, self.Tip_Y_handle, y)
        elif self.method == "MANIFOLD":
            self.gym.set_dof_target_velocity(self.env0, self.Tip_X_handle, x) #0.003
            self.gym.set_dof_target_velocity(self.env0, self.Tip_Y_handle, y)
        
    def desired_trajectory(self):
        # if pos >= 0.0:
        pos_x = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
        pos_y = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
        x_values, y_values, self.points = gen_base_traj(self.points, pos_x, pos_y)
        self.actuate_Base(x_values,y_values)

    def tip_trajectory(self):
        if self.method == "PID":
            pos_x = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
            pos_y = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
            x, y = self.controller.compute(self.points, pos_x, pos_y)
            self.actuate_Tip(x, y)
        elif self.method == "RL":
            self.run_step = 1
            self.epsilon = max(0.01, 0.8 - 0.01 * (self.run_step / 20))
            xb = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
            yb = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
            xt = (self.gym.get_dof_position(self.env0, self.Base_X_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_X_handle))
            yt = (self.gym.get_dof_position(self.env0, self.Base_Y_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_Y_handle))
            self.obs_buf = torch.tensor([[xb, yb, xb, yb, xt, yt]], device=self.args.sim_device)
            obs = self.obs_buf.clone()
            x, y = self.controller.compute(self.points, xb, yb, obs, self.epsilon)
            self.actuate_Tip(x, y)
            self.action = x+y
        elif self.method == "MANIFOLD":
            xb = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
            yb = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
            xt = (self.gym.get_dof_position(self.env0, self.Base_X_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_X_handle))
            yt = (self.gym.get_dof_position(self.env0, self.Base_Y_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_Y_handle))
            x, y = self.controller.compute(self.points, xb, yb, xt, yt)
            self.actuate_Tip(x, y)


    def compute_error(self):
        xb = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
        yb = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
        xt = (self.gym.get_dof_position(self.env0, self.Base_X_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_X_handle))
        yt = (self.gym.get_dof_position(self.env0, self.Base_Y_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_Y_handle))
        self.error_b, self.error_t = distance_error(self.points, xb, yb, xt, yt,self.method)
        self.reward = 1.0 - self.error_t*40
        
    
    def run(self):
        if self.method == "PID":
            self.desired_trajectory()
            self.tip_trajectory()
            self.compute_error()
        elif self.method == "RL":
            self.desired_trajectory()
            self.tip_trajectory()
            self.compute_error()
            self.controller.push(self.obs_buf, self.action, torch.tensor([self.reward],device=self.args.sim_device), self.obs_buf, torch.tensor([0],device=self.args.sim_device))
            loss = self.controller.update()
            self.score += torch.mean(torch.tensor([self.reward],device=self.args.sim_device)).item()
            if self.run_step:
                print('Steps: {:04d} | Reward {:.04f} | TD Loss {:.04f} Epsilon {:.04f} '
                      .format(self.run_step, self.score, loss.item(), self.epsilon))
                self.score = 0
        elif self.method == "MANIFOLD":
            self.desired_trajectory()
            self.tip_trajectory()
            self.compute_error()
    def loopfunc(self):
        while not self.gym.query_viewer_has_closed(self.viewer) and self.run_scene <= 20:

            self.gym.simulate(self.sim)
            self.gym.fetch_results(self.sim, True)


            
            self.run()
            if self.method == "PID":
                self.desired_trajectory()
                self.tip_trajectory()
                self.gym.step_graphics(self.sim)
                self.gym.draw_viewer(self.viewer, self.sim, True)
                self.compute_error()
            elif self.method == "RL":
                if self.points[4]:
                    self.points = [False, False, False, False, False]
                    self.reset()
                    self.run_scene += 1
                self.desired_trajectory()
                self.tip_trajectory()
                self.gym.step_graphics(self.sim)
                self.gym.draw_viewer(self.viewer, self.sim, True)
                self.compute_error()
            elif self.method == "MANIFOLD":
                self.desired_trajectory()
                self.tip_trajectory()
                self.gym.step_graphics(self.sim)
                self.gym.draw_viewer(self.viewer, self.sim, True)
                self.compute_error()
            if self.save_data:
                self.save_base_trajectory()
                self.save_tip_trajectory()
                self.save_error_trajectory()
                
            self.gym.sync_frame_time(self.sim)

        print('Done')

        self.gym.destroy_viewer(self.viewer)
        self.gym.destroy_sim(self.sim)













    def get_state_tensor(self):
        # get dof state tensor (of cartpole)
        _dof_states = self.gym.acquire_dof_state_tensor(self.sim)
        dof_states = gymtorch.wrap_tensor(_dof_states)
        dof_states = dof_states.view(self.args.num_envs, self.num_obs)
        return dof_states

    def get_obs(self, env_ids=None):
        # get state observation from each environment id
        if env_ids is None:
            env_ids = torch.arange(self.args.num_envs, device=self.args.sim_device)

        self.gym.refresh_dof_state_tensor(self.sim)
        self.obs_buf[env_ids] = self.dof_states[env_ids]
    def get_reward(self):
        self.reward_buf[:] = compute_cancellor_reward(self.dof_states, self.reset_dist, self.reset_buf, self.progress_buf, self.max_episode_length)


    def save_base_trajectory(self):
        pos_x = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
        pos_y = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
        self.logger.save_base_transition(np.array([pos_x, pos_y]))
        
    def save_tip_trajectory(self):
        pos_x = (self.gym.get_dof_position(self.env0, self.Base_X_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_X_handle))
        pos_y = (self.gym.get_dof_position(self.env0, self.Base_Y_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_Y_handle))
        self.logger.save_tip_transition(np.array([pos_x, pos_y]))
        
    def save_error_trajectory(self):
        self.logger.save_error(np.array([self.error_b, self.error_t]))
        
        
        
    # def run(self):
        

    #     # collect data

    #     self.env.step(action)
    #     next_obs, reward, done = self.env.obs_buf.clone(), self.env.reward_buf.clone(), self.env.reset_buf.clone()
    #     self.env.reset()

    #     self.replay.push(obs, action, reward, next_obs, 1 - done)

    #     # training mode
    #     if self.replay.size() > self.mini_batch_size:
    #         loss = self.update()
    #         self.score += torch.mean(reward.float()).item() / self.num_eval_freq

    #         # evaluation mode
    #         if self.run_step % self.num_eval_freq == 0:
    #             print('Steps: {:04d} | Reward {:.04f} | TD Loss {:.04f} Epsilon {:.04f} Buffer {:03d}'
    #                   .format(self.run_step, self.score, loss.item(), epsilon, self.replay.size()))
    #             self.score = 0

    #     self.run_step += 1
    
