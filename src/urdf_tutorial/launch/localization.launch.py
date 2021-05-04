import os

import launch.actions
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, EnvironmentVariable

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    nav2_yaml = os.path.join(get_package_share_directory('urdf_tutorial'), 'config', 'nav2.yaml')
    print('nav2_yaml: {}'.format(nav2_yaml))
    map_file = os.path.join(get_package_share_directory('urdf_tutorial'), 'maps', 'new_map.yaml')
    print('map_file: {}'.format(map_file))
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='se simulation (Gazebo) clock if true'
        ),
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[nav2_yaml, {'yaml_filename':map_file} ]),
            
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[nav2_yaml]),

        # Node(
        #     package='nav2_lifecycle_manager',
        #     executable='lifecycle_manager',
        #     name='lifecycle_manager_localization',
        #     output='screen',
        #     parameters=[{'use_sim_time': True},
        #                 {'autostart': True},
        #                 {'node_names': ['map_server', 'amcl']}]),
        ])