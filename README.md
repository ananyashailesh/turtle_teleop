🐢 TurtleBot3 Teleop (Keyboard Control)

This package provides a simple keyboard teleoperation node for controlling a TurtleBot3 robot (tested with ROS Noetic + Gazebo on the Waffle model).

It publishes velocity commands (geometry_msgs/Twist) to the /cmd_vel topic based on user key presses.

📂 Package Structure
turtle_teleop/
├── launch/
│   └── teleop_waffle.launch
├── scripts/
│   └── keyboard_teleop.py
├── CMakeLists.txt
└── package.xml

✨ Features

Interactive keyboard teleoperation for TurtleBot3

Adjustable linear and angular speeds (z/x and c/v keys)

Works in simulation (Gazebo) or with a real robot

Clean exit (robot stops when you quit)

⛓ Dependencies

Make sure you have these installed:

sudo apt update
sudo apt install -y \
  ros-noetic-rospy \
  ros-noetic-geometry-msgs \
  ros-noetic-turtlebot3-gazebo


Also ensure you have a workspace built:

mkdir -p ~/turtle_line_ws/src
cd ~/turtle_line_ws
catkin_make

🚀 Installation

Clone/copy this package into your workspace src folder:

cd ~/turtle_line_ws/src
git clone <your-repo-url> turtle_teleop
cd ~/turtle_line_ws
catkin_make


Make sure the teleop script is executable:

chmod +x ~/turtle_line_ws/src/turtle_teleop/scripts/keyboard_teleop.py


Source your workspace:

source ~/turtle_line_ws/devel/setup.bash

▶️ Usage
Option 1: Launch everything (Gazebo + Teleop)
export TURTLEBOT3_MODEL=waffle
roslaunch turtle_teleop teleop_waffle.launch

Option 2: Run manually

Terminal A — Start Gazebo

export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_gazebo turtlebot3_world.launch


Terminal B — Run Teleop Node

source ~/turtle_line_ws/devel/setup.bash
rosrun turtle_teleop keyboard_teleop.py

🎮 Controls
Key	Action
w	Move forward
s	Move backward
a	Small left turn
d	Small right turn
q	Rotate left
e	Rotate right
SPACE	Stop immediately
z	Decrease linear speed
x	Increase linear speed
c	Decrease angular speed
v	Increase angular speed
h/?	Print help message
Ctrl+C	Quit (robot stops automatically)
🐞 Troubleshooting

No movement?
Run rostopic list and ensure /cmd_vel is published and subscribed. The gazebo_ros_diff_drive plugin must be loaded.

Script exits immediately
Make sure you run it in an interactive terminal (not hidden behind roslaunch). If needed, run directly:

python3 ~/turtle_line_ws/src/turtle_teleop/scripts/keyboard_teleop.py


Gazebo not installed
Install:

sudo apt install ros-noetic-turtlebot3-gazebo
