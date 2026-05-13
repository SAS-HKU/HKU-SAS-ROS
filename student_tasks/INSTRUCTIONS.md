# Mecanum Motor Control Student Task

## Goal
Complete the core ROS2 motor-control code for the MentorPi mecanum chassis. Your code will convert velocity commands into individual wheel speeds and send those motor commands to the robot controller board.

## Files

| File | Purpose | Student action |
|---|---|---|
| `mecanum_student.py` | Starter version of `controller/mecanum.py` | Complete speed conversion and mecanum wheel equations |
| `controller_student.launch.py` | Starter version of `controller.launch.py` | Complete package path lookup for installed launch mode |
| `ros_robot_controller_node_student.py` | Starter version of `ros_robot_controller_node.py` | Complete motor message conversion in `set_motor_state()` |
| Original files without `_student` | Complete reference versions | Do not submit these as your answer |

The grading system will copy completed starter files into their ROS package locations before building.

## ROS Data Flow

1. A user publishes `geometry_msgs/Twist` to `/controller/cmd_vel`.
2. The controller node reads `linear.x`, `linear.y`, and `angular.z`.
3. `MecanumChassis.set_velocity()` converts chassis velocity into four wheel speeds.
4. The controller publishes `ros_robot_controller_msgs/MotorsState`.
5. `RosRobotController.set_motor_state()` converts that ROS message into board commands.
6. The STM32 controller drives motors 1 to 4.

## What To Complete

### `mecanum_student.py`
Complete:

- `speed_covert(speed)`
- `set_velocity(linear_x, linear_y, angular_z)`

Use the mecanum equations from the lesson. Convert each wheel speed from meters/second to rotations/second before creating `MotorState` messages.

### `controller_student.launch.py`
Complete the installed-package path lookup using `get_package_share_directory()` for:

- `peripherals`
- `controller`

### `ros_robot_controller_node_student.py`
Complete `set_motor_state()` so each incoming `MotorState` becomes `[id, rps]`, then call `self.board.set_motor_speed(data)`.

## Build Command

```bash
cd /home/ubuntu/ros2_ws
colcon build --packages-select ros_robot_controller controller
source install/setup.bash
```

## Run Command

```bash
ros2 launch controller controller.launch.py
```

## Example Velocity Command

```bash
ros2 topic pub /controller/cmd_vel geometry_msgs/Twist "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Stop the robot by publishing zero velocity:

```bash
ros2 topic pub /controller/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

## Success Criteria

Your program should compile, run without `NotImplementedError`, produce four motor commands with IDs 1 to 4, and stop safely when zero velocity is published.
