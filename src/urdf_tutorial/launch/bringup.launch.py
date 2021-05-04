import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, EnvironmentVariable
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_working_gazebo = get_package_share_directory('urdf_tutorial')

    urdf_file_name = 'urdf/robot_4wd.urdf.xml'
    print("urdf_file_name : {}".format(urdf_file_name))

    urdf = os.path.join(get_package_share_directory('urdf_tutorial'),urdf_file_name)
    
    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )

    with open(urdf,'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        DeclareLaunchArgument(
          'world',
        #   default_value='false',
          default_value=[os.path.join(pkg_working_gazebo, 'worlds', 'emptyworld.world'), ''],
          description='Use simulation (Gazebo) clock if true'),
        gazebo,
        DeclareLaunchArgument(
              'use_sim_time',
              default_value='true',
              description='se simulation (Gazebo) clock if true'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time':use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf]
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-topic','/robot_description','-entity','myrobot'],
            output='screen'
        )
    ])