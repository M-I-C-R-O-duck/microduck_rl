# microduck-rl

Reinforcement learning for the **MicroDuck** robot in **MuJoCo**, using a from-scratch **PPO** implementation, with ONNX export for deployment outside simulation.

## Setup

Run from the repo root: (don't do pip install -e as for now)

```bash
python3 -m venv .venv          # create the virtual environment (first time only)
source .venv/bin/activate      # activate it (every new terminal)
pip install -e .               # install the project + dependencies (first time, or after editing pyproject.toml)
```

## Project Structure

```
microduck-rl/
├── assets/
│   ├── microduck.xml        # Robot model (MJCF)
│   ├── scene.xml            # Simulation environment (floor, lighting, includes the robot)
│   └── meshes/              # 3D mesh files (.stl / .obj) referenced by the MJCF
├── envs/
│   └── microduck_env.py     # Python interface between the robot model and MuJoCo
├── algorithms/
│   ├── ppo.py               # PPO update: improves the policy from collected experience
│   ├── networks.py          # Policy (actor) and value (critic) networks
│   ├── rollout_buffer.py    # Stores experience collected during rollouts
│   └── advantages.py        # GAE: estimates how much better/worse each action was than expected
├── scripts/
│   ├── train.py             # Main training entry point
│   ├── test_env.py          # Environment debugging / sanity checks
│   └── export_onnx.py       # Exports the trained policy to ONNX for deployment
├── config/
│   ├── simulation.yaml      # Simulation settings (timestep, etc.)
│   ├── environment.yaml     # Environment settings (observations, rewards, resets)
│   └── ppo.yaml             # PPO hyperparameters
├── pyproject.toml           # Project metadata and dependencies
└── README.md
```

## Components

### `assets/` — Robot and scene
- **`microduck.xml`**: MJCF description of MicroDuck — bodies, joints, actuators, sensors.
- **`scene.xml`**: The simulation world (floor, lights, physics options); includes the robot model.
- **`meshes/`**: Mesh files for the robot's parts, referenced from the MJCF.

### `envs/` — Environment interface
`microduck_env.py` wraps MuJoCo so the RL code can interact with the robot. Planned functionality:
- Load MicroDuck and display it in the MuJoCo viewer : setup and debugging
- Read joint positions and velocities : the raw material for observations
- Send a command to a joint and observe its movement : the raw material for step()
- Reset the simulation to a known initial configuration : reset()
- Translate policy outputs into actuator commands : action mapping inside step()
- Observations, rewards, termination conditions : the RL-specific parts that come last
- *(more to come: observations, rewards, termination conditions)*

### `algorithms/` — PPO
| File | Role |
|---|---|
| `networks.py` | Defines the neural network that chooses actions (actor) and estimates state values (critic) |
| `rollout_buffer.py` | Stores observations, actions, rewards, and values collected during rollouts |
| `advantages.py` | Computes advantages with GAE (Generalized Advantage Estimation) |
| `ppo.py` | Updates the networks using the collected experience |

### `scripts/` — Entry points
- **`train.py`**: Runs training.
- **`test_env.py`**: For debugging the environment before training.
- **`export_onnx.py`**: Exports the trained policy to ONNX so it can run outside the simulation (e.g., on the real robot).

### `config/` — Configuration
YAML files that keep settings separate from code: `simulation.yaml`, `environment.yaml`, and `ppo.yaml`.

## Acknowledgements

This project is inspired by [pollen-robotics/microduck_rl](https://github.com/pollen-robotics/microduck_rl) by Pollen Robotics. We are re-implementing it from scratch as a learning project, to understand how RL training for MicroDuck works end to end.