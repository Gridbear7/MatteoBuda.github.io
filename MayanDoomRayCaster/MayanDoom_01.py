import maya.cmds as cmds
import time
import math
from Qt import QtWidgets, QtCore, QtGui, QtCompat
import os, sys
import maya.cmds as cmds
from maya import OpenMayaUI
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

try:
    dirpathstr = os.path.dirname(__file__)

except NameError as e:
    dirpathstr = r'D:\Scripts\rendering\RayCaster_A'

if True:
    resfile_pathstr = os.path.join(dirpathstr, "MayanDoom_resource_file.rcc")
    retval = QtCore.QResource.registerResource(resfile_pathstr) # Vital for registering a new rcc

def maya_main_window():
    main_window_ptr=OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

inMaya =  cmds and hasattr(cmds, "scriptJob")
class MayanDoom(QtWidgets.QDialog):
    def __init__(self):
        super(MayanDoom, self).__init__()
        path_to_ui = os.path.join(dirpathstr, "MayanDoom_UI.ui")
        QtCompat.loadUi(path_to_ui, baseinstance=self)

        self.setWindowTitle('MayanDoom')
        self.setFixedSize(600, 300)


        # Variables
        self.env_scanline_list = []
        self.sub_list = []
        self.scanline_list = []
        self.ground_panel = []
        self.sky_panel = []
        self.start_time = time.time()
        self.end_time = None
        self.score = None
        self.wall_color_R = 0.5
        self.wall_color_G = 0.5
        self.wall_color_B = 0.5

        self.map_1 = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 1],
            [1, 1, 2, 1, 1, 1, 1],
        ]

        # start pos 5,1 rot 180
        self.map_2 = [
            [1, 1, 1, 1, 1, 1, 1],
            [2, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]

        # start pos 1,1 rot 270
        self.map_3 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 1, 0, 1, 1, 0, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 1, 0, 0, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.map_template_A = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]

        self.map_template_B = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.current_map = self.map_1

        # pos_x, pox_y = (cmds.getAttr(), cmds.getAttr()
        self.pos_x, self.pos_y = (1.3, 2.3)
        self.player_rot_deg = 0
        self.fov = self.spinBox_FOV.value()
        self.player_mov_step = 0.2
        self.current_map_pos_x = 1.3
        self.current_map_pos_y = 2.3
        self.current_map_rot = 0

        self.env_screen_setup()
        self.pushButton_start.clicked.connect(self.render_env)
        self.pushButton_reset.clicked.connect(self.reset_game)
        self.pushButton_interact.clicked.connect(self.interact_door)
        self.pushButton_help.clicked.connect(self.help_menu)
        self.spinBox_val_1.valueChanged.connect(self.render_env)
        self.spinBox_val_2.valueChanged.connect(self.render_env)
        self.pushButton_help.hide()

        # Movement controls
        self.pushButton_player_rot_cw.clicked.connect(self.edit_attr_rot_cw)
        self.pushButton_player_rot_ccw.clicked.connect(self.edit_attr_rot_ccw)
        self.pushButton_player_mov_forward.clicked.connect(self.edit_attr_mov_forward)
        self.pushButton_player_mov_backward.clicked.connect(self.edit_attr_mov_backward)
        self.pushButton_player_mov_right.clicked.connect(self.edit_attr_mov_right)
        self.pushButton_player_mov_left.clicked.connect(self.edit_attr_mov_left)

        # Pixel list item format : [[cube_transform, cube_shape], material, shading group, scanline group]

    def edit_attr_mov_forward(self):

        direction_rad = math.radians(self.player_rot_deg - 180)
        if self.collision_check(direction_rad) == 0:
            self.pos_x = self.pos_x - self.player_mov_step * math.cos(direction_rad)
            self.pos_y = self.pos_y + self.player_mov_step * math.sin(direction_rad)
        self.render_env()

    def edit_attr_mov_backward(self):

        direction_rad = math.radians(self.player_rot_deg - 0)
        if self.collision_check(direction_rad) == 0:
            self.pos_x = self.pos_x - self.player_mov_step * math.cos(direction_rad)
            self.pos_y = self.pos_y + self.player_mov_step * math.sin(direction_rad)
        self.render_env()

    def edit_attr_mov_right(self):

        direction_rad = math.radians(self.player_rot_deg - 90)
        if self.collision_check(direction_rad) == 0:
            self.pos_x = self.pos_x - self.player_mov_step * math.cos(direction_rad)
            self.pos_y = self.pos_y + self.player_mov_step * math.sin(direction_rad)
        self.render_env()

    def edit_attr_mov_left(self):

        direction_rad = math.radians(self.player_rot_deg - 270)
        if self.collision_check(direction_rad) == 0:
            self.pos_x = self.pos_x - self.player_mov_step * math.cos(direction_rad)
            self.pos_y = self.pos_y + self.player_mov_step * math.sin(direction_rad)
        self.render_env()

    def edit_attr_rot_cw(self):

        self.player_rot_deg += 10
        self.render_env()

    def edit_attr_rot_ccw(self):

        self.player_rot_deg -= 10
        self.render_env()

    def reset_game(self):

        self.pos_x, self.pos_y = (self.current_map_pos_x, self.current_map_pos_y)
        self.player_rot_deg = self.current_map_rot
        self.fov = self.spinBox_FOV.value()
        self.env_screen_setup()
        self.color_planes()
        self.render_env()

    def interact_door(self):

        # check 0.7 units in front to see what wall value is
        direction_rad = math.radians(self.player_rot_deg - 180)
        wall_value_x = self.pos_x - 0.7 * math.cos(direction_rad)
        wall_value_y = self.pos_y + 0.7 * math.sin(direction_rad)

        wall_value = self.current_map[int(wall_value_x)][int(wall_value_y)]

        # door logic for each level, referenced when door interaction is triggered
        if wall_value == 2:  # is a door

            if self.current_map == self.map_1:
                self.map_switcher(self.map_2, 5, 1.3, 180, 'Level 1 Complete!')
                self.textEdit_gamelog.append('Level 1 Complete')

            elif self.current_map == self.map_2:
                self.map_switcher(self.map_3, 1.3, 1.3, 270, 'Level 2 Complete!')
                self.textEdit_gamelog.append('Level 2 Complete')

            elif self.current_map == self.map_3:
                self.map_switcher(self.map_1, 1.3, 2.3, 0, 'Level 3 Complete!')
                self.end_time = time.time()
                time_taken = int(self.end_time - self.start_time)
                self.score = int(10000 / time_taken)
                self.textEdit_gamelog.append('Level 3 Complete! Your Score: {}'.format(self.score))

        else:
            self.textEdit_gamelog.append('No doors in reach')


    def map_switcher(self, new_map, new_pos_x, new_pos_y, new_rot, comment):

        self.current_map = new_map
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y
        self.player_rot_deg = new_rot

        self.current_map_pos_x = new_pos_x
        self.current_map_pos_y = new_pos_y
        self.current_map_rot = new_rot

        print(comment)
        self.color_planes()
        self.render_env()



    def misc_function(self):

        print(self.current_map)


    def collision_check(self, rot_direction):

        wall_value_x = self.pos_x - 0.4 * math.cos(rot_direction)
        wall_value_y = self.pos_y + 0.4 * math.sin(rot_direction)
        wall_value = self.current_map[int(wall_value_x)][int(wall_value_y)]
        if wall_value == 1:
            self.textEdit_gamelog.append('You run into a wall')
        return wall_value


    def help_menu(self):

        # display new pop up that has all info needed for controls and such
        self.pop_up_help = QtWidgets.QMessageBox()

        self.pop_up_help.setWindowTitle("MayanDoom Help Menu")
        self.pop_up_help.setText('''
                [ Help Menu ]\n
                -Press Start to begin the game\n
                -Interact button opens nearby green doors\n
                -FOV value will adjust camera field of view\n
                -Higher FOV values increase frame render time\n
                -Press Reset after making FOV changes to enact them\n
                -If stuck, Reset will return to level beginning\n
                ''')
        self.pop_up_help.setIcon(QtWidgets.QMessageBox.Question)
        self.pop_up_help.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.pop_up_help.exec_()

    def env_screen_setup(self):
        # Delete all previous created nodes
        cmds.SelectAll()
        cmds.delete()
        self.env_scanline_list = []
        self.ground_panel = []
        self.sky_panel = []

        # Setup camera, attributes, and look through
        cam = cmds.camera(name='user_cam')
        print(cam)
        cmds.lookThru(cam)
        cmds.setAttr(cam[0] + '.tz', 80)
        cmds.refresh()

        # Setup scanline screen

        for x in range(self.fov):
            # Setup cube and transformations
            cube = cmds.polyCube()
            cmds.setAttr(cube[0] + '.tx', (1 * (x - (self.fov / 2))) + 0.5)
            cmds.setAttr(cube[0] + '.sy', 40)
            cmds.refresh()
            time.sleep(0.02)

            # Create material
            lambert = cmds.shadingNode('lambert', name='lambert_' + cube[0], asShader=True)

            # Create shading group
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)

            # Assign the Lambert material to the shading group
            cmds.connectAttr(lambert + '.outColor', shading_group + '.surfaceShader', force=True)

            # Assign the shading group to the cube
            cmds.sets(cube[0], edit=True, forceElement=shading_group)

            # Add info to pixel list
            self.env_scanline_list.append([cube, lambert, shading_group])

        # Setup Ground and Sky Panels

        ground_panel = cmds.polyPlane()
        cmds.setAttr(ground_panel[0] + '.ty', 13)
        cmds.setAttr(ground_panel[0] + '.rx', 90)
        cmds.setAttr(ground_panel[0] + '.sx', 84)
        cmds.setAttr(ground_panel[0] + '.sz', 26)
        cmds.refresh()
        time.sleep(0.02)

        # Create material
        lambert = cmds.shadingNode('lambert', name='lambert_' + ground_panel[0], asShader=True)

        # Create shading group
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)

        # Assign the Lambert material to the shading group
        cmds.connectAttr(lambert + '.outColor', shading_group + '.surfaceShader', force=True)

        # Assign the shading group to the cube
        cmds.sets(ground_panel[0], edit=True, forceElement=shading_group)

        # Add info to pixel list
        self.ground_panel.append([ground_panel, lambert, shading_group])


        sky_panel = cmds.polyPlane()
        cmds.setAttr(sky_panel[0] + '.ty', -13)
        cmds.setAttr(sky_panel[0] + '.rx', 90)
        cmds.setAttr(sky_panel[0] + '.sx', 84)
        cmds.setAttr(sky_panel[0] + '.sz', 26)
        cmds.refresh()
        time.sleep(0.02)

        # Create material
        lambert = cmds.shadingNode('lambert', name='lambert_' + sky_panel[0], asShader=True)

        # Create shading group
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)

        # Assign the Lambert material to the shading group
        cmds.connectAttr(lambert + '.outColor', shading_group + '.surfaceShader', force=True)

        # Assign the shading group to the cube
        cmds.sets(sky_panel[0], edit=True, forceElement=shading_group)

        # Add info to pixel list
        self.sky_panel.append([sky_panel, lambert, shading_group])


    def direction_vector(self, start_x, start_y, angle):
        # get x and y, get x and y with 1 unt in sin/cos angle direction, return noramilzed direction
        end_x = self.pos_x + 1 * math.cos(angle)
        end_y = self.pos_y + 1 * math.sin(angle)
        x = end_x - start_x
        y = end_y - start_y

        return x, y

    def color_planes(self):

        # Set color for current level
        print('color planes')

        if self.current_map == self.map_1:

            cmds.setAttr(self.ground_panel[0][1] + '.color', 0.33, 0.64, 0.64)
            cmds.setAttr(self.sky_panel[0][1] + '.color', 0.14, 0.22, 0.11)
            self.wall_color_R = 0.45
            self.wall_color_G = 0.40
            self.wall_color_B = 0.29

        elif self.current_map == self.map_2:

            cmds.setAttr(self.ground_panel[0][1] + '.color', 0.39, 0.20, 0)
            cmds.setAttr(self.sky_panel[0][1] + '.color', 0.53, 0.41, 0.27)
            self.wall_color_R = 0.3
            self.wall_color_G = 0.05
            self.wall_color_B = -0.3

        elif self.current_map == self.map_3:

            cmds.setAttr(self.ground_panel[0][1] + '.color', 0, 0, 0)
            cmds.setAttr(self.sky_panel[0][1] + '.color', 0.16, 0.02, 0.01)
            self.wall_color_R = 0.1
            self.wall_color_G = -0.4
            self.wall_color_B = -0.4


    def render_env(self):

        frame_render_start_time = time.time()

        for index, scanline_number in enumerate(
                self.env_scanline_list):  # list length matches fov, 1 scanline per degree of fov

            rot_deg_cycle = index + ((self.player_rot_deg - 0) - (self.fov / 2))

            rot_rad_cycle = math.radians(rot_deg_cycle)

            fisheye_correction = math.cos(rot_rad_cycle)

            current_ray_length = 0.1
            ray_step_length = 0.05
            test_val = 0
            while True:

                casting_ray_pos_x = self.pos_x + current_ray_length * math.cos(rot_rad_cycle)
                casting_ray_pos_y = self.pos_y - current_ray_length * math.sin(rot_rad_cycle)
                # print(casting_ray_pos_x, casting_ray_pos_y)
                test_val += 1
                if self.current_map[int(casting_ray_pos_x)][int(casting_ray_pos_y)] == 1:

                    # scanline_height = 1 / (0.03 * (current_ray_length * fisheye_correction)) # Makes seemingly non euclide world
                    scanline_height = 1 / (0.03 * current_ray_length)
                    #perp_dist = dist_to_wall * math.cos(ray_angle)
                    cmds.setAttr(scanline_number[0][0] + '.sy', scanline_height)
                    # current_ray_length = round(abs(current_ray_length * math.cos(rot_rad_cycle)), 4)

                    depth_color_value = 1 - (
                                (self.spinBox_val_1.value() * abs(current_ray_length)) / self.spinBox_val_2.value())
                    cmds.setAttr(scanline_number[1] + '.color', depth_color_value + self.wall_color_R, depth_color_value + self.wall_color_G, depth_color_value + self.wall_color_B)

                    print(test_val, depth_color_value)

                    break

                elif self.current_map[int(casting_ray_pos_x)][int(casting_ray_pos_y)] == 2:

                    scanline_height = 1 / (0.03 * current_ray_length)

                    cmds.setAttr(scanline_number[0][0] + '.sy', scanline_height)

                    depth_color_value = 1 - ((1.1 * current_ray_length) / 7)
                    cmds.setAttr(scanline_number[1] + '.color', 0.2, depth_color_value, 0.2)

                    break

                else:

                    current_ray_length = current_ray_length + ray_step_length


        frame_render_end_time = time.time() - frame_render_start_time
        print("Execution Time: {}".format(str(frame_render_end_time)))
        print("Current Location X:{} Y:{} R:{} FOV:{}".format(str(self.pos_x), str(self.pos_y), str(self.player_rot_deg), self.fov))

        cmds.refresh()




MyWindow = MayanDoom()
MyWindow.show()



