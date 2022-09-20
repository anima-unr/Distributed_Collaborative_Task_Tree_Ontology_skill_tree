#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def main_publisher():
    pub1 = rospy.Publisher('/launch_1', String, queue_size=100)
    pub2 = rospy.Publisher('/launch_2', String, queue_size=10)
    pub4 = rospy.Publisher('/launch_4', String, queue_size=10)
    rospy.init_node('main_publisher', anonymous=True)
    rate = rospy.Rate(100) # 10hz
    rate.sleep()
    while not rospy.is_shutdown():
        pub1.publish('table_task_sim table_task_sim.launch')
        pub2.publish('table_task_sim human_multi_demo_baxter_param.launch')
        pub4.publish('remote_mutex table_setting_mutex_baxter.launch')
        # rospy.spin()
        rate.sleep()
    # if __name__ == '__main__':
    # try:
    #     talker()
    # except rospy.ROSInterruptException:
    #     pass


