import time
import mujoco, mujoco.viewer
from microduck_locomotion.robot.microduck_cfg import INIT_STATE

m = mujoco.MjModel.from_xml_path("assets/scene.xml")
d = mujoco.MjData(m)

d.qpos[0:3] = INIT_STATE.pos
d.qpos[3:7] = INIT_STATE.rot
for name, val in INIT_STATE.joint_pos.items():
    d.qpos[m.joint(name).qposadr[0]] = val

mujoco.mj_forward(m, d)

with mujoco.viewer.launch_passive(m, d) as v:
    while v.is_running():
        v.sync()
        time.sleep(0.02)