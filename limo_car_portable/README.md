# Portable LiMo Ackermann model

Self-contained meshes, Xacro/URDF, sensor definitions, RViz configuration and Gazebo Classic launch. No original workspace or robot hardware drivers required. Source details and export repairs are in SOURCE.md.

## Import on another computer

Clone the lab repository and copy only this package into a fresh simulation workspace:

```bash
source /opt/ros/humble/setup.bash
git clone https://github.com/SAS-HKU/HKU-SAS-ROS.git
mkdir -p ~/limo_sim_ws/src
cp -a HKU-SAS-ROS/limo_car_portable ~/limo_sim_ws/src/
cd ~/limo_sim_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select limo_car_portable
source install/setup.bash
ros2 launch limo_car_portable display.launch.py
```

Before this package is merged, clone with `--branch feat/portable-limo-simulation`.

For interactive joints: append `gui:=true` to the display launch command.

## Gazebo Classic simulation

The supplied simulator plugins target Gazebo Classic (Gazebo 11 / ROS 2 Humble). Install the optional simulator dependencies separately so RViz-only installations need no Gazebo:

```bash
sudo apt install ros-humble-gazebo-ros-pkgs
ros2 launch limo_car_portable gazebo_classic.launch.py
```

For headless simulation append `gui:=false rviz:=false`. The simulator uses `/cmd_vel` (geometry_msgs/msg/Twist), and publishes odometry and simulated joint states. Do not run the standalone display launch at the same time, since that publishes synthetic joint states. Controller tuning and sensor performance require validation on your target system.

Modern Gazebo (Fortress/Harmonic and later) requires migration of the Classic drive/sensor plugins and ROS bridges. This export does not claim that compatibility. The geometry/URDF and RViz resources can be reused. Migration reference: https://gazebosim.org/docs/latest/migrating_gazebo_classic_ros2_packages/

## Model files

- `gazebo/ackermann_with_sensor.xacro`: complete simulation model, including chassis, wheels, lidar, depth camera and IMU.
- `urdf/limo_ackermann.urdf`: expanded simulation model with portable package mesh URIs.
- `urdf/limo_ackerman_base.xacro`: original alternative visualization model, retained with its original dimensions (different from the simulation variant).
- `meshes/`: all four original DAE/STL assets.

The expanded URDF still requires the installed package for resolving mesh URIs; transfer the whole package, not only the URDF.

## Export validation

Independent colcon build passed on the source machine with ROS 2 Humble. Both model entry points expanded successfully (isolated Xacro 2.1.1). `check_urdf` accepted the complete simulation model: 11 links, 10 joints, root `base_link`. All mesh references resolve within this package; launch Python syntax checks passed. Source package file hashes remained unchanged. Gazebo/RViz graphical execution, driving dynamics and sensor streams have not been tested by this export.
