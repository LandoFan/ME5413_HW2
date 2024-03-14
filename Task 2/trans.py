import rosbag
from tf.transformations import quaternion_multiply, quaternion_matrix, quaternion_from_matrix
import numpy as np

# Lidar to camera coordinate system conversion matrix
# Trans = np.array([[0, -1, 0, 0],   
#               [0, 0, -1, -0.08],
#               [1, 0, 0, -0.27],
#               [0, 0, 0, 1]]) 
transform_matrix = np.array([
    [ 7.533745e-03, -9.999714e-01, -6.166020e-04, -4.069766e-03],
    [ 1.480249e-02,  7.280733e-04, -9.998902e-01, -7.631618e-02],
    [ 9.998621e-01,  7.523790e-03,  1.480755e-02, -2.717806e-01],
    [0, 0, 0, 1]
])

bag_path = '/home/zachary/.ros/my_odometry_bag.bag'
topic_name = '/aft_mapped_to_init'
output_file = 'output_tum_format.txt'

# contain position and timestamps
timestamps_and_poses = []

with rosbag.Bag(bag_path, 'r') as bag:
    base_time = None
    for topic, msg, t in bag.read_messages(topics=[topic_name]):
        # calculate relative timestamps
        if base_time is None:
            base_time = t.to_sec()
        relative_timestamp = t.to_sec() - base_time
        
        # Get position and rotation quaternions
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        q = [orientation.x, orientation.y, orientation.z, orientation.w]
        translation = [position.x, position.y, position.z, 1]
        rotation_matrix = quaternion_matrix(q)
        
        # Synthesize the complete transformation matrix
        transform_matrix_full = rotation_matrix
        transform_matrix_full[:3, 3] = translation[:3]
        
        # Application Conversion Matrix
        transformed_matrix = np.dot(transform_matrix, transform_matrix_full)
        transformed_translation = transformed_matrix[:3, 3]
        transformed_rotation = quaternion_from_matrix(transformed_matrix)
        
        # Save converted timestamps and bit positions
        timestamps_and_poses.append((relative_timestamp, *transformed_translation, *transformed_rotation))

# write to a file
with open(output_file, 'w') as f:
    for timestamp, x, y, z, qx, qy, qz, qw in timestamps_and_poses:
        f.write(f"{timestamp} {x} {y} {z} {qx} {qy} {qz} {qw}\n")

print(f"data has been saved {output_file}")
