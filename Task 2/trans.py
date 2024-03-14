import rosbag
from tf.transformations import quaternion_multiply, quaternion_matrix, quaternion_from_matrix
import numpy as np

# 激光雷达到相机坐标系的转换矩阵（根据你的实际情况替换）
transform_matrix = np.array([
    [ 7.533745e-03, -9.999714e-01, -6.166020e-04, -4.069766e-03],
    [ 1.480249e-02,  7.280733e-04, -9.998902e-01, -7.631618e-02],
    [ 9.998621e-01,  7.523790e-03,  1.480755e-02, -2.717806e-01],
    [0, 0, 0, 1]
])

bag_path = '/home/zachary/.ros/my_odometry_bag.bag'
topic_name = '/aft_mapped_to_init'
output_file = 'output_tum_format.txt'

# 用于存储转换后的时间戳和位姿的列表
timestamps_and_poses = []

with rosbag.Bag(bag_path, 'r') as bag:
    base_time = None
    for topic, msg, t in bag.read_messages(topics=[topic_name]):
        # 计算相对时间戳
        if base_time is None:
            base_time = t.to_sec()
        relative_timestamp = t.to_sec() - base_time
        
        # 获取位置和旋转四元数
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        q = [orientation.x, orientation.y, orientation.z, orientation.w]
        translation = [position.x, position.y, position.z, 1]
        rotation_matrix = quaternion_matrix(q)
        
        # 合成完整的变换矩阵
        transform_matrix_full = rotation_matrix
        transform_matrix_full[:3, 3] = translation[:3]
        
        # 应用转换矩阵
        transformed_matrix = np.dot(transform_matrix, transform_matrix_full)
        transformed_translation = transformed_matrix[:3, 3]
        transformed_rotation = quaternion_from_matrix(transformed_matrix)
        
        # 保存转换后的时间戳和位姿
        timestamps_and_poses.append((relative_timestamp, *transformed_translation, *transformed_rotation))

# 写入文件
with open(output_file, 'w') as f:
    for timestamp, x, y, z, qx, qy, qz, qw in timestamps_and_poses:
        f.write(f"{timestamp} {x} {y} {z} {qx} {qy} {qz} {qw}\n")

print(f"数据已转换并保存到 {output_file}")