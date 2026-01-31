
the commands are expected to be run one-by-one
 
# Navigation

```shell
rviz2
## 启动底盘
ros2 launch limo_bringup limo_start.launch.py
sleep 2
## 启动导航
ros2 launch limo_bringup limo_navigation.launch.py
sleep 2
## 启动定位
ros2 launch limo_bringup limo_localization.launch.py
```

# Mapping

```shell
ros2 launch limo_bringup limo_start.launch.py
ros2 launch build_map_2d revo_build_map_2d.launch.py
#上面三条指令启动之后，用遥控器控制车子行走
# 建完图保存， 放到 limo_bringup/maps 里， 再 colcon build 编译一下XXX
```


# teleop keyboard control

```shell
ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 launch limo_bringup limo_start.launch.py
```
