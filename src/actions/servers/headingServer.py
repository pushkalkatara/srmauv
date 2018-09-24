#! /usr/bin/env python
import rospy
import actionlib
import actions.msg
from std_msgs.msg import Float64

class headingAction(object):
    _feedback = actions.msg.headingFeedback()
    _result = actions.msg.headingResult()

    def __init__(self, name):
        rospy.Subscriber("/imu/HeadingTrue_degree/theta", Float64, self.heading_cb)
        self._ha = name
        self._hs = actionlib.SimpleActionServer(
            self._ha, \
            actions.msg.headingAction, \
            execute_cb = self.headingCallback, \
            auto_start = False)
        self._hs.start()

    def heading_cb(self, data):
        if(data < 0):
            self.heading_value = 360 + data
        else:
            self.heading_value = data

    def headingCallback(self, goal):
        r = rospy.Rate(10)
        success = True

        while(goal.heading_setpoint != self.heading_value):
            if self._hs.is_preempt_requested():
                rospy.loginfo('%s : Preempted' % self._ha)
                self._hs.set_preempted()
                success = False
                break
            self._feedback.heading_error = self.heading_value
            self._hs.publish_feedback(self._feedback)
            self._feedback.heading_error = self.heading_value - goal.heading_setpoint
            rospy.loginfo('%s : Going to Heading %f with Error : ',\
                self._ha, \
                goal.heading_setpoint, \
                self._feedback.heading_error)

            r.sleep()

        if success:
            self._result.heading_final = self._feedback.heading_error
            rospy.loginfo('%s : Success' % self._ha)
            self._hs.set_succeeded(self._result)


if __name__ == '__main__':
    rospy.init_node('headingServer')
    server = headingAction(rospy.get_name())
    rospy.spin()