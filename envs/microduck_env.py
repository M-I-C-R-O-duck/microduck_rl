from pathlib import Path
import time

import mujoco
import mujoco.viewer

class MicroDuckEnv:

    def __init__(self, xml_path=None):
        if xml_path is None:
            xml_path = Path(__file__).parent.parent / "tests" / "fixtures" / "toy_assets"  / "scene.xml" # TODO: need to fix

        self.model = mujoco.MjModel.from_xml_path(str(xml_path))
        self.data = mujoco.MjData(self.model)


    def run_viewer(self): # run simulation for 5 seconds
        with mujoco.viewer.launch_passive(self.model, self.data) as viewer:
            while viewer.is_running():
                mujoco.mj_step(self.model, self.data) # sim time += 0.002 s
                viewer.sync()                         # redraw the window
                time.sleep(self.model.opt.timestep)   # wait ~0.002 s (depends on the val set in model.opt.timestep)

        time.sleep(0.5)


if __name__ == "__main__":
    env = MicroDuckEnv()
    env.run_viewer()