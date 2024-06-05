import math
from isaacgym import gymapi
from isaacgym import gymutil
from base import Base
from logger import Logger
from utils import *
from controller import *
import os
import numpy as np
class Cancellor(Base):
    def __init__(self, _save_data_):
        # self.gym = None
        # self.sim = None
        # self.viewer = None
        super().__init__()
        self.save_data = _save_data_
        if self.save_data:
            self.logger = Logger(os.path.abspath('logs'))
        # np.random.seed(42)
        self.controller = PIDcontroller()

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
        
        
        # Create environment 0
        # Cart held steady using position target mode.
        # Pole held at a 45 degree angle using position target mode.
        self.env0 = self.gym.create_env(self.sim, env_lower, env_upper, 2)
        cancellor = self.gym.create_actor(self.env0, cancellor_asset, initial_pose, 'cancellor', 0, 1)
        
        # Configure DOF properties
        props = self.gym.get_actor_dof_properties(self.env0, cancellor)
        props["driveMode"] = (gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_VEL, gymapi.DOF_MODE_POS, gymapi.DOF_MODE_POS)
        props["stiffness"] = (0.0, 0.0, 5000.0, 5000.0)
        props["damping"] = (200.0, 200.0, 100.0, 100.0)
        self.gym.set_actor_dof_properties(self.env0, cancellor, props)
        # Set DOF drive targets
        self.Base_X_handle = self.gym.find_actor_dof_handle(self.env0, cancellor, 'move_x')
        self.Base_Y_handle = self.gym.find_actor_dof_handle(self.env0, cancellor, 'move_y')
        self.gym.set_dof_target_velocity(self.env0, self.Base_X_handle, 0.0)
        self.gym.set_dof_target_velocity(self.env0, self.Base_Y_handle, 0.0)
        self.Tip_X_handle = self.gym.find_actor_dof_handle(self.env0, cancellor, 'tip_x')
        self.Tip_Y_handle = self.gym.find_actor_dof_handle(self.env0, cancellor, 'tip_y')
        self.gym.set_dof_target_velocity(self.env0, self.Base_X_handle, 0.0)
        self.gym.set_dof_target_velocity(self.env0, self.Base_Y_handle, 0.0)
        cam_pos = gymapi.Vec3(0, 0.5, 0.1)
        cam_target = gymapi.Vec3(0, 0, 0)
        self.gym.viewer_camera_look_at(self.viewer, None, cam_pos, cam_target)
    
    def actuate_Base(self, x, y):
        self.gym.set_dof_target_velocity(self.env0, self.Base_X_handle, x)
        self.gym.set_dof_target_velocity(self.env0, self.Base_Y_handle, y)
        
    def actuate_Tip(self, x, y):
        self.gym.set_dof_target_position(self.env0, self.Tip_X_handle, x) #0.003
        self.gym.set_dof_target_position(self.env0, self.Tip_Y_handle, y)
        
    def desired_trajectory(self):
        # if pos >= 0.0:
        pos_x = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
        pos_y = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
        x_values, y_values, self.points = gen_base_traj(self.points, pos_x, pos_y)
        print(x_values)
        self.actuate_Base(x_values,y_values)

    def tip_trajectory(self):
        pos_x = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
        pos_y = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
        x, y = self.controller.compute(self.points, pos_x, pos_y)
        self.gym.set_dof_target_position(self.env0, self.Tip_X_handle, x)
        self.gym.set_dof_target_position(self.env0, self.Tip_Y_handle, y)

    def compute_error(self):
        xb = (self.gym.get_dof_position(self.env0, self.Base_X_handle))
        yb = (self.gym.get_dof_position(self.env0, self.Base_Y_handle))
        xt = (self.gym.get_dof_position(self.env0, self.Base_X_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_X_handle))
        yt = (self.gym.get_dof_position(self.env0, self.Base_Y_handle)) + (self.gym.get_dof_position(self.env0, self.Tip_Y_handle))
        self.error_b, self.error_t = distance_error(self.points, xb, yb, xt, yt)
    def loopfunc(self):
        while not self.gym.query_viewer_has_closed(self.viewer):

            self.gym.simulate(self.sim)
            self.gym.fetch_results(self.sim, True)

            self.gym.step_graphics(self.sim)
            self.gym.draw_viewer(self.viewer, self.sim, True)
            
            self.desired_trajectory()
            self.tip_trajectory()
            self.compute_error()
            if self.save_data:
                self.save_base_trajectory()
                self.save_tip_trajectory()
                self.save_error_trajectory()
                
            self.gym.sync_frame_time(self.sim)

        print('Done')

        self.gym.destroy_viewer(viewer)
        self.gym.destroy_sim(sim)




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