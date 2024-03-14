import open3d as o3d
import numpy as np

point = o3d.io.read_point_cloud("output_cloud_margin.pcd")

o3d.visualization.draw_geometries([point])

#open3d显示的时候有个bug 要把python  pycharm设置为高性能  系统显示里 图形设置
