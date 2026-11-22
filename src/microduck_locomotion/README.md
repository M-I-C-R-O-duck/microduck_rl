# microduck_locomotion

MicroDuck 在 mjlab 里的机器人配置和 RL 训练任务（velocity tracking：按速度命令走路）。

安装方式：在仓库根目录 `pip install -e .`（editable 安装，改代码不用重装；改 `pyproject.toml` 后要重装）。

## 目录结构

```
microduck_locomotion/
├── __init__.py               # 空文件，标记这是一个 Python package
├── README.md                 # 本文件
│
├── robot/                    # 机器人本身（和任务无关）
│   ├── __init__.py           # 空文件
│   └── microduck_cfg.py      # 机器人配置：加载 XML、初始姿态、注册 actuator
│
└── tasks/                    # 训练任务（走路）
    ├── __init__.py           # 把任务注册到 mjlab（task id: Microduck-Velocity-Flat）
    ├── velocity_env_cfg.py   # 环境配置：观测、动作、速度命令、reward、随机化……
    ├── mdp.py                # 自己写的 reward / 观测函数（空，待定）
    └── rl_cfg.py             # PPO 和网络的参数（空，待定）
```

## 每个文件做什么

### robot/microduck_cfg.py ✅ 完成

告诉 mjlab"机器人是什么样的"。

- `get_spec()`：读取仓库根目录的 `assets/microduck.xml`
- `INIT_STATE`：初始姿态（站姿）
  - 躯干高度 z = 0.1172 m：这个高度下脚刚好贴地（二分搜索算出来的）
  - 14 个关节角：和原来 XML 里的 STAND keyframe 一样
  - 这也是 action 的零点：`目标角 = INIT_STATE 关节角 + scale × 策略输出`
  - **初始姿态现在只以这里为准**，XML 里的 STAND keyframe 已经注释掉了
- `ARTICULATION`：用 `XmlActuatorCfg` 把 XML 里已有的 14 个 position servo 登记给 mjlab
  - 正则只匹配关节名（`.*_hip_yaw`、`.*_knee`、`head_.*` 等），不会误匹配到 site
  - 不写这个的话，mjlab 认为机器人没有 actuator：reset 时 ctrl 是 0，action 也找不到关节
- `get_microduck_robot_cfg()`：把上面三样组合成 `EntityCfg`，给任务使用

### tasks/velocity_env_cfg.py 🟡 第 7 步（reward）未完成

`microduck_flat_env_cfg(play=False)`：从 mjlab 的通用模板 `make_velocity_env_cfg()`（按 G1 人形机器人写的）开始，改成适合 MicroDuck 的设置。

