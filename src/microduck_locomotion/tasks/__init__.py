# src/microduck_locomotion/tasks/__init__.py

from mjlab.tasks.registry import register_mjlab_task
from mjlab.tasks.velocity.rl import VelocityOnPolicyRunner

from .velocity_env_cfg import microduck_flat_env_cfg
from .rl_cfg import microduck_ppo_runner_cfg

register_mjlab_task(
    task_id="Microduck-Velocity-Flat",
    env_cfg=microduck_flat_env_cfg(),                 # for training
    play_env_cfg=microduck_flat_env_cfg(play=True),   # for testing
    rl_cfg=microduck_ppo_runner_cfg(),                # TODO: not yet implemented
    runner_cls=VelocityOnPolicyRunner,
)