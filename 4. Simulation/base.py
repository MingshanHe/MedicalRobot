import math
from isaacgym import gymapi
from isaacgym import gymutil
class Base:
    def __init__(self, _method_):
        self.method = _method_
        self.gym = gymapi.acquire_gym()
        self.set_sim_params()
        self.create_sim()
        self.create_viewer()
        self.create_scene()

    def set_sim_params(self):
        # initialize sim
        self.sim_params = gymapi.SimParams()
        self.sim_params.substeps = 2
        self.sim_params.dt = 1./60.
        self.sim_params.physx.solver_type = 1
        self.sim_params.physx.num_position_iterations = 4
        self.sim_params.physx.num_velocity_iterations = 1
        self.sim_params.physx.num_threads = 0
        self.sim_params.physx.use_gpu = True
        self.sim_params.use_gpu_pipeline = False

    def create_sim(self):
        # initialize gym 
        self.sim = self.gym.create_sim(0,0,gymapi.SIM_PHYSX, self.sim_params)
        if self.sim is None:
            print("*** Failed to create sim")
            quit()

    def create_viewer(self):
        self.viewer = self.gym.create_viewer(self.sim, gymapi.CameraProperties())
        cam_pos = gymapi.Vec3(0, 0.5, 0.1)
        cam_target = gymapi.Vec3(0, 0, 0)
        self.gym.viewer_camera_look_at(self.viewer, None, cam_pos, cam_target)
        if self.viewer is None:
            raise ValueError('*** Failed to create viewer')
        
    def simulate(self):
        #step the physics
        self.gym.simulate(self.sim)
        self.gym.fetch_results(self.sim, True)
    
    def render(self):
        #update the viewer
        self.gym.simulate(self.sim)
        self.gym.draw_viewer(self.viewer, self.sim, True)
        self.gym.sync_frame_time(self.sim)
        
    def exit(self):
        # close the simulator
        self.gym.destroy_viewer(self.viewer)
        self.gym.destroy_sim(self.sim)