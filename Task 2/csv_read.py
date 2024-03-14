import pandas as pd
import numpy as np
import tf.transformations as tf

# 文件路径
f = r"my_odometry_bag/laser_odom_to_init.csv"

# 读取 CSV 文件
df = pd.read_csv(f)

# 显示 DataFrame 的前几行
print(df.head())
time_data = df['Time']
positionX = df['pose.pose.position.x']
positionY = df['pose.pose.position.y']
positionZ = df['pose.pose.position.z']
orientationX = df['pose.pose.orientation.x']
orientationY = df['pose.pose.orientation.y']
orientationZ = df['pose.pose.orientation.z']
orientationW = df['pose.pose.orientation.w']

# print(time_data)
# print(positionX)
# print(orientationX)
# T = np.array([[0, -1, 0, 0],   #lidar 
#               [0, 0, -1, -0.08],
#               [1, 0, 0, 0.27],
#               [0, 0, 0, 1]]) 
# Trans = np.array([[0, -1, 0, 0],   #lidar 
#               [0, 0, -1, -0.08],
#               [1, 0, 0, 0.27],
#               [0, 0, 0, 1]]) 
Trans = np.array([[ 7.533745e-03, -9.999714e-01, -6.166020e-04, -4.069766e-03],
                    [ 1.480249e-02,  7.280733e-04, -9.998902e-01, -7.631618e-02],
                    [ 9.998621e-01,  7.523790e-03,  1.480755e-02, -2.717806e-01],
                    [0, 0, 0, 1]])


positions = np.column_stack((positionX, positionY, positionZ, np.ones_like(positionX)))

# 进行坐标变换
transformed_positions = np.dot(Trans, positions.T).T

# 提取变换后的位置坐标
transformed_positionX = transformed_positions[:, 0]
transformed_positionY = transformed_positions[:, 1]
transformed_positionZ = transformed_positions[:, 2]
# 文件路径
output_file = "output_tum.txt"

# 打开文件以写入模式
with open(output_file, 'w') as file:
    # 写入列标题
    # file.write("Time, Position X, Position Y, Position Z, Orientation X, Orientation Y, Orientation Z, Orientation W\n")
    
    # 逐行写入数据
    for i in range(len(time_data)):
        line = "{:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(time_data[i] - time_data[0], 
                                                                                transformed_positionX[i], transformed_positionY[i], transformed_positionZ[i], 
                                               orientationX[i], orientationY[i], orientationZ[i], orientationW[i])
        file.write(line)
        
print("数据已写入到文件:", output_file)