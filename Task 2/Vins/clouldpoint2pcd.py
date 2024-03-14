
import rosbag
import numpy as np
import open3d as o3d

bag_file = "/home/lando/vins_odometry_bag.bag"
output_pcd_file = "output_cloud_margin.pcd"

# 创建一个空的点云对象
all_points = []

# 读取 ROS Bag 文件
with rosbag.Bag(bag_file, "r") as bag:
    # 遍历 Bag 文件中的所有消息
    for topic, msg, t in bag.read_messages():
        # 检查消息类型是否为点云消息
        if topic.endswith("/loop_fusion/margin_cloud_loop_rect"):  # 替换为您实际的点云话题名称
            # 提取点云数据并添加到列表中
            for point in msg.points:
                all_points.append([point.x, point.y, point.z])

# 将所有点云数据转换为 Open3D 点云对象
cloud = o3d.geometry.PointCloud()
cloud.points = o3d.utility.Vector3dVector(all_points)

# 保存 Open3D 点云为 PCD 文件
o3d.io.write_point_cloud(output_pcd_file, cloud)
print("All point cloud data saved to", output_pcd_file)


