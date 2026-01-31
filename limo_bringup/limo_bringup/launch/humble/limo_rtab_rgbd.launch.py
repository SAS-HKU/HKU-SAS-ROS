
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    qos = LaunchConfiguration('qos')
    localization = LaunchConfiguration('localization')
    rviz_config_dir = os.path.join(get_package_share_directory('limo_bringup'),'rviz','rtabmap.rviz')

    parameters={
          'frame_id':'base_link',
          'use_sim_time':False,
          'subscribe_depth':True,
          'subscribe_rgbd':False,
          'subscribe_rgb':True,
          'subscribe_scan':True,
          'use_action_for_goal':True,
          'wait_for_transform':0.2,
          'qos_image':qos,
          'qos_scan':qos,
          'qos_camera_info':qos,
          'approx_sync':True,
          'Reg/Force3DoF':'true',
          'Optimizer/GravitySigma':'0' # Disable imu constraints (we are already in 2D)
    }

    remappings=[
          ('odom','/wheel/odom'),
          ('scan','/scan'),
          ('rgb/image', '/camera/color/image_raw'),
          ('rgb/camera_info', '/camera/color/camera_info'),
          ('depth/image', '/camera/depth/image_raw')]
    base_link_to_camera_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_base_camera',
        arguments=['0.1','0','0.18','0','0','0','1','base_link','camera_link']
    )
    
    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen')

    return LaunchDescription([

        # Launch arguments
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        
        DeclareLaunchArgument(
            'qos', default_value='2',
            description='QoS used for input sensor topics'),
            
        DeclareLaunchArgument(
            'localization', default_value='false',
            description='Launch in localization mode.'),

        # Nodes to launch
        
        # SLAM mode:
        Node(
            condition=UnlessCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters],
            remappings=remappings,
            arguments=['-d']), # This will delete the previous database (~/.ros/rtabmap.db)
            
        # Localization mode:
        Node(
            condition=IfCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters,
              {'Mem/IncrementalMemory':'False',
               'Mem/InitWMWithAllNodes':'True'}],
            remappings=remappings),

        Node(
             package='rtabmap_viz', executable='rtabmap_viz', output='screen',
             parameters=[parameters],
             remappings=remappings),
        


        rviz_node,
        base_link_to_camera_node
    ])
