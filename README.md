# microduck-rl

Reinforcement learning for the **MicroDuck** robot in **MuJoCo**, using a from-scratch **PPO** implementation, with ONNX export for deployment outside simulation.

## Setup

Run from the repo root:

```bash
python3 -m venv .venv          # create the virtual environment (first time only)
source .venv/bin/activate      # activate it (every new terminal)
pip install -e .               # install the project + dependencies (first time, or after editing pyproject.toml)
```

## View the Model in MuJoCo

```bash
source .venv/bin/activate
python -m mujoco.viewer --mjcf=assets/scene.xml
```

## Project Structure

```
microduck-rl/
│
├── assets/
│   ├── microduck.xml                 # Robot model (MJCF)
│   ├── scene.xml                     # Scene for standalone MuJoCo testing
│   └── meshes/                       # Robot 3D mesh files
│
├── src/
│   └── microduck_locomotion/
│       ├── __init__.py
│       │
│       ├── robot/
│       │   ├── __init__.py
│       │   └── microduck_cfg.py      # Robot configuration for mjlab
│       │
│       └── tasks/
│           ├── __init__.py           # Register the RL training task
│           ├── velocity_env_cfg.py   # Environment and task configuration
│           ├── mdp.py                # Custom reward / observation functions
│           └── rl_cfg.py             # PPO and Actor-Critic configuration
│
├── scripts/
│   ├── inspect_model.py              # Debug MJCF, joints, actuators, sensors
│   └── test_env.py                   # Test mjlab environment step / reset
│
├── logs/                             # Training logs and checkpoints
│
├── pyproject.toml                    # Dependencies and task entry point
├── .gitignore
└── README.md
```

## Acknowledgements

This project is inspired by [pollen-robotics/microduck_rl](https://github.com/pollen-robotics/microduck_rl) by Pollen Robotics. We are re-implementing it from scratch as a learning project, to understand how RL training for MicroDuck works end to end.