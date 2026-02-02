# LIMO_ROS2_SAS
The repo contains the basic ROS2 packages for multiple functionalties available for R&D related purposes
### author: Peter WANG (busg please contact peterwang.dase@connect.hku.hk/peter.w030522@gmail.com)

# Structure of the Repo:
- ## I. Platform Specifications
- ## II. Function Uses

# I. Platform Specifications

### Hardware Specifications
- Nomachine login: username: agilex password: agx
- Login ssh/nx: please check directly from the onboard Nomachine
### Car Warmup
- Long press the switch to start (short press to pause the program). Observe the electricity meter, and charge or replace the battery in time when the last red light is on.
- Observe the status of the front latch and the color of the vehicle light to determine the current mode

Start keyboard control:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

# II. Function Uses

## Bringup and Interfaces

The chassis driver publishes the standard control / state topics (e.g., `/cmd_vel`, `/imu`, `/tf`, `/wheel/odom`, `/limo_status`). Start it with: 

```bash
ros2 launch limo_base limo_base.launch.py
```

For the standard “robot + LiDAR” bringup used by mapping/navigation launch files:

```bash
ros2 launch limo_bringup limo_start.launch.py
```

## Mapping + Navigation

### A) 2D LiDAR pipeline (Cartographer + Nav2)

**1) Start sensor + base**

```bash
ros2 launch limo_bringup limo_start.launch.py
```

**2) Run Cartographer mapping**

```bash
ros2 launch limo_bringup limo_cartographer.launch.py
```

Drive slowly while mapping; fast motion tends to degrade scan-matching and submap consistency. 

**3) Save the map**

```bash
ros2 run nav2_map_server map_saver_cli -f map
```

This produces `map.yaml` + `map.pgm` (or equivalent) in the current directory. 

**4) Run Nav2 localization + navigation (differential / track / mecanum modes)**

```bash
ros2 launch limo_bringup limo_nav2_diff.launch.py
```

If using Ackermann mode:

```bash
roslaunch limo_bringup limo_nav2_ackermann.launch.py
```

In RViz2, we usually do an initial pose estimate (2D Pose Estimate) if the laser overlay doesn’t align with the map, then send goals with 2D Nav Goal. Multi-goal navigation is supported from the RViz Nav2 panel. 

---

### B) RGB-D visual pipeline (RTAB-Map + Nav2)

This path uses the Dabai RGB-D camera + LiDAR bringup, builds an RTAB-Map database, and then runs Nav2 on top of RTAB localization. 

**1) Start sensor + base**

```bash
ros2 launch limo_bringup limo_start.launch.py
ros2 launch astra_camera dabai.launch.py
```

**2) Mapping (RTAB-Map)**

```bash
ros2 launch limo_bringup limo_rtab_rgbd.launch.py
```

The database is saved as `rtabmap.db` under directory home (often within the hidden `.ros/` directory). 

**3) Localization using the saved DB**

```bash
ros2 launch limo_bringup limo_rtab_rgbd.launch.py localization:=true
```

**4) Navigation**

```bash
ros2 launch limo_bringup limo_rtab_nav2_diff.launch.py
```

Ackermann variant:

```bash
roslaunch limo_bringup limo_rtab_nav2_ackermann.launch.py
```

RTAB-Map localization typically removes the need for manual initial-pose alignment; We usually start sending Nav2 goals directly once localization is stable. 

## Loading Image / LiDAR Data

## Implementation Examples:
Car following trial:

[![Watch the demo](http://i3.ytimg.com/vi/yJlPozCGnqk/hqdefault.jpg)](https://youtu.be/yJlPozCGnqk)
