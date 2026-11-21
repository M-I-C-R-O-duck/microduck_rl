11.19
完成的：
-在xml文件中导入了所有的零件，包括运动相关的实体和其他实体
-为运动相关部件设置了质量和转动惯量相关参数
-为14个舵机设置了actuator，可以在mujoco里拖动滑块来看各个关节的运动
-按照官方推荐设置了一个站立状态，但未必站得住（使用loadkey）
-为大部分运动相关的零件设置了碰撞体积
-设置了一个地面

待补充的：
-非运动相关部件的碰撞体积
-暂时想不起来了 好像还有点傻

两个inspection python代码主要是为了检查stl文件的几何中心点之类的用的


python版本为3.12.16


## Body 结构树（microduck.xml）

L 后面是 microduck.xml 里的行号（11.21 时的版本，改文件后会变）。`[ ]` 里是这个 body 自己的关节，表示它相对父 body 怎么动；"焊死"表示没有关节，跟着父 body 一起动。

```
world（世界，固定不动）                              地面 ground（在 scene.xml 里）
└── trunk_body  躯干                                 L69   0.199 kg  [trunk_freejoint · free]
    ├── left_shell  身体左外壳                       L124  0 kg      焊死
    ├── right_shell  身体右外壳                      L139  0 kg      焊死
    │
    ├── neck  脖子                                   L154  0.037 kg  [neck_pitch]
    │   └── neck_pitch  脖子上段                     L183  0.006 kg  [head_pitch]
    │       └── yaw_roll_motion  头部转动支架        L207  0.049 kg  [head_yaw]
    │           └── jaw_soft  头（主体）             L243  0.189 kg  [head_roll]
    │               ├── face_part  脸                L312  0 kg      焊死
    │               ├── top_head_shell  头顶外壳     L322  0 kg      焊死
    │               ├── bottom_head_shell  头底外壳  L338  0 kg      焊死
    │               ├── jaw  嘴/下巴                 L354  0 kg      焊死
    │               └── noenoeil  眼睛部件           L370  0 kg      焊死
    │
    ├── bearing_roll  右髋（转向）                   L383  0.023 kg  [right_hip_yaw]
    │   └── hip_l_2  右髋（侧摆）                    L417  0.006 kg  [right_hip_roll]
    │       └── upper_leg_right  右大腿              L447  0.048 kg  [right_hip_pitch]
    │           └── leg_2  右小腿                    L489  0.022 kg  [right_knee]
    │               └── ankle_right  右脚踝+右脚     L519  0.030 kg  [right_ankle]
    │
    └── yaw2roll  左髋（转向）                       L570  0.023 kg  [left_hip_yaw]
        └── hip_l  左髋（侧摆）                      L604  0.006 kg  [left_hip_roll]
            └── upper_leg_left  左大腿               L634  0.048 kg  [left_hip_pitch]
                └── leg  左小腿                      L673  0.022 kg  [left_knee]
                    └── ankle_left  左脚踝+左脚      L703  0.030 kg  [left_ankle]
```

