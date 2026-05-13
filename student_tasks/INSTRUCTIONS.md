# Lidar Obstacle Avoidance Student Task

## Goal
Complete the obstacle avoidance logic for the MentorPi lidar application. Your code will read `LaserScan` distance data, decide whether the robot should move forward or turn, and publish a `Twist` command to the chassis controller.

## Files

| File | Purpose | Student action |
|---|---|---|
| `lidar_controller_student.py` | Starter version of `app/app/lidar_controller.py` | Complete the `running_mode == 1` obstacle avoidance block |
| `lidar_controller.py` | Complete reference version | Do not submit this as your answer |

The grading system will copy your completed `lidar_controller_student.py` into the ROS package as `app/app/lidar_controller.py` before building.

## ROS Topics and Services

- Input topic: `/scan_raw` (`sensor_msgs/LaserScan`)
- Output topic: `/controller/cmd_vel` (`geometry_msgs/Twist`)
- Enter service: `/lidar_app/enter` (`std_srvs/srv/Trigger`)
- Mode service: `/lidar_app/set_running` (`interfaces/srv/SetInt64`)

Mode values:

- `0`: stop
- `1`: obstacle avoidance
- `2`: lidar following
- `3`: lidar guarding

## What To Complete

Inside `lidar_callback()`, complete the block for `self.running_mode == 1` when the robot is not an Ackermann model. Your implementation should:

1. Filter invalid lidar readings from `left_range` and `right_range`. Ignore `0`, `inf`, and `nan` values.
2. Compute the nearest valid distance on the left and right sides.
3. Compare each distance with `self.threshold`.
4. Publish a `Twist` command:
   - no obstacle: drive forward with `linear.x = self.speed`
   - left obstacle: turn right
   - right obstacle: turn left
   - both sides blocked: turn around
5. Update `self.last_act` and `self.timestamp` so the robot keeps turning long enough to avoid the obstacle.

## Build Command

```bash
cd /home/ubuntu/ros2_ws
colcon build --packages-select app
source install/setup.bash
```

## Run Commands

```bash
ros2 launch app lidar_node.launch.py debug:=true
ros2 service call /lidar_app/enter std_srvs/srv/Trigger {}
ros2 service call /lidar_app/set_running interfaces/srv/SetInt64 "{data: 1}"
```

Stop the mode:

```bash
ros2 service call /lidar_app/set_running interfaces/srv/SetInt64 "{data: 0}"
```

## Success Criteria

Your program should compile, run without `NotImplementedError`, and publish reasonable `Twist` commands for clear path, left obstacle, right obstacle, and both-sides-blocked cases.
