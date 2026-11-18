
# MicroDuck Environment (`microduck_env.py`)

## Overview

The `MicroDuckEnv` class manages the MuJoCo simulation and provides the interface for reinforcement learning.

Its main responsibilities include loading the robot model, reading robot states, controlling actuators, advancing physics, resetting the simulation, and supporting RL training.

## Implementation Checklist

### 1. Environment Setup
*Done once in the constructor (`__init__`).*

- [ ] **Load XML:** Initialize `self.model` and `self.data`.
- [ ] **Simulation settings:** Set control frequency, action scale, and other parameters (hardcoded for now; config later).
- [ ] **Store robot information:**
  - Number of actuators
  - Home keyframe
  - Joint limits
  - Trunk body ID

### 2. Basic Robot Interaction
*Core MuJoCo functionality — no RL knowledge required.*

- [ ] **Read state:** Get joint positions (`qpos`), velocities (`qvel`), trunk orientation, and angular velocity (from `qpos`/`qvel` or IMU sensors).
- [ ] **Send commands:** Write joint targets into `data.ctrl` (assuming position actuators).
- [ ] **Advance physics:** Call `mujoco.mj_step()` for each physics step. Execute multiple physics steps per policy step (decimation).
- [ ] **Reset simulation:** Restore the home pose, zero velocities, and reset simulation time.

### 3. Reinforcement Learning Interface
*Build the RL interface using the basic functions above.*

- [ ] **Action mapping:** Convert policy outputs (typically `[-1, 1]`) into valid joint targets.
- [ ] **Observation:** Combine relevant robot states into a single flat NumPy array.
- [ ] **Reward:** Calculate a scalar reward representing how well the robot performs.
- [ ] **Termination:** Determine when an episode ends (e.g., falling over or reaching the time limit).
- [ ] **`reset()`:**
  - Restore the robot to its initial state.
  - Add randomized initialization later.
  - Return the initial observation.
- [ ] **`step(action)`:**
  1. Map the policy action to joint targets.
  2. Send commands to actuators.
  3. Advance the simulation.
  4. Collect the new observation.
  5. Calculate the reward.
  6. Check termination conditions.
  7. Return observation, reward, and episode status.

### 4. Visualization & Debugging
*Optional — not required during training.*

- [ ] **Viewer:** Open a MuJoCo viewer to visualize and debug the simulation.

## Recommended Development Order

| Phase | Tasks | RL Knowledge Required |
|---|---|---|
| 1. Setup | Load XML, configure simulation, store robot information | No |
| 2. Robot Interaction | Read state, send commands, advance physics, reset | No |
| 3. RL Interface | Action mapping, observations, `reset()`, `step()` | Basic |
| 4. Training Logic | Reward function, termination conditions | Yes |
| 5. Debugging | Visualization and testing | No |

**First milestone:** Complete environment setup, basic robot interaction, and visualization.

**Later:** Focus on reward design and termination conditions, as these require more RL-specific decisions.
