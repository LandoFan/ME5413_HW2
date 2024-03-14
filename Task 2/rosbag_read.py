import bagpy
from bagpy import bagreader
import pandas as pd
import numpy as np
import rospy
import tf.transformations as tf

fpath = r"my_odometry_bag.bag"
b = bagreader(fpath)
#查看所有的topics

print(b.topic_table)
# topics = b.topic_table#['Topics']
odometry_path = b.message_by_topic('/laser_odom_path')
print('odom_path',odometry_path)
odometry_path = np.array(odometry_path)
odometry_data = b.message_by_topic('/laser_odom_to_init')
odometry_data = np.array(odometry_data)

print('odom_path',odometry_path)
print('odometry_data',odometry_data)