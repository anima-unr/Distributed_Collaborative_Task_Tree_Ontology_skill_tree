#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <cstdlib>
#include <blob_vision/Blob.h>
#include <blob_vision/Blob_array.h>
#include "geometry_msgs/PointStamped.h"
#include <tf/transform_listener.h>
#include "std_msgs/String.h"

///////////////////////////////////////////
// need to set up the message type so can do the code below!!!!!
//     map<string,Blob> current_location_;
    
//     so for publishing, could iterate through the current_location and publish the color and Blob as arrays??
     
//     class Blob 
// {
//   public:
//     int x, y, width, height, size;
// };
///////////////////////////////////////////

// ==========================================================


tf::TransformListener *t;


geometry_msgs::PointStamped transPoint(double x, double y, double z, const std::string old_frame, const std::string new_frame){
  // ros::Time now = ros::Time::now() + ros::Duration(1.0);
  ros::Time now = ros::Time(0);
  // tf::TransformListener t = new tf::TransformListener(ros::Duration(10.0), true);
  t->waitForTransform(new_frame, old_frame, now, ros::Duration(3.0));

  geometry_msgs::PointStamped pnt;
  pnt.header.frame_id = old_frame;
  pnt.header.stamp = now;
  pnt.point.x = x;
  pnt.point.y = y;
  pnt.point.z = z;

  // geometry_msgs::PoseStamped newPnt = t.transformPose(new_frame, pnt);
  geometry_msgs::PointStamped newPnt;
  t->transformPoint(new_frame, pnt, newPnt);

  std::cout << "\nTRANSFORM: " << newPnt << '\n';
  return newPnt;
}

// ==========================================================


///////////////////////////////////////////
// code that needs to get called in the pick and place imp right before it gets moved to pick
///////////////////////////////////////////

// void blobsCallback(const blob_vision::Blob_array::ConstPtr& msg){
void blobsCallback(const std_msgs::String::ConstPtr& msg){


ROS_INFO("I heard: [%s]", msg->data.c_str());

// figure out which object is being held

// launch subprocess so can track in background
pid_t pid;
pid = fork();
if(pid == 0) { // child process
    setpgid(getpid(), getpid());
    //system("roslaunch vision_manip_pipeline jb_tutorial1.launch");

    // loop until told to stop
    while(1){  
    printf("FROM SUBPROCESS");
    // system("ls");
    // sleep(1);

        // iterate through the topic and search for the object and its position
        // GET THESE FROM THE MESSAGE INSTEAD!!!!!
        int x = 0;
        int y = 0;
        int z = 0;

        // transform position to the 3d coords based on base link
        geometry_msgs::PointStamped transPnt = transPoint(x, y, z, "/FOREARM SOMETHING HERE", "/base_link");

        // get position of gripper

        // check if distance between object and gripper are too large
            // throw flag that object was dropped!!!
    }

}
else {

///////////////////////////////////////////
// code that needs to get called in the pick and place imp right after it gets placed
///////////////////////////////////////////

//stub for there to be something happening....
int i = 0;
while( i < 1000){
    printf("i%d ", i);
    i++;
}

// end subprocess
kill(-pid, SIGKILL);
printf("Subproces killed");
printf("killed process group %d\n", pid);
}

}

// =================================================
// =================================================
// =================================================
// =================================================

int main(int argc, char **argv) {

blob_vision::Blob blob;

// TODO: Remove this later to use the node handle from the grasping
ros::init(argc, argv, "listener");
ros::NodeHandle n;

// subscribe to the blob topic
ros::Subscriber sub = n.subscribe("blob_locs", 1000, blobsCallback);

ros::spin();

return 0;

}
