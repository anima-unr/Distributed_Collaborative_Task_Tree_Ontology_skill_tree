#include "ros/ros.h"
#include "std_msgs/String.h"
#include <blob_vision/Blob.h>
#include <blob_vision/Blob_array.h>
#include <string>
#include <cstdlib>
#include <iostream>
#include <fstream>

using namespace std;

struct blob {
	int x, y;
	double width, height, size;
	string name;
};

struct blob OBJ[4];
int PLACE;

void callBack(const blob_vision::Blob_array::ConstPtr& msg)
{
	string names[4] = {"yellow", "blue", "green", "red"};
	for (int i=0; i<4; i++) {
		if(msg->blobs[i].obj_name == names[i]) {
			OBJ[i].name = names[i];
			OBJ[i].x = msg->blobs[i].x;
			OBJ[i].y = msg->blobs[i].y;
			OBJ[i].width = msg->blobs[i].width;
			OBJ[i].height = msg->blobs[i].height;
			OBJ[i].size = msg->blobs[i].size;
		}
	}
}

void tracking(std::ofstream& ofile, struct blob objs[10]) 
{
	cout<< "hello";
        cout << objs[0].name;
	for (int i=0; i<4; i++) {
		if (OBJ[i].name != "") { 
			if (PLACE <= 1) {
				objs[PLACE] = OBJ[i];
				ofile << objs[PLACE].name << " " << objs[PLACE].x << " " << objs[PLACE].y << '\n' << endl;
				PLACE++;
			} else {
				if (objs[0].name == OBJ[i].name) {
					if (abs(objs[0].x - OBJ[i].x) > 110 or abs(objs[0].y - OBJ[i].y) > 110) {
						objs[PLACE] = OBJ[i];
						ofile << objs[PLACE].name << " " << objs[PLACE].x << " " << objs[PLACE].y << '\n' << endl;
						objs[0].x = objs[PLACE].x;
						objs[0].y = objs[PLACE].y;
						PLACE++;
					}
				} else if (objs[1].name == OBJ[i].name) {
					if (abs(objs[1].x - OBJ[i].x) > 110 or abs(objs[1].y - OBJ[i].y) > 110) {
						objs[PLACE] = OBJ[i];
						ofile << objs[PLACE].name << " " << objs[PLACE].x << " " << objs[PLACE].y << '\n' << endl;
						objs[1].x = objs[PLACE].x;
						objs[1].y = objs[PLACE].y;
						PLACE++;
					}
				} else if (objs[2].name == OBJ[i].name) {
					if (abs(objs[2].x - OBJ[i].x) > 110 or abs(objs[2].y - OBJ[i].y) > 110) {
						objs[PLACE] = OBJ[i];
						ofile << objs[PLACE].name << " " << objs[PLACE].x << " " << objs[PLACE].y << '\n' << endl;
						objs[2].x = objs[PLACE].x;
						objs[2].y = objs[PLACE].y;
						PLACE++;
					}
				} else if (objs[3].name == OBJ[i].name) {
					if (abs(objs[3].x - OBJ[i].x) > 110 or abs(objs[3].y - OBJ[i].y) > 110) {
						objs[PLACE] = OBJ[i];
						ofile << objs[PLACE].name << " " << objs[PLACE].x << " " << objs[PLACE].y << '\n' << endl;
						objs[3].x = objs[PLACE].x;
						objs[3].y = objs[PLACE].y;
						PLACE++;
					}
				}
				 /*else {
					objs[PLACE] = OBJ[i];
					ofile << objs[PLACE].name << " " << objs[PLACE].x << " " << objs[PLACE].y << '\n' << endl;
					PLACE++;
				}*/
			}
		}
	}
}

void sequences(std::ofstream& ofile2, struct blob objs[10]) {
	ofile2 << endl << "task sequence key:\n" << "1 = yellow\n" << "2 = blue\n" << endl;
	ofile2 << "[";
	for (int i=2; i<10; i++) {
		if (objs[i].name == "yellow") {
			ofile2 << "1";
		} else if (objs[i].name == "blue") {
			ofile2 << "2";
		}
	}
	ofile2 << "]" << endl;
}

int main(int argc, char *argv[])
{
	ros::init(argc, argv, "sequence_builder");
	ros::NodeHandle n;
	ros::Subscriber sub = n.subscribe("/blob_locs", 1000, callBack);
	string filename, filename2;
	cout << "output file name: ";
	cin >> filename;
	cout << "output file name2: ";
	cin >> filename2;
	struct blob objs[10];
        cout << objs[0].name << "+" << objs[1].name;
	ofstream ofile;
	ofstream ofile2;
	ofile.open(filename);
	ros::Rate r(100);
	while (ros::ok())
	{
		tracking(ofile, objs);
		ros::spinOnce();
		r.sleep();
	}
	ofile.close();
	ofile2.open(filename2, std::ios_base::app); //appends
	sequences(ofile2, objs);
	ofile2.close();
	return 0;
}
