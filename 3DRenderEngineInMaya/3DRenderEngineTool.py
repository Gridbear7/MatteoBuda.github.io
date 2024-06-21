import math
from Qt import QtWidgets, QtCore, QtGui, QtCompat
import os, sys
import maya.cmds as cmds
from maya import OpenMayaUI
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import numpy as np
import time

dirpathstr = r'D:\Scripts\GitHubPortfolioUploads\3DProjectionVisualizer'

resfile_pathstr = os.path.join(dirpathstr, "3DRenderEngine.rcc")
retval = QtCore.QResource.registerResource(resfile_pathstr)


def maya_main_window():
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class RenderEngineTool(QtWidgets.QDialog):
    def __init__(self):
        super(RenderEngineTool, self).__init__()
        path_to_ui = os.path.join(dirpathstr, "3DRenderEngine_UI.ui")
        QtCompat.loadUi(path_to_ui, baseinstance=self)

        self.setWindowTitle('3D Render Engine Tool')
        self.setFixedSize(400, 300)

        self.scale = 0.75
        self.timestep = 0.1
        self.distance = 4

        self.fov = 20  # field of view
        self.aspect = 4 / 3  # aspect ratio
        self.near = 0.1  # near clipping plane
        self.far = 500.0  # far clipping plane
        self.width = 20
        self.height = 20

        self.pos_edit_step = 0.2
        self.rot_edit_step = 20
        self.scl_edit_step = 0.2

        self.model_pos_x = 0.0
        self.model_pos_y = 0.0
        self.model_pos_z = 10.0

        self.model_rot_x = 0.0
        self.model_rot_y = 0.0
        self.model_rot_z = 0.0

        self.cam_pos_x = 0.0
        self.cam_pos_y = 0.0
        self.cam_pos_z = 0.0

        self.cam_rot_x = 0.0
        self.cam_rot_y = 0.0
        self.cam_rot_z = 0.0

        self.look_x = 0.0
        self.look_y = 0.0
        self.look_z = 1.0

        self.centerx = 0
        self.centery = 0

        # default shape vertices
        self.points = np.array([

            [-0.5, -0.5, -0.5, 1],
            [0.5, -0.5, -0.5, 1],
            [0.5, 0.5, -0.5, 1],
            [-0.5, 0.5, -0.5, 1],

            [-0.5, -0.5, 0.5, 1],
            [0.5, -0.5, 0.5, 1],
            [0.5, 0.5, 0.5, 1],
            [-0.5, 0.5, 0.5, 1]

        ])

        # Buffers and Collections
        self.pixel_grid = []
        self.frame_buffer = []

        # Button Connections
        self.pushButton_setup.clicked.connect(self.screen_setup)
        self.pushButton_draw.clicked.connect(self.draw_verts)
        self.pushButton_animation.clicked.connect(self.test_animation)
        self.pushButton_reset.clicked.connect(self.clear_pixels)
        self.pushButton_copy.clicked.connect(lambda : (self.copy_points(cmds.ls(sl=1)[0])))

        self.pushButton_scl_pos.clicked.connect(lambda : (self.edit_attr('scale', self.scl_edit_step)))
        self.pushButton_scl_neg.clicked.connect(lambda: (self.edit_attr('scale', self.scl_edit_step * -1)))

        self.pushButton_pos_pls_x.clicked.connect(lambda: (self.edit_attr('pos_x', self.scl_edit_step)))
        self.pushButton_pos_neg_x.clicked.connect(lambda: (self.edit_attr('pos_x', self.scl_edit_step * -1)))
        self.pushButton_pos_pls_y.clicked.connect(lambda: (self.edit_attr('pos_y', self.scl_edit_step)))
        self.pushButton_pos_neg_y.clicked.connect(lambda: (self.edit_attr('pos_y', self.scl_edit_step * -1)))
        self.pushButton_pos_pls_z.clicked.connect(lambda: (self.edit_attr('pos_z', self.scl_edit_step)))
        self.pushButton_pos_neg_z.clicked.connect(lambda: (self.edit_attr('pos_z', self.scl_edit_step * -1)))

        self.pushButton_rot_pls_x.clicked.connect(lambda: (self.edit_attr('rot_x', self.scl_edit_step)))
        self.pushButton_rot_neg_x.clicked.connect(lambda: (self.edit_attr('rot_x', self.scl_edit_step * -1)))
        self.pushButton_rot_pls_y.clicked.connect(lambda: (self.edit_attr('rot_y', self.scl_edit_step)))
        self.pushButton_rot_neg_y.clicked.connect(lambda: (self.edit_attr('rot_y', self.scl_edit_step * -1)))
        self.pushButton_rot_pls_z.clicked.connect(lambda: (self.edit_attr('rot_z', self.scl_edit_step)))
        self.pushButton_rot_neg_z.clicked.connect(lambda: (self.edit_attr('rot_z', self.scl_edit_step * -1)))

    def screen_setup(self):

        # Includes setup for screen, camera, and scene clearing

        # Delete all previous created nodes
        cmds.SelectAll()
        cmds.delete()

        # Setup camera, attributes, and look through
        cam = cmds.camera(name='user_cam')
        print(cam)
        cmds.lookThru(cam)
        cmds.setAttr(cam[0] + '.tz', 80)
        cmds.refresh()

        for x in range(self.width):
            row = []
            for y in range(self.height):
                # Setup cube and transformations
                cube = cmds.polyCube()
                cmds.setAttr(cube[0] + '.tx', (1 / 2 * self.width) - x * 1.05)
                cmds.setAttr(cube[0] + '.ty', (3 / 4 * self.height) - y * 1.05)
                time.sleep(0.0005)
                cmds.refresh()

                # Create material
                lambert = cmds.shadingNode('lambert', name='lambert_' + cube[0], asShader=True)

                # Create shading group
                shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)

                # Assign the Lambert material to the shading group
                cmds.connectAttr(lambert + '.outColor', shading_group + '.surfaceShader', force=True)

                # Assign the shading group to the cube
                cmds.sets(cube[0], edit=True, forceElement=shading_group)

                # Add info to pixel list
                row.append([cube, lambert, shading_group])
            self.pixel_grid.append(row)


    def draw_verts(self):

        projected = []
        vertex_buffer = []


        # Clear old pixels in frame_buffer from screen
        self.clear_pixels()


        # reset frame buffer
        self.frame_buffer = []

        for vert in self.points:

            if len(vertex_buffer) == 3:  # once it reaches 3 vertices, it will be reset. problem is you are only able to access z
                vertex_buffer = []

            cam_rot_rad_x = np.radians(self.cam_rot_x)
            cam_rot_rad_y = np.radians(self.cam_rot_y)
            cam_rot_rad_z = np.radians(self.cam_rot_z)

            # Transform matrices

            rotationX = np.array([

                [1, 0, 0, 0],
                [0, np.cos(self.model_rot_x), -np.sin(self.model_rot_x), 0],
                [0, np.sin(self.model_rot_x), np.cos(self.model_rot_x), 0],
                [0, 0, 0, 1]

            ])

            rotationY = np.array([

                [np.cos(self.model_rot_y), 0, -np.sin(self.model_rot_y), 0],
                [0, 1, 0, 0],
                [np.sin(self.model_rot_y), 0, np.cos(self.model_rot_y), 0],
                [0, 0, 0, 1]

            ])

            rotationZ = np.array(
                [

                    [np.cos(self.model_rot_z), -np.sin(self.model_rot_z), 0, 0],
                    [np.sin(self.model_rot_z), np.cos(self.model_rot_z), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]

                ])

            scale_matrix = np.array([
                [self.scale, 0, 0, 0],
                [0, self.scale, 0, 0],
                [0, 0, self.scale, 0],
                [0, 0, 0, 1]
            ])

            translation_matrix = np.array([
                [1, 0, 0, self.model_pos_x],
                [0, 1, 0, self.model_pos_y],
                [0, 0, 1, self.model_pos_z],
                [0, 0, 0, 1]
            ])

            # Intrinsic parameters
            focal_length = 800  # in pixels
            principal_point = (320, 240)  # in pixels
            aspect_ratio = 1.0  # width/height

            # Create intrinsic matrix
            intrinsic_camera_matrix = np.array([
                [focal_length, 0, principal_point[0], 0],
                [0, focal_length * aspect_ratio, principal_point[1], 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])

            # Extrinsic Camera matrices

            # Define rotation matrix (R) and translation vector (t)
            matrix_cam_rot_x = np.array([
                [1, 0, 0],
                [0, np.cos(cam_rot_rad_x), -np.sin(cam_rot_rad_x)],
                [0, np.sin(cam_rot_rad_x), np.cos(cam_rot_rad_x)]
            ])

            matrix_cam_rot_y = np.array([
                [np.cos(cam_rot_rad_y), 0, np.sin(cam_rot_rad_y)],
                [0, 1, 0],
                [-np.sin(cam_rot_rad_y), 0, np.cos(cam_rot_rad_y)]
            ])

            matrix_cam_rot_z = np.array([
                [np.cos(cam_rot_rad_z), -np.sin(cam_rot_rad_z), 0],
                [np.sin(cam_rot_rad_z), np.cos(cam_rot_rad_z), 0],
                [0, 0, 1]
            ])

            matrix_cam_rot = np.dot(matrix_cam_rot_z, np.dot(matrix_cam_rot_y, matrix_cam_rot_x))
            matrix_cam_pos = np.array([0, 0, 1])

            # Create 4x4 camera matrix
            camera_matrix = np.eye(4)
            camera_matrix[:3, :3] = matrix_cam_rot
            camera_matrix[:3, 3] = matrix_cam_pos

            converted_vert = np.array([  # convert to 4x1 column vector
                [vert[0]],
                [vert[1]],
                [vert[2]],
                [vert[3]]
            ])

            rotatedY = np.matmul(rotationY, vert)
            rotatedX = np.matmul(rotationX, rotatedY)
            rotatedZ = np.matmul(rotationZ, rotatedX)
            scaled = np.matmul(scale_matrix, rotatedZ)
            translated = np.matmul(translation_matrix, scaled)
            view = np.matmul(camera_matrix, translated)

            # calculate the top, bottom, left, and right values for the frustum
            t = self.near * math.tan(self.fov / 2)
            b = -t
            r = t * self.aspect
            l = -r

            persp_projection_matrix = np.array([
                [2 * self.near / (r - l), 0, (r + l) / (r - l), 0],
                [0, 2 * self.near / (t - b), (t + b) / (t - b), 0],
                [0, 0, -(self.far + self.near) / (self.far - self.near),
                 -2 * self.far * self.near / (self.far - self.near)],
                [0, 0, -1, 0]
            ])

            # multiply the persp against the translated vertices
            persp_projection_vertices = np.matmul(persp_projection_matrix,
                                                  view)

            projected_vertices = persp_projection_vertices
            projected.append(projected_vertices)  # add vertices into my  list

            screen_coord_x = ((projected_vertices[0] / projected_vertices[3]) * self.width / 2 + self.width / 2) - (
                    self.width / 2)  # needs offsets to centre the camera
            screen_coord_y = ((projected_vertices[1] / projected_vertices[3]) * self.height / 2 + self.height / 2) - (
                    self.height / 2)
            screen_coord_z = projected_vertices[3]

            screen_coord_edit_x = int(10 * (screen_coord_x + 1.0))
            screen_coord_edit_y = int(10 * (screen_coord_y + 1.0))
            self.frame_buffer.append([screen_coord_edit_x, screen_coord_edit_y, 'RED'])



        # this is outside of scope of vertex projecting loop

        for projected_coordinate in self.frame_buffer:
            self.point(projected_coordinate[0], projected_coordinate[1])
            print('from draw', self.frame_buffer)

        # completed drawing all verts
        time.sleep(0.075)
        cmds.refresh()

    def point(self, x, y):

        try:
            cube_mat = self.pixel_grid[x][y][1]
            cmds.setAttr(cube_mat + '.color', 0.1, 0.1, 0.1)

        except:
            print('skipping vert draw')


    def test_animation(self):

        for i in range(40):
            self.model_rot_z += 3
            self.model_rot_y += 3
            self.model_rot_x += 3

            self.draw_verts()


    def copy_points(self, object_name):
        # Get the list of vertices of the object
        vertices = cmds.ls(object_name + '.vtx[*]', flatten=True)

        # Initialize a list to store vertex positions
        vertex_positions = []

        # Clear self.points
        self.points = []

        # Iterate through each vertex and query its position
        for vertex in vertices:
            position = cmds.xform(vertex, query=True, translation=True, worldSpace=True)
            fourth_component = 1
            position.append(fourth_component)
            self.points.append(position)


    def clear_pixels(self):

        for old_pixel in self.frame_buffer:
            # item in frame_buffer looks like [[x, y, col], [x,y,col], ...]
            # item in pixel_grid looks like [[cube_transform, cube_material, cube_SG],[cube_transform, cube_material, cube_SG],...]

            try:

                old_pixel_x = old_pixel[0]
                old_pixel_y = old_pixel[1]
                cube_mat = self.pixel_grid[old_pixel_x][old_pixel_y][1]

                cmds.setAttr(cube_mat + '.color', 0.5, 0.5, 0.5)

            except:

                pass




    def edit_attr(self, attribute, direction):

        if attribute == 'scale':
            self.scale += direction

        elif attribute == 'pos_x':
            self.model_pos_x += direction

        elif attribute == 'pos_y':
            self.model_pos_y += direction

        elif attribute == 'pos_z':
            self.model_pos_z += direction

        elif attribute == 'rot_x':
            self.model_rot_x += direction

        elif attribute == 'rot_y':
            self.model_rot_y += direction

        elif attribute == 'rot_z':
            self.model_rot_z += direction

        self.draw_verts()


MyWindow = RenderEngineTool()
MyWindow.show()


