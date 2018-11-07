#! /usr/bin/env python
import rospy
from smach import StateMachine
import smach
from smach_ros import IntrospectionServer
from Sink import Sink
from ImageTask import ImageTask
from darknet_ros_msgs.msg import BoundingBox

def main():
    rospy.init_node('mission_planner')
    sm = smach.StateMachine(outcomes=['mission_complete', 'mission_failed', 'aborted'])

    with sm:
        Sink(sm, 5, 'mission_complete')
        #ImageTask(sm, 'mission_complete') 

        sis = IntrospectionServer('ZARNA_MISSION_PLANNER', sm, '/START_ZARNA')
        # start introspection server by - rosrun smach_viewer smach_viewer.py
        sis.start()
        outcome = sm.execute()


    rospy.spin()
    sis.stop()
if __name__ == '__main__':
    main()