模板源码（对应我们装的 mjlab v1.6.1）：[mjlab/tasks/velocity/velocity_env_cfg.py](https://github.com/mujocolab/mjlab/blob/v1.6.1/src/mjlab/tasks/velocity/velocity_env_cfg.py)。本地也有同一份：`.venv/lib/python3.12/site-packages/mjlab/tasks/velocity/velocity_env_cfg.py`。

| 步骤 | 内容 | 状态 |
|---|---|---|
| 1 | 拿到 mjlab 模板 | ✅ |
| 2 | 把机器人换成 MicroDuck | ✅ |
| 3 | 平地：去掉地形生成器、`terrain_scan` 传感器、`height_scan` 观测、`out_of_terrain_bounds` 终止条件、`terrain_levels` curriculum | ✅ |
| 4 | 填模板里所有 "Set per-robot" 的空位（见下） | ✅（reward 部分除外） |
| 5 | action scale = 0.44 rad（= 0.25 × 力矩上限 0.96 / kp 0.55） | ✅ |
| 6 | 观测和速度命令（见下） | ✅ |
| 7 | reward 和终止条件 | ❌ 待定，和队友商量中 |
| 8 | play 模式（看效果时用） | ✅ |

**第 4 步用到的名字（都来自 `assets/microduck.xml`）：**

| 用在哪 | 类型 | 名字 |
|---|---|---|
| `foot_height_scan`（每只脚往下打射线，测脚离地多高） | site | `left_foot`、`right_foot` |
| `feet_ground_contact`（新建的接触传感器：脚有没有着地、接触力、腾空时间） | body | `ankle_left`、`ankle_right` |
| `foot_friction`（随机化脚的摩擦力） | geom | `left_foot_collision`、`right_foot_collision` |
| `base_com`（随机化躯干质心） | body | `trunk_body` |
| viewer 镜头跟随 | body | `trunk_body`，距离 0.5 m |

另外把 `reset_base` 的出生高度偏移改成 0–5 mm（模板是 1–5 cm，会让小鸭子从高处掉下来）。

**第 6 步：**
- actor 删掉 `base_lin_vel`：真机的 IMU（LSM6DSV16X）只有陀螺仪和加速度计，测不到线速度。critic 保留它作为特权信息
- actor 观测：`base_ang_vel`、`projected_gravity`、`joint_pos`、`joint_vel`、`actions`、`command`（51 维）；critic 66 维
- 速度命令：前后 ±0.4 m/s、左右 ±0.3 m/s、转向 ±1.0 rad/s（参考 pollen）
- 删掉 `command_vel` curriculum：它会把速度范围改回 ±1 m/s，最后放大到 3 m/s
- `rel_heading_envs = 0`：直接给转向速度，不用"目标朝向"模式（方便以后 CV / 手柄直接发速度）

**第 8 步（`play=True`）：** episode 永不超时、关掉观测噪声、每 0.5–1 秒推一次（测试抗干扰）、清空 curriculum。

⚠️ 目前 `env.reset()` 可以跑通，但 `env.step()` 会报错，因为模板里 `pose` reward 的 std 还是空的。这要等第 7 步。

### tasks/__init__.py 🟡 写好了，但依赖 rl_cfg.py

调用 `register_mjlab_task(...)`，把任务 `Microduck-Velocity-Flat` 注册到 mjlab，这样 mjlab 的 `train` / `play` / `list-envs` 命令能找到它。

⚠️ 它 import 了 `rl_cfg.py` 里的 `microduck_ppo_runner_cfg`，但 `rl_cfg.py` 现在是空的，所以**目前任何 `import microduck_locomotion.tasks...` 都会报 ImportError**（包括只 import `velocity_env_cfg`）。在 `rl_cfg.py` 写好之前，想测试环境的话可以先把这个文件的内容注释掉。

还要在 `pyproject.toml` 里加 entry point，mjlab 才会去 import 这个包（还没加）：

```toml
[project.entry-points."mjlab.tasks"]
microduck = "microduck_locomotion.tasks"
```

### tasks/rl_cfg.py ❌ 空，待定

PPO 的超参数和 actor / critic 网络结构（`RslRlOnPolicyRunnerCfg`），参考 `mjlab/tasks/velocity/config/g1/rl_cfg.py`。只有在用 rsl_rl 的 PPO 时才需要；如果完全自己写 PPO，可以不用。

### tasks/mdp.py ❌ 空，待定

自己写的 reward / 观测函数。格式：`def my_reward(env, ...) -> torch.Tensor`，返回形状 `[num_envs]`，再在 `velocity_env_cfg.py` 里用 `RewardTermCfg(func=..., weight=..., params=...)` 接进去。

## 参考链接

mjlab 官方仓库：https://github.com/mujocolab/mjlab （文档：https://mujocolab.github.io/mjlab/ ）

下面的链接都固定在 tag `v1.6.1`，和 `pyproject.toml` 装的版本一致。`main` 分支上的代码可能已经改了，以本地 `.venv` 里的那份为准。

| 文件 | 内容 |
|---|---|
| [tasks/velocity/velocity_env_cfg.py](https://github.com/mujocolab/mjlab/blob/v1.6.1/src/mjlab/tasks/velocity/velocity_env_cfg.py) | 通用模板 `make_velocity_env_cfg()`，我们的 `velocity_env_cfg.py` 就是在改它 |
| [tasks/velocity/config/g1/env_cfgs.py](https://github.com/mujocolab/mjlab/blob/v1.6.1/src/mjlab/tasks/velocity/config/g1/env_cfgs.py) | G1 怎么填模板的空位，写法可以直接对照 |
| [tasks/velocity/mdp/rewards.py](https://github.com/mujocolab/mjlab/blob/v1.6.1/src/mjlab/tasks/velocity/mdp/rewards.py) | 模板里每个 reward 函数的具体公式（第 7 步要看） |

MicroDuck 的原版实现（我们参考的数值来源）：[pollen-robotics/microduck_rl](https://github.com/pollen-robotics/microduck_rl)，其中环境配置在 `src/mjlab_microduck/tasks/microduck_velocity_env_cfg.py`，机器人模型在 `src/mjlab_microduck/robot/microduck/robot_walk.xml`。

## 待决定

1. **Reward**：直接用模板的 13 项 / 在 `mdp.py` 里替换其中几项 / 整套自己设计
2. **PPO**：先用 rsl_rl 跑出 baseline，再换成自己写的 / 直接自己写
   - 根目录 README 第 3 行写的是 "from-scratch PPO"，但项目结构里只有 `rl_cfg.py`（rsl_rl 的写法），定了以后要统一

## Update

### 11.21

`robot/microduck_cfg.py`
- 写了 `get_spec`、`INIT_STATE`、`ARTICULATION`、`get_microduck_robot_cfg`
- 修了 XML 路径（要往上 4 层 `.parent` 才到仓库根目录）
- `INIT_STATE` 的 z 从 0.12 调到 0.1172，让脚刚好贴地出生

`tasks/velocity_env_cfg.py`
- 完成第 1–6 步和第 8 步，第 7 步（reward）留空

`tasks/__init__.py`
- 写了任务注册（还缺 `rl_cfg.py` 和 pyproject entry point）

这个 package 以外的相关改动：
- `assets/microduck.xml`：
  - 加了 IMU site（`trunk_body` 里）和两个脚底 site（`ankle_left` / `ankle_right` 里），位置照抄 pollen 的 `robot_walk.xml`
  - 加了 `<sensor>` 块：`imu_ang_vel`（陀螺仪）、`imu_accel`（加速度计）、`imu_lin_vel`（仿真才有）、`orientation`、`root_angmom`（仿真才有）
  - 注释掉了 STAND keyframe（初始姿态改为只以 `INIT_STATE` 为准）
- `scripts/view_init_state.py`：在 MuJoCo viewer 里显示 `INIT_STATE` 的姿态（仓库根目录运行；关窗口退出，不要用 Ctrl+C）
- `pyproject.toml` 加了 `mjlab` 依赖，`pip install -e .` 装好了
- 根目录 README 加了 "View the Model in MuJoCo"
