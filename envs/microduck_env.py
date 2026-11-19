from pathlib import Path
import time
import math

import mujoco
import mujoco.viewer

import yaml

class MicroDuckEnv:

    def __init__(self, xml_path=None, config_path=None):
        """Class Constructor."""

        ## load xml files
        if xml_path is None:
            xml_path = Path(__file__).parent.parent / "tests" / "fixtures" / "toy_assets"  / "scene.xml" # TODO: need to fix

        self.model = mujoco.MjModel.from_xml_path(str(xml_path))
        self.data = mujoco.MjData(self.model)

        ## Simulation settings
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "environmental.yaml"
            
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        self.control_freq = cfg["control_freq"]
        self.action_scale = cfg["action_scale"]
        self.episode_seconds = cfg["episode_seconds"]

        # (1 / control_freq) s per policy, (model.opt.timestep) s per step
        ratio = (1 / self.control_freq) / self.model.opt.timestep # steps per policy
        if not math.isclose(ratio, round(ratio), rel_tol=1e-6):
            raise ValueError(
                f"Invalid decimation: {ratio}. "
                "Control frequency must be compatible with physics timestep."
            )
        
        self.decimation = round(ratio)

        # control_freq: number of policy steps per second,  episode_seconds: maximum duration of each episode
        self.max_policy_steps_per_episode = round(self.control_freq * self.episode_seconds) # maximum number of policy steps for each episode


        ## TODO: Store robot information


    def read_state(self):
        """Read the robot's current state from the simulation."""
        joint_angles = self.data.qpos[7:].copy()
        joint_velocities = self.data.qvel[6:].copy()
        trunk_orientation = self.data.qpos[3:7].copy()
        trunk_angular_velocity = self.data.qvel[3:6].copy()

        return joint_angles, joint_velocities, trunk_orientation, trunk_angular_velocity


    def send_command(self):
        pass


    def advance_physics(self):
        """Advance the simulation by one policy step."""
        for _ in range(self.decimation):
            mujoco.mj_step(self.model, self.data)


    def reset(self):
        pass
        

    def run_viewer(self): # run simulation for 5 seconds
        """Open the MuJoCo viewer and simulate until the window is closed."""
        with mujoco.viewer.launch_passive(self.model, self.data) as viewer:
            while viewer.is_running():
                mujoco.mj_step(self.model, self.data) # sim time += 0.002 s
                viewer.sync()                         # redraw the window
                time.sleep(self.model.opt.timestep)   # wait ~0.002 s (depends on the val set in model.opt.timestep)
        time.sleep(0.5)

    

if __name__ == "__main__":
    env = MicroDuckEnv()
    env.run_viewer()