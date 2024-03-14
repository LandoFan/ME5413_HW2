import open3d as o3d
import numpy as np
import os

# 文件夹路径，包含所有的PCD文件
folder_path = '/home/zachary/.ros'
# 输出文件名
output_filename = 'merged.pcd'

# 读取文件夹中的所有PCD文件
pcd_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pcd')]
combined_pcd = None

# 初始化进度变量
total_files = len(pcd_files)
processed_files = 0

# 合并PCD文件
for filename in pcd_files:
    print(f"Processing {filename} ({processed_files+1}/{total_files})...")
    pcd = o3d.io.read_point_cloud(filename)
    if combined_pcd is None:
        combined_pcd = pcd
    else:
        combined_pcd.points = o3d.utility.Vector3dVector(np.vstack((np.asarray(combined_pcd.points), np.asarray(pcd.points))))
    processed_files += 1

# 保存合并后的PCD文件
o3d.io.write_point_cloud(output_filename, combined_pcd)
print(f'Merged PCD file saved as {output_filename}')
