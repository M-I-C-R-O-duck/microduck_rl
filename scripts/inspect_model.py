# scripts/inspect_model.py

from pathlib import Path

import mujoco

ROOT = Path(__file__).resolve().parent.parent

model = mujoco.MjModel.from_xml_path(
    str(
        ROOT / "assets" / "scene.xml"
    )
)
data = mujoco.MjData(model)

print("Number of joints:", model.njnt)
print("Number of actuators:", model.nu)
print("Number of sensors:", model.nsensor)

for i in range(model.njnt):
    print(
        mujoco.mj_id2name(
            model,
            mujoco.mjtObj.mjOBJ_JOINT,
            i
        )
    )
