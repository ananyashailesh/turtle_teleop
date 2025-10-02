#!/usr/bin/env python3
"""
keyboard_teleop.py

Robust keyboard teleop for TurtleBot3 (Waffle) — ROS Noetic, Python3.

Controls (interactive terminal must have focus):
  w/s : forward / backward
  a/d : small turn left / right
  q/e : rotate left / rotate right
  SPACE: stop
  z/x : decrease/increase linear speed
  c/v : decrease/increase angular speed
  h/? : show help
  Ctrl-C: quit

Publishes geometry_msgs/Twist to /cmd_vel.
"""

import rospy
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty
import time
import os
import rosgraph

HELP_MSG = """
Keyboard Teleop for TurtleBot3 (Waffle)

w/s : forward / backward
a/d : small turn left / right
q/e : rotate left / rotate right
SPACE: stop
z/x : decrease/increase linear speed
c/v : decrease/increase angular speed
h/? : show this help
Ctrl-C : quit

Current:
  linear speed = {lin:.2f} m/s
  angular speed = {ang:.2f} rad/s
"""

# Default speeds
LIN_SPEED = 0.20
ANG_SPEED = 0.60

def is_tty():
    return sys.stdin.isatty()

def get_key(timeout=0.1):
    """Non-blocking single-key read with timeout (returns '' on timeout)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        rlist, _, _ = select.select([fd], [], [], timeout)
        if rlist:
            ch = sys.stdin.read(1)
            return ch
        return ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def wait_for_ros_master(timeout=10.0):
    """Wait up to `timeout` seconds for ROS master to be available."""
    t0 = time.time()
    master = rosgraph.Master('/keyboard_teleop')
    while time.time() - t0 < timeout:
        try:
            master.getPid()
            return True
        except Exception:
            time.sleep(0.2)
    return False

def main():
    tty_ok = is_tty()
    print("=== keyboard_teleop starting ===")
    if not tty_ok:
        print("[WARN] stdin is not a TTY. Run this node in an interactive terminal to accept key presses.")
        print("If you launched via roslaunch, consider running this with rosrun or directly with python3 in a terminal.")

    print("Checking for ROS master ({}s timeout)...".format(10.0))
    master_found = wait_for_ros_master(10.0)
    if master_found:
        print("ROS master detected.")
    else:
        print("[WARN] ROS master NOT detected within timeout. The node will still run and attempt to connect.")

    # init node (ok if master not present yet, it'll connect when available)
    rospy.init_node('keyboard_teleop', anonymous=False)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    lin = LIN_SPEED
    ang = ANG_SPEED
    print(HELP_MSG.format(lin=lin, ang=ang))

    rate = rospy.Rate(10)  # Hz

    try:
        while not rospy.is_shutdown():
            if not tty_ok:
                # no interactive TTY — idle but keep node alive
                time.sleep(0.5)
                continue

            key = get_key(timeout=0.1)
            twist = Twist()
            dirty = False

            if key == 'w':
                twist.linear.x = lin; dirty = True
            elif key == 's':
                twist.linear.x = -lin; dirty = True
            elif key == 'a':
                twist.angular.z = ang * 0.6; dirty = True
            elif key == 'd':
                twist.angular.z = -ang * 0.6; dirty = True
            elif key == 'q':
                twist.angular.z = ang; dirty = True
            elif key == 'e':
                twist.angular.z = -ang; dirty = True
            elif key == ' ':
                twist = Twist(); dirty = True
            elif key == 'z':
                lin = max(0.01, lin - 0.01)
                print("Linear speed decreased: {:.3f} m/s".format(lin))
            elif key == 'x':
                lin += 0.01
                print("Linear speed increased: {:.3f} m/s".format(lin))
            elif key == 'c':
                ang = max(0.05, ang - 0.05)
                print("Angular speed decreased: {:.3f} rad/s".format(ang))
            elif key == 'v':
                ang += 0.05
                print("Angular speed increased: {:.3f} rad/s".format(ang))
            elif key in ['h', '?']:
                print(HELP_MSG.format(lin=lin, ang=ang))
            elif key == '':
                # timeout/no key pressed
                pass
            else:
                # unknown key — ignore
                pass

            if dirty:
                pub.publish(twist)

            rate.sleep()

    except (rospy.ROSInterruptException, KeyboardInterrupt):
        pass
    finally:
        # attempt clean stop
        try:
            pub.publish(Twist())
        except Exception:
            pass
        print("\nShutting down keyboard teleop node.")

if __name__ == "__main__":
    main()
