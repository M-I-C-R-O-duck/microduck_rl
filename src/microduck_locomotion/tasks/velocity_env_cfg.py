# src/microduck_locomotion/tasks/velocity_env_cfg.py

import math
from dataclasses import replace

from mjlab.envs import ManagerBasedRlEnvCfg
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.sensor import (
    ContactMatch,
    ContactSensorCfg,
    ObjRef,
    RingPatternCfg,
    TerrainHeightSensorCfg,
)
from mjlab.tasks.velocity.mdp import UniformVelocityCommandCfg
from mjlab.tasks.velocity.velocity_env_cfg import make_velocity_env_cfg
from mjlab.utils.noise import UniformNoiseCfg as Unoise

from microduck_locomotion.robot.microduck_cfg import get_microduck_robot_cfg

def microduck_flat_env_cfg(play: bool = False) -> ManagerBasedRlEnvCfg:
    # 1. Use template in mjlab
    cfg = make_velocity_env_cfg()

    # 2. Replace robot
    cfg.scene.entities = {"robot": get_microduck_robot_cfg()}

    # 3. Configure flat terrain
    cfg.scene.terrain.terrain_type = "plane"
    cfg.scene.terrain.terrain_generator = None
    cfg.scene.terrain.max_init_terrain_level = None

    cfg.scene.sensors = tuple(
        s for s in (cfg.scene.sensors or ()) if s.name != "terrain_scan"
    )

    del cfg.observations["actor"].terms["height_scan"]
    del cfg.observations["critic"].terms["height_scan"]
    del cfg.terminations["out_of_terrain_bounds"]
    del cfg.curriculum["terrain_levels"]

    # 4. Fix Set per-robot in the template
    for sensor in cfg.scene.sensors:
        if sensor.name == "foot_height_scan":
            sensor.frame = (
                ObjRef(type="site", name="left_foot",  entity="robot"),
                ObjRef(type="site", name="right_foot", entity="robot"),
            )
            sensor.pattern = RingPatternCfg.single_ring(
                radius=0.01,
                num_samples=6,
            )
            sensor.ray_alignment = "yaw"
            sensor.max_distance = 1.0

    cfg.events["foot_friction"].params["asset_cfg"].geom_names = ("left_foot_collision", "right_foot_collision")
    cfg.events["base_com"].params["asset_cfg"].body_names = ("trunk_body",)

    # TODO: Fix Reward.

    cfg.viewer.body_name = "trunk_body"
    cfg.viewer.distance = 0.5

    feet_ground_cfg = ContactSensorCfg(
        name="feet_ground_contact",
        primary=ContactMatch(
            mode="subtree",
            pattern=r"^(ankle_left|ankle_right)$",
            entity="robot",
        ),
        secondary=ContactMatch(
            mode="body",
            pattern="terrain",
        ),
        fields=("found", "force"),
        reduce="netforce",
        num_slots=1,
        track_air_time=True,
    )
    cfg.scene.sensors = (cfg.scene.sensors or ()) + (
        feet_ground_cfg,
    )

    cfg.events["reset_base"].params["pose_range"]["z"] = (0.0, 0.005)

    # 5. Configure action scale
    cfg.actions["joint_pos"].scale = 0.44

    # 6. Choose observations and commands
    del cfg.observations["actor"].terms["base_lin_vel"]

    cfg.commands["twist"].ranges.lin_vel_x = (-0.4, 0.4)
    cfg.commands["twist"].ranges.lin_vel_y = (-0.3, 0.3)
    cfg.commands["twist"].ranges.ang_vel_z = (-1.0, 1.0)

    del cfg.curriculum["command_vel"]
    cfg.commands["twist"].rel_heading_envs = 0.0

    # 7. Configure rewards and termination

    # 8. Apply play-mode overrides
    if play:
        cfg.episode_length_s = int(1e9)
        cfg.observations["actor"].enable_corruption = False
        cfg.events["push_robot"].interval_range_s = (0.5, 1.0)
        cfg.curriculum = {}


    return cfg