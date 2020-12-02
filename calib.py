import numpy as np
import matplotlib.pyplot as plt
from kitti_utils.calibration import Calibration
from PIL import Image
from mayavi import mlab
import math

def draw_point_cloud(points, label_data, colors=None):
    '''Draw draw point cloud.

    Args:
      pc: (np.array) point cloud, sized (n,3) of XYZ.
      boxes: (list(np.array)) list of 3D bounding boxes, each sized [8,3].
      colors: (list(tuple)) list of RGB colors.
    '''

    fig = mlab.figure(figure=None, bgcolor=(0, 0, 0),
                      fgcolor=None, engine=None, size=(1600, 1000))
    
    color = points[:, 2]

  
    mlab.points3d(points[:, 0], points[:, 1], points[:, 2], color, color=None,
                  mode='point', colormap='Oranges', scale_factor=0.3, figure=fig)
    

    for i, data in enumerate(label_data):
        length = float(data[10])
        height = float(data[8])
        width = float(data[9])
        
        x = float(data[13])
        y = float(data[11])
        z = float(data[12])
        pi = float(data[14])

        y *= -1
        z *= -1
        #print(x, y, z)
        vertex = np.array([
            [x - length / 2, y-width/2, z],
            [x + length / 2, y-width/2, z],
            [x + length / 2, y+width/2, z],
            [x - length / 2, y+width/2, z],
            [x - length / 2, y-width/2, z+height],
            [x + length / 2, y-width/2, z+height],
            [x + length / 2, y+width/2, z+height],
            [x - length / 2, y+width/2, z+height],
        ])
        vertex = rotation(x, y, z, vertex, pi)
        print(vertex.shape)
        '''
        points_in_3dbox = np.array([point for point in points if check_point_in_3dbox(point, vertex)])
        if len(points_in_3dbox) == 0:
            continue
        color = points_in_3dbox[:, 2]

        mlab.points3d(points_in_3dbox[:, 0], points_in_3dbox[:, 1], points_in_3dbox[:, 2], color, color=None,
           
                  mode='point', colormap='Oranges', scale_factor=0.3, figure=fig)
        '''

        mlab.points3d(vertex[:, 0], vertex[:, 1], vertex[:, 2], color=(0, 1, 1), mode='sphere', scale_factor=0.2)


    # draw origin
    mlab.points3d(0, 0, 0, color=(1, 1, 1), mode='sphere', scale_factor=0.2)
    mlab.view(azimuth=180, elevation=70, focalpoint=[
              12.0909996, -1.04700089, -2.03249991], distance=62.0, figure=fig)

    mlab.show()


def rotation(x, y, z, vertex_list, rad):
    #rad = deg * np.pi / 180
    rad = -math.pi / 2 - rad
    rot = np.array([[np.cos(rad), -np.sin(rad)],
                    [np.sin(rad), np.cos(rad)]])
    for vertex in vertex_list:
        vertex_x = vertex[0] - x
        vertex_y = vertex[1] - y
        rotated_vertex = np.dot(rot, np.array([vertex_x, vertex_y]))
        vertex[0] = rotated_vertex[0] + x
        vertex[1] = rotated_vertex[1] + y
    
    return vertex_list


def check_point_in_3dbox(point, vertex_list):
    vertex_list = vertex_list[:4]
    vertex_list = np.append(vertex_list, vertex_list[0]).reshape(5, 3)
    print(vertex_list)

    outer_count = 0

    for i in range(4):
        x1 = vertex_list[i, 0]
        x2 = vertex_list[i + 1, 0]
        y1 = vertex_list[i, 1]
        y2 = vertex_list[i + 1, 1]
        px = point[0]
        py = point[1]
        outer = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        if outer >= 0:
            outer_count += 1
    if outer_count == 0 or outer_count == 4:
        return True
    else:
        return False
    
        
        


        

if __name__ == "__main__":
    with open('label/002155.txt', 'r') as f:
        lines = f.readlines()
    label_data = [line.strip().split(' ') for line in lines if line[0] != 'DontCare']
    label_data = [data for data in label_data if data[0] != 'DontCare']
    #print(label_data)
    points = np.fromfile('velodyne/002155.bin', dtype=np.float32, count = -1).reshape([-1, 4])
    draw_point_cloud(points, label_data)



    '''
    png_img = np.array(Image.open('image2/000003.png'))
    HEIGHT = png_img.shape[0]
    WIDTH = png_img.shape[1]
    #print(HEIGHT, WIDTH)


    calibration = Calibration('calib/000003.txt')
    points = np.fromfile('velodyne/000003.bin', dtype=np.float32, count = -1).reshape([-1, 4])
    print(points.shape)
    cam0 = calibration.project_velo_to_ref(points)

    cam2 = calibration.project_ref_to_cam(cam0)
    #print(cam0)
    #print(cam2)
    img = calibration.project_cam_to_img(cam2)
    #print(img)
    #draw_point_cloud(points)
    #print(img.shape)
    points_in_pic = []
    for i, point in enumerate(points):
        x = int(img[i][0])
        y = int(img[i][1])
        #print(x, y)
        if 0<= x < WIDTH and 0<= y < HEIGHT and point[0] >= 0:
            points_in_pic.append(point)
        #else:
        #    points_in_pic.append(np.zeros(3))
    points_in_pic_array = np.stack(points_in_pic)
    '''