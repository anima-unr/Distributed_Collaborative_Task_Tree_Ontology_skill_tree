Running the pick and place:

roslaunch kinect2_bridge kinect2_bridge.launch publish_tf:=true depth_registration:=true

roslaunch moveit_check baxter_base_trans.launch

roslaunch ar_track_alvar pr2_indiv.launch

rosrun baxter_interface joint_trajectory_action_server.py

roslaunch baxter_moveit_config baxter_grippers.launch

roslaunch moveit_check object_position_server.launch

rosrun moveit_check test_moveit_tea_sandwich_scenario.py 

(you can find it in the moveit_check repo)


Running architecture:

roslaunch table_setting_demo multi_robot_task_demo_visionManip_baxter.launch

roslaunch remote_mutex table_setting_mutex_baxter.launch


Running chatbot for ontology:

sudo docker run -p 7474:7474 -p 7687:7687 --name SemanticMemory --rm -i -t stsbukhari/seedsemantic

Root@c993e94d0534:/# neo4j console

rosrun launching_file_from_web chatbot_v6.py

