# src/microduck_locomotion/robot/microduck_cfg.py

from pathlib import Path

import mujoco
from mjlab.entity import EntityCfg, EntityArticulationInfoCfg
from mjlab.actuator import XmlActuatorCfg

def get_spec():
    ROBOT_XML_PATH = Path(__file__).resolve().parent.parent.parent.parent
    return mujoco.MjSpec.from_file(
        str(
            ROBOT_XML_PATH / "assets" / "microduck.xml"
        )
    )

INIT_STATE = EntityCfg.InitialStateCfg(
    pos=(0.0, 0.0, 0.1172),
    joint_pos={
        "left_hip_yaw": 0.0, "left_hip_roll": -0.08726646, "left_hip_pitch": -0.457924, "left_knee": -0.004940, "left_ankle": 0.452984,
        "right_hip_yaw": 0.0, "right_hip_roll": 0.08726646, "right_hip_pitch": 0.457924, "right_knee": 0.004940, "right_ankle": -0.452984,
        "neck_pitch": 0.34906585, "head_pitch": 0.34906585, "head_yaw": 0.0, "head_roll": 0.0,
    },
)

ARTICULATION = EntityArticulationInfoCfg(
    actuators=(
        XmlActuatorCfg(target_names_expr=(
            "neck_pitch", "head_.*",
            ".*_hip_yaw", ".*_hip_roll", ".*_hip_pitch", ".*_knee", ".*_ankle",
        )),
    ),
)

def get_microduck_robot_cfg():
    return EntityCfg(
        spec_fn=get_spec,
        init_state=INIT_STATE,
        articulation=ARTICULATION,
    )