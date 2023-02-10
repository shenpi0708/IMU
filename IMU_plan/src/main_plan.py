#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion,Point, PoseStamped,Pose
from nav_msgs.msg import Path
from visualization_msgs.msg import Marker

class PlanPath:
    def callback(self,data):
        
        self.path.header.frame_id="map"
        self.path.header.stamp = rospy.Time.now()
        self.poses.header.stamp = rospy.Time.now()
        self.V=[self.V[0]+data.linear_acceleration.x,self.V[1]+data.linear_acceleration.y,self.V[2]+data.linear_acceleration.z]    
        self.poses.pose.position.x=self.poses.pose.position.x+self.V[0]/100
        self.poses.pose.position.y=self.poses.pose.position.y+self.V[1]/100
        self.poses.pose.position.z=self.poses.pose.position.z+self.V[2]/100
        self.poses.pose.orientation.x=data.orientation.x
        self.poses.pose.orientation.y=data.orientation.y
        self.poses.pose.orientation.z=data.orientation.z
        self.poses.pose.orientation.w=data.orientation.w
        self.marker()
        
    def marker(self):
        marker = Marker()

        marker.header.frame_id = "/map"
        marker.header.stamp = rospy.Time.now()

        # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
        marker.type = 2
        marker.id = 0

        # Set the scale of the marker
        marker.scale.x = 1.0
        marker.scale.y = 1.0
        marker.scale.z = 1.0

        # Set the color
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        # Set the pose of the marker
        marker.pose.position.x = self.poses.pose.position.x
        marker.pose.position.y = self.poses.pose.position.y
        marker.pose.position.z = self.poses.pose.position.z
        marker.pose.orientation.x = self.poses.pose.orientation.x
        marker.pose.orientation.y = self.poses.pose.orientation.y
        marker.pose.orientation.z = self.poses.pose.orientation.z
        marker.pose.orientation.w = self.poses.pose.orientation.w

        self.marker_pub.publish(marker)
    def __init__(self):
        self.V=[0,0,0]
        self.path=Path()
        self.poses=PoseStamped()
        self.poses.header.frame_id="map"
        #self.path.poses.header.frame_id="map"
        rospy.init_node('plan_originaldata', anonymous=True) 
        self.marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)  
        rospy.Subscriber("Imu", Imu, self.callback)

        rospy.spin()

if __name__ == '__main__':
    PlanPath()