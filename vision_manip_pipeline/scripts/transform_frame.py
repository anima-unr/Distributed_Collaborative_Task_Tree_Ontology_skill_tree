# #!/usr/bin/env python
# import rospy
# from geometry_msgs.msg import Pose

# import tf2_ros
# import tf2_geometry_msgs  # **Do not use geometry_msgs. Use this instead for PoseStamped


# def transform_pose(input_pose, from_frame, to_frame):

#     # **Assuming /tf2 topic is being broadcasted
#     tf_buffer = tf2_ros.Buffer()
#     listener = tf2_ros.TransformListener(tf_buffer)

#     pose_stamped = tf2_geometry_msgs.PoseStamped()
#     pose_stamped.pose = input_pose
#     pose_stamped.header.frame_id = from_frame
#     pose_stamped.header.stamp = rospy.Time.now()

#     try:
#         # ** It is important to wait for the listener to start listening. Hence the rospy.Duration(1)
#         output_pose_stamped = tf_buffer.transform(pose_stamped, to_frame, rospy.Duration(1))
#         return output_pose_stamped.pose

#     except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
#         raise


# # Test Case
# rospy.init_node("transform_test")

# my_pose = Pose()
# my_pose.position.x = 0.312167077015
# my_pose.position.y = -0.00491186380653
# my_pose.position.z = 1.08760421723
# my_pose.orientation.x = -0.413855004214
# my_pose.orientation.y = 0.742213644886
# my_pose.orientation.z = 0.515717491433
# my_pose.orientation.w = -0.108988117987

# transformed_pose = transform_pose(my_pose, "kinect2_link", "right_gripper")

# print(transformed_pose)
import rospy
from transform_frames import TransformFrames
from geometry_msgs.msg import Pose, Point, Quaternion, PoseArray
from std_msgs.msg import Header

if __name__=="__main__":

    rospy.init_node('base_scan_coords') 

    tf = TransformFrames()  # This initializes frame buffer
    rospy.sleep(1.0)         # Sleep so that buffer can fill up

    # Here a pose defined in base_scan
    scan_pos = Pose(position=Point(0.783297669595,-0.0469012368112,-0.182741324213), orientation=Quaternion(-0.0003481747685,-0.0242994292008,-0.120378653421,0.99243054987))
    # Create a pose_array with frame_id='base_scan' to store it
    pose_array = PoseArray(header=Header(frame_id='base',stamp=rospy.Time(0)))
    pose_array.poses.append(scan_pos)

    new_pose_array = tf.pose_transform(pose_array=pose_array, target_frame='ar_marker_11')

    rospy.loginfo('Original pose in base_scan')
    rospy.loginfo(pose_array)
    rospy.loginfo('New pose in base_footprint')
    rospy.loginfo(new_pose_array)

