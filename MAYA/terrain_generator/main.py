##################################    LIBRARIES  #################################
import maya.cmds as cmds
from random import uniform as rand
import time
from os import listdir
import re

# create a variable to store the group of rocks
LIST_OF_ROCK_GROUPS = cmds.ls(sl=False)
NEW_ROCK_GROUP_LIST=[]

# todo review and fix the code & name convention
# todo move functions to modules

# ###################################   WINDOWS FUNCTIONS  #########################

# creating the main menu window for the terrain creator

def MainWindow():
    # providing initial defaults values for variables
    MainWindow.terrain_width = int(500);         MainWindow.terrain_height = int(500)
    MainWindow.range_value_x = 0.0;              MainWindow.range_value_z = 0.0
    MainWindow.range_value_height = 0.0;         MainWindow.range_value_depth = 0.0
    MainWindow.frequency_ind = 20;               MainWindow.comp_type = 0
    MainWindow.soft_select = False;              MainWindow.soft_select_radius = 20
    MainWindow.animation_time = 0.0;             MainWindow.rock_amount = 20
    MainWindow.rock_range_x = 30.0;              MainWindow.rock_range_z = 30.0
    MainWindow.rock_place_on_terrain = False;    MainWindow.rock_max_radius = 6
    MainWindow.terrain_name = "Terrain";         MainWindow.rock_place_on_selection = False
    MainWindow.ocean_button = False;             MainWindow.text_file_choice = ""
    MainWindow.rock_grp_selection = []

    # Checking if the window already exist and delete to open a new one.
    if cmds.window("GenTool", ex=True):
        cmds.deleteUI("GenTool")
    MainWindow.terrain_maker = cmds.window("GenTool", s=False, rtf=True, wh=(450, 600))

    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=50, innerMarginHeight=50)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 10), (tabs, 'left', 10),
                                                  (tabs, 'bottom', 10), (tabs, 'right', 10)) )

    # ----------------------------------- TAB-CHILD 1 ---------------------
    tab_child1 = cmds.rowColumnLayout(adj=True, numberOfColumns=1)
    cmds.text("\nProvide name for the Terrain that will be generated\n",align="left")
    MainWindow.terrain_name_ = cmds.textField(tx="Terrain",
                        cc="MainWindow.terrain_name = cmds.textField(MainWindow.terrain_name_, q=True, tx=True)")
    cmds.separator(st='in', w=450, h=25)
    cmds.text(l="What is the width of the terrain?", align="left")
    MainWindow.terrain_width_ = cmds.intSliderGrp(l="Min:", min=100, max=1000, f=True, v=500,
                            cc="MainWindow.TerrainWidth=cmds.intSliderGrp(MainWindow.terrain_width_,q=True, v=True)")
    cmds.text(l="What is the height of the terrain?",align="left")    
    MainWindow.terrain_height_ = cmds.intSliderGrp(l="Min:", min=100, max=1000, f=True, v=500,
                            cc="MainWindow.TerrainHeight=cmds.intSliderGrp(MainWindow.terrain_height_,q=True, v=True)")
    cmds.separator(st='in', w=450, h=20)

    # here I created the sliders to user define number of subdivisions width and height
    cmds.text(l="How many width subdivisions?", align="left")
    MainWindow.terrain_subdivisions_width = cmds.intSliderGrp(l="Min:", min=10, max=100, f=True, v=30)
    cmds.text(l="How many height subdivisions?", align="left")
    MainWindow.terrain_subdivisions_height = cmds.intSliderGrp(l="Max:", min=10, max=100, f=True, v=30)
    cmds.separator(st='in', w=450, h=20)

    # here a button is created to build the terrain
    cmds.button(l="Build a new terrain", c="TerrainBuilder()")
    cmds.separator(st='in', w=450, h=40)

    # create a button to delete last obj
    cmds.button(l="Delete Terrain", c="DeleteTerrain()")
    cmds.separator(st='in', w=450, h=15)

    # here a button is created to build the ocean under terrain
    cmds.text("\nYou can create an Ocean under the Terrain\n", align="left" )
    cmds.button(l="Ocean", en=True, c="F_Ocean()")
    cmds.separator(st='in', w=450, h=10)
    cmds.button(l="Move Ocean UP", en=True, c="MoveOceanUP()")
    cmds.button(l="Move Ocean DOWN", en=True, c="MoveOceanDOWN()")
    cmds.separator(st='in', w=450, h=10)
    cmds.button(l="Ocean Advanced Options", en=True, c="OceanSettingsWindow()")
    cmds.setParent( '..' )

    # ---------------------------------------- TAB-CHILD 2 ---------------------
    tab_child2 = cmds.rowColumnLayout(adj= True,numberOfColumns=1)
    cmds.text("\nPlease provide the range you desire", align="left")
    MainWindow.rock_range_x_ = cmds.floatSliderGrp(l="Range for X", f=True, min=0, max=10, v=0,
                            cc="MainWindow.rock_range_x = cmds.floatSliderGrp(MainWindow.rock_range_x_,q=True,v=True)")
    MainWindow.rock_range_z_ = cmds.floatSliderGrp(l="Range for Z", f=True, min=0, max=10, v=0,
                            cc="MainWindow.rock_range_z = cmds.floatSliderGrp(MainWindow.rock_range_z_,q=True,v=True)")
    MainWindow.rock_range_height_ = cmds.floatSliderGrp(l="Range for High", f=True, min=0, max=10, v=0,
                            cc="MainWindow.rock_value_height = cmds.floatSliderGrp(MainWindow.rock_range_height_,q=True,v=True)")
    MainWindow.rock_range_depth_ = cmds.floatSliderGrp(l="Range for Depth", f=True, min=-10, max=0, v=0,
                            cc="MainWindow.rock_range_depth = cmds.floatSliderGrp(MainWindow.rock_range_depth_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=20)

    cmds.text("Please indicate the frequency of noise. higher the number, bigger the area", align="left")
    MainWindow.FreqUser=cmds.intSliderGrp(l="Frequency Indicator", f=True, min=1, max=500, v=20,
                                    cc="MainWindow.FreqInd=cmds.intSliderGrp(MainWindow.FreqUser,q=True,v=True)")
    cmds.separator(st='in',w=450,h=20)

    # --- Soft selection checkbox on/off plus slider for radius 
    cmds.text("Click the checkbox to apply soft select and set the radius on the slider\n", align="left")
    MainWindow.SSel=cmds.checkBox(l="SoftSelect", en=True, align="center",
                                cc="MainWindow.SoftSelect=cmds.checkBox(MainWindow.SSel,q=True,value=True)")
    MainWindow.SoftSelR_=cmds.intSliderGrp(l="Radius", f=True, min=0, max=100, v=20,
                                cc="MainWindow.SoftSelR=float(cmds.intSliderGrp(MainWindow.SoftSelR_,q=True,v=True))")
    cmds.separator(st='in', w=450, h=20)

    cmds.text("Choose based on what component you like to deform", align="left")
    cmds.radioCollection()
    cmds.radioButton(l="Vertex", cc="MainWindow.comp_type=0", sl=True)
    cmds.radioButton(l="Edges", cc="MainWindow.comp_type=1")
    cmds.radioButton(l="Faces", cc="MainWindow.comp_type=2")
    cmds.radioButton(l="Selection", cc="MainWindow.comp_type=4")
    cmds.separator(st='in', w=450, h=20)

    # here I give the option to the user choose the speed of the animation
    cmds.text(l="You can animate the construction of the terrain", align="left")
    cmds.text(l="Choose between 0 (fast) and 1(slow)", align="left")
    MainWindow.AnimTime_=cmds.floatSliderGrp(l="Time:", min=0, max=1, f=True, v=0,
                                cc="MainWindow.AnimTime=cmds.floatSliderGrp(MainWindow.AnimTime_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=20)

    #cmds.button(l="TEST", c="print (MainWindow.SoftSelect,MainWindow.SoftSelR,MainWindow.AnimTime)")
    cmds.button(l="Deform", c="DeformTerrain()")
    cmds.separator(st='in', w=450, h=20)

    # create a button to smooth the terrain view
    cmds.button(l="Smooth the Terrain", c="Smoothing()")
    cmds.separator(st='in', w=450, h=8)
    cmds.setParent('..')

    # --------------------------------------- TAB-CHILD 3 ---------------------
    tab_child3 = cmds.rowColumnLayout(adj=True, numberOfColumns=1)
    # here we create a text field to the user provide name for the rock
    cmds.text("\nProvide name for the rock that will be generated\n", align="left")
    MainWindow.RockName = cmds.textField(tx="Rock")
    cmds.separator(st='in', w=450, h=20)

    # here we ask the amount of rock user needs
    cmds.text("\nProvide the amount of the rocks \n",align="left")
    MainWindow.RockAmount_ = cmds.intSliderGrp(l="Rock Copies", f=True, min=2, max=100, v=20,
                                cc="MainWindow.RockAmount=cmds.intSliderGrp(MainWindow.RockAmount_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=20)

    # here we set slider to user choose the random range location x and Z
    cmds.text("\nPlease provide the range for random distribution of the rocks\n",align="left")
    MainWindow.rock_range_x_ = cmds.floatSliderGrp(l="Range for X", en=True, f=True, min=0, max=500, v=30,
                            cc="MainWindow.RockRIValueX=cmds.floatSliderGrp(MainWindow.rock_range_x_,q=True,v=True)")
    MainWindow.rock_range_z_ = cmds.floatSliderGrp(l="Range for Z", en=True, f=True, min=0, max=500, v=30,
                            cc="MainWindow.RockRIValueZ=cmds.floatSliderGrp(MainWindow.rock_range_z_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=20)
    cmds.text("Maximum radius for the rock\n", align="left")
    MainWindow.RockMaxR_ = cmds.intSliderGrp(l="Radius", f=True, min=4, max=10, v=6,
                                      cc="MainWindow.RockMaxR=cmds.intSliderGrp(MainWindow.RockMaxR_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=20)

    # here provide a checkbox to the user confirm if you want place the rocks on the selection
    MainWindow.rock_on_selection_ = cmds.checkBox(l="Place Rocks only on the Selection", en=True, cc="F_CheckBoxWin()")
    cmds.text("**you need change selection to Vertices,Faces or Edges and select")
    cmds.text("the area on the terrain you desire the rocks be moved after created \n")
    cmds.separator(st='in', w=450, h=20)

    # here provide a checkbox to the user confirm if you want place the rocks on the terrain
    MainWindow.rock_on_terrain_checkbox = cmds.checkBox(l="Place Rocks on the terrain", en=True,
        cc="MainWindow.rock_place_on_terrain = cmds.checkBox(MainWindow.rock_on_terrain_checkbox,q=True,value=True)")
    cmds.text("if this checkbox is selected you spread the rocks in all terrain")
    cmds.separator(st='in', w=450, h=20)

    # group all rocks together
    cmds.button(l="GENERATE", c="RockGenerator()")
    cmds.separator(st='in', w=450, h=40)
    cmds.button(l="UNDO", c="cmds.undo()")
    cmds.setParent( '..' )

    #-------------------------------- TAB-CHILD 4 ---------------------
    tab_child4 = cmds.rowColumnLayout(adj=True,numberOfColumns=1)
    cmds.text("\nSelect the folder where where you have your Textures files\n")
    cmds.button(l="Select Directory", w=450, rs=True, c="cmds.select(clear=True);SelectDirectory()")
    cmds.separator(st='in', h=40)

    cmds.text("Click in the drop box and choose the Texture file of your choice\n")
    MainWindow.text_file_choice_ = cmds.optionMenu('optionMenu', l="File List",
                        cc="MainWindow.TextFileChoice=cmds.optionMenu(MainWindow.text_file_choice_,q=True,v=True)")

    cmds.text("\nIf you want to choose another folder clear the list clicking in the button\n")
    cmds.button(l="Clear List", c="ClearDirectory()")
    cmds.separator(st='in', h=40)

    cmds.text('Select your object and click on the button below to apply the texture', h=25)
    cmds.button(l="Apply Texture to the TERRAIN", c="Shading()")
    cmds.separator(st='in', h=60)

    cmds.text('Select Folder, then Texture on the dropbox,choose the group in the)')
    cmds.text('box below you want to apply the Texture and click on the button\n APPLY TEXTURE TO A GROUP OF ROCKS')
    MainWindow.RockGroups=cmds.textScrollList(nr=10, ams=False, append=NEW_ROCK_GROUP_LIST, shi=4, ai=True)
    cmds.separator(st='in', h=20)

    cmds.button(l="Apply Texture to a GROUP of ROCKS", c="ShadertoGroup()")
    cmds.setParent( '..' )

    cmds.tabLayout( tabs, edit=True, tabLabel=((tab_child1, 'Terrain Generator'),(tab_child2, 'Deform Terrain'),
    (tab_child3,"Rock Generator"),(tab_child4,"Terrain Texture")))        #setting the tabs names
    cmds.showWindow()

# Windows Function to the user set values to smooth the object
def SmoothingWindow():
    # condition to check if the window exist
    if cmds.window("Terrain Smoother", ex=True):
        cmds.deleteUI("Terrain Smoother")

    smoothing_menu = cmds.window("Terrain Smoother",s=True,rtf=True,wh=(300,300))
    cmds.columnLayout()

    #here I created the sliders to user define values of dv,du,pw,ps,po
    cmds.text(l="Divisions U?")
    SmoothingWindow.du=cmds.intSliderGrp(l="Value:", min=0, max=3, f=True, v=0)
    cmds.text(l="Divisions V?")
    SmoothingWindow.dv=cmds.intSliderGrp(l="Value:", min=0, max=3, f=True, v=0)
    cmds.text(l="Points Wire?")
    SmoothingWindow.pw=cmds.intSliderGrp(l="Value:", min=4, max=16, f=True, v=4)
    cmds.text(l="Points Shaded?")
    SmoothingWindow.ps=cmds.intSliderGrp(l="Value:", min=1, max=4, f=True, v=1)
    cmds.text(l="Polygon Object?")
    SmoothingWindow.po=cmds.intSliderGrp(l="Value:", min=1, max=3, f=True, v=1)
    cmds.button(l="Change", w=100, h=50, c="Smoothing()")
    cmds.showWindow(smoothing_menu)


# Windows Function to set attributes for the ocean
def OceanSettingsWindow():
    # initiate variables with default values
    OceanSettingsWindow.scale = 1000;          OceanSettingsWindow.frequency = 3000
    OceanSettingsWindow.wave_length_min = 0.3;   OceanSettingsWindow.wave_length_max = 4000

    # condition to check if the window exist
    if cmds.window("Ocean Window", ex=True):
        cmds.deleteUI("Ocean Window")
    ocean_menu = cmds.window("Ocean Window",s=True,rtf=True,wh=(300,300))
    cmds.columnLayout()

    # here I created the sliders to user define values of dv,du,pw,ps,po
    cmds.text(l="Ocean Scale?")
    OceanSettingsWindow.Scale_ = cmds.floatSliderGrp(l="Value:", min=1, max=7000, f=True, v=1000,
                                    cc="F_OceanWin.Scale=cmds.floatSliderGrp(OceanSettingsWindow.Scale_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=10)

    cmds.text(l="Ocean Frequency?")    
    OceanSettingsWindow.Freq_=cmds.floatSliderGrp(l="Value:", min=1, max=10000, f=True, v=3000,
                                cc="F_OceanWin.Freq=cmds.floatSliderGrp(OceanSettingsWindow.Freq_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=10)

    cmds.text(l="Ocean Wave Length Minimum?")    
    OceanSettingsWindow.wave_Length_min_=cmds.floatSliderGrp(l="Value:", min=1, max=10000, f=True, v=0.3,
            cc="F_OceanWin.wave_length_min = cmds.floatSliderGrp(OceanSettingsWindow.wave_Length_min_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=10)

    cmds.text(l="Ocean Wave Length Maximum?")
    OceanSettingsWindow.wave_length_max_=cmds.floatSliderGrp(l="Value:", min=1, max=10000, f=True, v=4000,
            cc="F_OceanWin.wave_length_max = cmds.floatSliderGrp(OceanSettingsWindow.wave_length_max_,q=True,v=True)")
    cmds.separator(st='in', w=450, h=40)

    cmds.button(l="Change", w=100, h=50, c="OceanSetup()")
    cmds.showWindow(ocean_menu)

# #######################################   FUNCTIONS   ####################################


# here a function to create terrain deforming faces
def TerrainBuilder():
    MainWindow.terrain_name = cmds.textField(MainWindow.terrain_name_, q=True, tx=True)
    # fetch the variables from the windows/user choice
    opt_width = cmds.intSliderGrp(MainWindow.terrain_width_, q=True, v=True)
    opt_height = cmds.intSliderGrp(MainWindow.terrain_height_, q=True, v=True)
    opt_sw = cmds.intSliderGrp(MainWindow.terrain_subdivisions_width, q=True, v=True)
    opt_sh = cmds.intSliderGrp(MainWindow.terrain_subdivisions_height, q=True, v=True)

    # check if the terrain exist and tells user to delete first before create another one
    if cmds.objExists(MainWindow.terrain_name):
        cmds.warning ("You need to delete the previews Terrain to build another one")
    # create the terrain according to values the user choose
    else:
        TerrainBuilder.Obj = cmds.polyPlane(n=MainWindow.terrain_name, w=opt_width, h=opt_height, sw=opt_sw, sh=opt_sh)
        cmds.displaySmoothness(du=3, dv=3, pw=16, ps=4, po=3)
    cmds.select(clear=True)


# function do delete the last terrain created
def DeleteTerrain():
    # check if the terrain exists and delete
    if cmds.objExists(MainWindow.terrain_name):
        confirm_del=cmds.confirmDialog(m="Do you really want to delete the Terrain?", b=["Confirm", "Cancel"])
        if confirm_del == "Confirm":
            cmds.select(MainWindow.terrain_name)
            cmds.delete(MainWindow.terrain_name)
    else:
        # if terrain doesn't exist print message to user
        cmds.warning ("There is no Terrain to delete")

# here I create a function to apply changes to the attributes of the ocean
def OceanSetup():
    cmds.setAttr(OceanBuilder.Shader + ".scale", OceanSettingsWindow.scale)
    cmds.setAttr(OceanBuilder.Shader + ".numFrequencies", OceanSettingsWindow.frequency)
    cmds.setAttr(OceanBuilder.Shader + ".waveLengthMin", OceanSettingsWindow.wave_length_min)
    cmds.setAttr(OceanBuilder.Shader + ".waveLengthMax", OceanSettingsWindow.wave_length_max)

# here I have a function to check if the terrain exist before create a plane with an ocean shader applied
def OceanBuilder():
    # here I fetch the terrain Width and height to create the ocean with the same size
    ocean_width = int(MainWindow.terrain_width)
    ocean_height = int(MainWindow.terrain_height)

    # here I check if the terrain exist before create the ocean
    if cmds.objExists(MainWindow.terrain_name):
        OceanBuilder.Obj=cmds.polyPlane(n="Ocean", w=ocean_width, h=ocean_height)
        cmds.move(0, -5, 0)
        OceanBuilder.Shader=cmds.shadingNode("oceanShader", asShader=True)
        cmds.select(OceanBuilder.Obj)
        cmds.hyperShade(assign=OceanBuilder.Shader)
    # here is a warming to the user crate first the terrain
    else:
        cmds.warning("You need to create a Terrain first")

    cmds.select(clear=True)


# here I set two simple functions to move up and down the ocean
def MoveOceanUP():
        cmds.select(OceanBuilder.Obj)
        cmds.move(0,2.5,0,r=True)


def MoveOceanDOWN():
        cmds.select(OceanBuilder.Obj)
        cmds.move(0,-2.5,0,r=True)


# change the display of the terrain to smooth view according user choice
def Smoothing():
    # getting values from sliders and store in var
    Smoothing.du = cmds.intSliderGrp(SmoothingWindow.du, q=True, v=True)
    Smoothing.dv = cmds.intSliderGrp(SmoothingWindow.dv, q=True, v=True)
    Smoothing.pw = cmds.intSliderGrp(SmoothingWindow.pw, q=True, v=True)
    Smoothing.ps = cmds.intSliderGrp(SmoothingWindow.ps, q=True, v=True)
    Smoothing.po = cmds.intSliderGrp(SmoothingWindow.po, q=True, v=True)
    # change to smooth according to user choice
    cmds.displaySmoothness(du=Smoothing.du, dv=Smoothing.dv, pw=Smoothing.pw, ps=Smoothing.ps, po=Smoothing.po)


def DeformTerrain():
    # creating condition to check if the terrain exist
    if cmds.objExists(MainWindow.terrain_name):
        current_frame = 1
        # here we identify the component type based on MainWindow.comp_type value
        if MainWindow.comp_type == 0:
            cmds.ConvertSelectionToVertices()
            all_comp = cmds.ls(sl=True,fl=True)
        elif MainWindow.comp_type == 1:
            cmds.ConvertSelectionToEdges()
            all_comp = cmds.ls(sl=True,fl=True)
        elif MainWindow.comp_type == 2:
            cmds.ConvertSelectionToFaces()
            all_comp = cmds.ls(sl=True,fl=True)
        else:
            all_comp = cmds.ls(sl=True,fl=True)

        # at this point we are just deforming the Terrain
        for i in range (0, len(all_comp), MainWindow.FreqInd):
            rand_selection = int(rand(0, len(all_comp)))
            cmds.select(cl=True)
            single_comp = all_comp[rand_selection]
            cmds.select(single_comp)
            rand_x = rand(-MainWindow.range_value_x, MainWindow.range_value_x)
            rand_z = rand(-MainWindow.range_value_z, MainWindow.range_value_z)
            rand_y = rand(MainWindow.range_value_depth, MainWindow.range_value_height)
            cmds.move(rand_x, rand_y, rand_z, r=True)
            cmds.currentTime(current_frame)
            current_frame = current_frame+1
            time.sleep(MainWindow.AnimTime)
        cmds.DeleteHistory()

    # if terrain doesn't exist print message to user
    else:
        cmds.warning ("There is no Terrain to Deform")
    cmds.select(clear=True)


# here I create the rock gen function
def RockGenerator():
    current_frame=1

    RnX = MainWindow.RockRIUserX
    RnZ = MainWindow.RockRIUserZ
    rock_num = int(MainWindow.rock_amount) + 1
    # fetch the name of the rock
    rock_name = cmds.textField(MainWindow.rock_name, q=True, tx=True)
    # this command is to chance to soft select
    cmds.softSelect(sse=1, ssd=0.1)
    # checking if user want rocks on the selection
    if MainWindow.rock_place_on_selection:
        # add to a variable a list with all components in the selection
        selected_terrain = cmds.ls(sl=True, fl=True)
        if len(selected_terrain)<3:
            cmds.warning("Select a bigger area there")
        else:
            # creating a group to add the objects to it when every rock is created.
            rock_group = cmds.group(empty=True,name="Rocks_grp#")
            for i in range(1,rock_num):
                # creating a list of the objects selected by the user
                random_mod = int(rand(0, len(selected_terrain)))
                mod_obj = selected_terrain[random_mod]
                #get the transform from the objects
                mod_attr = cmds.xform(mod_obj,q=True,t=True)
                # getting a random radius number from 1 to user limit input
                rand_rad = rand(4, MainWindow.RockMaxR)
                # calculating a number in relation to the random radius
                move_num = rand_rad * 0.2
                # randomizing the amount of subdivisions to the object
                rand_sub_d = int(rand(10, 20))
                # randomizing the amount of subdivisions to the object
                rand_sub_d1 = int(rand(10, 20))
                # Creating the object
                follow_obj = cmds.polySphere(n=rock_name, r=rand_rad, sx=rand_sub_d1, sy=rand_sub_d)[0]

                # setting a random scale to the rock
                cmds.setAttr(follow_obj+".scaleY", rand(0.9, 1.5))
                cmds.setAttr(follow_obj+".rotateY", rand(0, 90))
                cmds.setAttr(follow_obj+".rotateX", rand(0, 90))
                cmds.setAttr(follow_obj+".rotateZ", rand(0, 90))

                # parenting the object to a group
                cmds.parent(follow_obj,rock_group)
                # here I move the object to a random vertices on the plane
                cmds.move(mod_attr[0], mod_attr[1], mod_attr[2])
                cmds.ConvertSelectionToVertices()
                # add to a variable a list with all vertices in the object
                component_all = cmds.ls(sl=True, fl=True)
                cmds.displaySmoothness(du=3, dv=3, pw=16, ps=4, po=3)
                # with this loop I go through all selection and one by one I move them to the random location
                for i in range(0,len(component_all)):
                    rand_selection=int(rand(1,len(component_all)))
                    single_comp=component_all[rand_selection]
                    cmds.select(single_comp)
                    random_x = rand(-move_num, move_num)
                    random_y = rand(-move_num, move_num)
                    random_z = rand(-move_num, move_num)
                    cmds.move(random_x,random_y,random_z,r=True)
                cmds.select(cl=True)
                cmds.DeleteHistory()

    elif cmds.objExists(MainWindow.terrain_name):
        # selecting the terrain
        cmds.select(MainWindow.terrain_name)
        cmds.ConvertSelectionToVertices()
        # here create a list with all terrain vertices
        vertices_selection = cmds.ls(sl=True, o=True)[0]
        sel_v = cmds.ls('{}.vtx[:]'.format(vertices_selection), fl=True)
        # creating a group to add the objects to it when every rock is created.
        rock_group = cmds.group(empty=True,name="Rocks_grp#")
        if MainWindow.rock_place_on_terrain:
            for i in range (1,rock_num) :
                random_mod = int(rand(0,len(sel_v)))
                mod_obj = sel_v[random_mod]
                #get the transform from the objects
                mod_attr = cmds.xform(mod_obj,q=True,t=True)
                # getting a random radius number from 1 to user limit input
                rand_rad = rand(4, MainWindow.RockMaxR)
                # calculating a number in relation to the random radius
                move_num = rand_rad*0.2
                # randomizing the amount of subdivisions to the object
                rand_sub_d = int(rand(10,20))
                # randomizing the amount of subdivisions to the object
                rand_sub_d1 = int(rand(10,20))
                follow_obj = cmds.polySphere(n=rock_name,r=rand_rad,sx=rand_sub_d1,sy=rand_sub_d)[0]
                cmds.setAttr(follow_obj+".scaleY",rand(0.9, 1.5))
                cmds.setAttr(follow_obj+".rotateY",rand(0, 90))
                cmds.setAttr(follow_obj+".rotateX",rand(0, 90))
                cmds.setAttr(follow_obj+".rotateZ",rand(0, 90))
                # parenting the object to a group
                cmds.parent(follow_obj, rock_group)
                # here I move the object to a random vertices on the plane
                cmds.move(mod_attr[0], mod_attr[1], mod_attr[2])
                cmds.ConvertSelectionToVertices()
                # add to a variable a list with all vertices in the object
                component_all = cmds.ls(sl=True, fl=True)
                # apply smoothness to the rocks
                cmds.displaySmoothness(du=3, dv=3, pw=16, ps=4, po=3)
                # with this loop I go through all selection and one by one I move them to the random location
                for i in range(0, len(component_all)):
                    rand_selection = int(rand(1,len(component_all)))
                    single_comp = component_all[rand_selection]
                    cmds.select(single_comp)
                    random_x = rand(-move_num, move_num)
                    random_y = rand(-move_num, move_num)
                    random_z = rand(-move_num, move_num)
                    cmds.move(random_x, random_y, random_z, r=True)
                cmds.select(cl=True)
                cmds.DeleteHistory()
        #here we have the script to generate rocks in the range determined by the user 

        else:
            for i in range (1, rock_num):
                # def. random num to move the rock to a random location X
                ran_loc_x = rand(-RnX,RnX)
                # def. random num to move the rock to a random location Z
                ran_loc_z = rand(-RnZ,RnZ)
                # getting a random radius number from 1 to user limit input
                rand_rad = rand(4, MainWindow.RockMaxR)
                # calculating a number in relation to the random radius
                move_num = rand_rad*0.2
                # randomizing the amount of subdivisions to the object
                rand_sub_d = int(rand(10,20))
                # Creating the object
                obj = cmds.polySphere(n=rock_name, r=rand_rad, sx=rand_sub_d, sy=rand_sub_d)[0]
                # setting a random scale to the rock
                cmds.setAttr(obj+".scaleY", rand(0.9, 1.5))
                # setting a random rotation Y
                cmds.setAttr(obj+".rotateY", rand(0, 90))
                # setting a random rotation X
                cmds.setAttr(obj+".rotateX", rand(0, 90))
                # setting a random rotation Z
                cmds.setAttr(obj+".rotateZ", rand(0, 90))
                # parenting the object to a group
                cmds.parent(obj, rock_group)
                # here I move the object to an X,Z random location inside a range
                cmds.move(ran_loc_x, 0, ran_loc_z)
                cmds.ConvertSelectionToVertices()
                # add to a variable a list with all vertices in the object
                component_all = cmds.ls(sl=True, fl=True)
                # apply smoothness to the rocks
                cmds.displaySmoothness(du=3, dv=3, pw=16, ps=4, po=3)

                # with this loop I go through all selection and one by one I move them to the random location
                for i in range(0, len(component_all)):
                    rand_selection = int(rand(0, len(component_all)))
                    single_comp = component_all[rand_selection]
                    cmds.select(single_comp)
                    random_x = rand(-move_num, move_num); random_y = rand(-move_num, move_num); random_z = rand(-move_num, move_num)
                    cmds.move(random_x, random_y, random_z, r=True)
            cmds.select(cl=True)
            cmds.DeleteHistory()

    # check all existing rock groups
    rock_grp_list = cmds.ls(sl=False )
    rock_group_list2 = []

    for rock_grp_list in rock_grp_list:
        ignore_string="|"                                                #crate a variable with a string to ignore it
        result_groups = re.search('.*grp.*', rock_grp_list)                      #returns None if search fails
        if ignore_string in str(result_groups):
            pass
        elif result_groups:                                                    #here add the result of the groups to a list
            rock_group_list2.append(rock_grp_list)

    for x in rock_group_list2:                                            #here I compare the list generated when run the script at first and added new groups.
        if x not in NEW_ROCK_GROUP_LIST:
            NEW_ROCK_GROUP_LIST.append(x)
            print (NEW_ROCK_GROUP_LIST)
    # here I will remove the items from the text scroll and refresh with updated list
    cmds.textScrollList(MainWindow.RockGroups, e=True, ra=True)
    cmds.textScrollList(MainWindow.RockGroups, e=True, append=NEW_ROCK_GROUP_LIST)


def CheckBoxWin():                                                    #here I create a function to change state of the checkbox
    MainWindow.rock_on_selection=cmds.checkBox(MainWindow.RockonSel_, q=True, value=True)
    if MainWindow.rock_on_selection:                                       #when user choose to move rock to selection the other checkbox is disabled
        cmds.checkBox(MainWindow.RockonTer, e=True, en=False, v=False)
    else:
        cmds.checkBox(MainWindow.RockonTer, e=True, en=True)


def SelectDirectory():                                                         #this function I create to user select the folder and list the files in a dropbox to the user
        basic_filter = "Image Files (*.jpg *.jpeg *.tga *.png *.tiff *.bmp *.psd)"
        SelectDirectory.myDir = cmds.fileDialog2 (fileFilter=basic_filter, dialogStyle=2, fm=3)
        SelectDirectory.Files= listdir(SelectDirectory.myDir[0])
        for items in SelectDirectory.Files:
            file_endings = ('.jpg','JPG','.jpeg','.JPEG','.tga','.TGA','.png','.PNG','.tiff','.TIFF','.bmp','.BMP')
            if items.endswith(file_endings):
                cmds.menuItem(items)
            else:
                pass


def ClearDirectory():                                                       #this function is to clear the dropbox with the list of files
    fileList = cmds.optionMenu('optionMenu', q=True, itemListLong=True)
    if fileList:
        cmds.deleteUI(fileList)


def ShaderToGroup():                                                    #apply texture to the group of rocks
    MainWindow.RockGrpSel = cmds.textScrollList(MainWindow.RockGroups, q=True, si=True) #fetch the group of rocks the user choose
    texture_name = MainWindow.TextFileChoice[:-4]
    #listing and saving existing materials to a variable
    mat_list = sorted(set(cmds.ls([mat for item in cmds.ls(type='shadingEngine') for mat in cmds.listConnections(item) if cmds.sets(item, q=True)], materials=True)))

    # here I select all the objects inside the group and delete the first (group reference in the list)
    cmds.select(MainWindow.RockGrpSel, hierarchy=True)
    # list all the objects in the group to apply texture in a loop
    list_objs = cmds.ls(MainWindow.RockGrpSel, dag=True, type="mesh")
    del (list_objs[0])

    # apply texture if already exists
    if (texture_name+"ShaderNode") in mat_list:
        for ll in range(0,len(list_objs)):
                cmds.select(list_objs[ll])
                object=cmds.ls(sl=True)
                cmds.sets(object, e=True, forceElement=texture_name+'RockMaterialGroup')
    else:
        # start to create the shader and connect.
        selected_menu_item = cmds.optionMenu('optionMenu', q=True, value=True)
        file_r_node = cmds.shadingNode('file', name=texture_name, asTexture=True)
        cmds.setAttr(texture_name +'.fileTextureName', SelectDirectory.myDir[0] + '/' + selected_menu_item, type="string")
        cmds.sets(name=texture_name+'RockMaterialGroup', renderable=True, empty=True)
        # create shader
        ShaderNode = cmds.shadingNode('blinn', name=texture_name+'ShaderNode', asShader=True)
        file_r_node = cmds.shadingNode('file', name=texture_name, asTexture=True)
        cmds.setAttr(texture_name +'.fileTextureName', SelectDirectory.myDir[0] + '/' + selected_menu_item, type="string")
        cmds.connectAttr(texture_name+'.outColor',texture_name+'ShaderNode'+'.color')
        my2_dr_placer=cmds.shadingNode("place2dTexture", n="MyTxtPlacer", asUtility=True)
        cmds.connectAttr(my2_dr_placer+".outUV",texture_name+".uvCoord", f=True)
        cmds.surfaceShaderList(texture_name+'ShaderNode', add=texture_name+'RockMaterialGroup')
        # here I apply texture for every object grouped
        for ll in range(0,len(list_objs)):
                cmds.select(list_objs[ll])
                object = cmds.ls(sl=True)
                cmds.sets(object, e=True, forceElement=texture_name+'RockMaterialGroup')

        # here create variables to save name of the files and check if exist or not in the for loop
        normal_map_file = [];       normal_map_exist = False
        rough_map_file = [];        rough_map_exist = False
        disp_map_file = [];         disp_map_exist = False

        files_list_normal = SelectDirectory.Files
        files_list_rough = SelectDirectory.Files
        files_list_disp = SelectDirectory.Files

        # here I create a variable to split the string of the file name
        ref_name = list(texture_name)
        # here I set a variable to save the five first letters from the file
        search_name = (ref_name[0]+ref_name[1]+ref_name[2]+ref_name[3]+ref_name[4])

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
        # Here I have a sequence of FOR loop where I check in the directory/folder, files that has the same start string from the texture file first, then I check for the  #
        # end if finish with map I'm looking for (*Normal.jpg, *Roughness.jpg,etc), after the second check if file founded is stored in a variable, also created a bool     #
        # to use to install the map or not         <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
        for files_list_normal in files_list_normal:
            result = files_list_normal.startswith(search_name)
            if result:
                result2 = files_list_normal.endswith("Normal.jpg")
                if result2:
                    normal_map_exist = True
                    normal_map_file.append(files_list_normal)
                    # here install normal map in case the file for normal map is founded
                    if normal_map_exist:
                        normal_node = cmds.shadingNode("file", name="NormalMap", asTexture=True)
                        bump_normal = cmds.shadingNode("bump2d", asUtility=True)
                        cmds.setAttr(normal_node +".fileTextureName",
                                     SelectDirectory.myDir[0] + '/' + normal_map_file[0], type="string")
                        cmds.connectAttr(normal_node +".outAlpha", bump_normal + ".bumpValue", f=True)
                        cmds.connectAttr(bump_normal + ".outNormal", ShaderNode + ".normalCamera")
                        cmds.connectAttr(my2_dr_placer+".outUV", normal_node+".uvCoord")
                        cmds.setAttr(bump_normal + ".bumpDepth", 0.29)
                        del files_list_normal                                                                         #deleting variables
                        del normal_map_exist
        for files_list_rough in files_list_rough:
            result = files_list_rough.startswith(search_name)
            if result:
                result2 = files_list_rough.endswith("Roughness.jpg")
                if result2:
                    rough_map_exist=True
                    rough_map_file.append(files_list_rough)
                    # here install roughness map in case the file for normal map is founded
                    if rough_map_exist:
                        rough_node=cmds.shadingNode("file", name="NormalMap", asTexture=True)
                        cmds.setAttr(rough_node +".fileTextureName",
                                     SelectDirectory.myDir[0] + '/' + rough_map_file[0], type="string")
                        cmds.connectAttr(rough_node+".outColor", ShaderNode+".ambientColor", f=True)
                        cmds.connectAttr(my2_dr_placer+".outUV", rough_node+".uvCoord")
                        del files_list_rough
                        del rough_map_exist
        for files_list_disp in files_list_disp:
            result = files_list_disp.startswith(search_name)
            if result:
                result2 = files_list_disp.endswith("Displacement.jpg")
                if result2:
                    disp_map_exist=True
                    disp_map_file.append(files_list_disp)
                    # here install Displacement map in case the file for normal map is founded
                    if disp_map_exist:
                        DispNode=cmds.shadingNode("file",name="NormalMap",asTexture=True)
                        cmds.setAttr(DispNode +".fileTextureName",
                                     SelectDirectory.myDir[0] + '/' + disp_map_file[0], type="string")
                        cmds.connectAttr(DispNode+".outColor", ShaderNode+".ambientColor", f=True)
                        cmds.connectAttr(my2_dr_placer+".outUV", DispNode+".uvCoord")
                        # deleting variables
                        del files_list_disp
                        del disp_map_exist


# here I have a function to select the texture from the files in a selected folder, create and applying a shader
def Shading():
    Shading.texture_name= MainWindow.TextFileChoice[:-4]
    # listing and saving existing materials to a variable
    mat_list = sorted(set(cmds.ls([mat for item in cmds.ls(type='shadingEngine') for mat in cmds.listConnections(item) if cmds.sets(item, q=True)], materials=True)))
    object = cmds.ls(sl=True)
    # check if the material already exist to apply directly and not create another material
    if (Shading.texture_name + "ShaderNode") in mat_list:
        for ll in range(0,len(ListObj)):
                cmds.select(ListObj[ll])
                Object=cmds.ls(sl=True)
                cmds.sets(Object, e=True, forceElement='imageMaterialGroup')
    else:
        # add the selected file to a variable
        selected_menu_item = cmds.optionMenu('optionMenu', q=True, value=True)
        file_node = cmds.shadingNode('file', name=Shading.texture_name, asTexture=True)
        cmds.setAttr(Shading.texture_name + '.fileTextureName', SelectDirectory.myDir[0] + '/' + selected_menu_item,
                     type="string")
        cmds.sets(name='imageMaterialGroup', renderable=True, empty=True)
        Shading.ShaderNode = cmds.shadingNode('blinn', name=Shading.texture_name + 'ShaderNode', asShader=True)

        file_node = cmds.shadingNode('file', name=Shading.texture_name, asTexture=True)
        cmds.setAttr(Shading.texture_name + '.fileTextureName', SelectDirectory.myDir[0] + '/' + selected_menu_item,
                     type="string")
        cmds.connectAttr(Shading.texture_name + '.outColor', Shading.texture_name + 'ShaderNode' + '.color')
        Shading.my_2D_placer=cmds.shadingNode("place2dTexture", n="MyTxtPlacer", asUtility=True)
        cmds.connectAttr(Shading.my_2D_placer + ".outUV", Shading.texture_name + ".uvCoord", f=True)
        cmds.surfaceShaderList(Shading.texture_name + 'ShaderNode', add='imageMaterialGroup')
        cmds.sets(object, e=True, forceElement='imageMaterialGroup')
        ShadingMaps()


def ShadingMaps():
        # here create variables to save name of the files and check if exist or not in the for loop
        normal_map_file = [];       normal_map_exist = False
        rough_map_file = [];        rough_map_exist = False
        disp_map_file = [];         disp_map_exist = False

        files_list_normal = SelectDirectory.Files
        files_list_rough = SelectDirectory.Files
        files_list_disp = SelectDirectory.Files
        # here I create a variable to split the string of the file name
        ref_name = list(Shading.TextureName)
        # here I set a variable to save the five first letters from the file
        search_name = (ref_name[0]+ref_name[1]+ref_name[2]+ref_name[3]+ref_name[4])

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
        # Here I have a sequence of FOR loop where I check in the directory/folder, files that has the same start string from the texture file first, then I check for the  #
        # end if finish with map I'm looking for (*Normal.jpg, *Roughness.jpg,etc), after the second check if file founded is stored in a variable, also created a bool     #
        # to use to install the map or not         <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#

        for files_list_normal in files_list_normal:
            result_files = files_list_normal.startswith(search_name)
            if result_files:
                result2=files_list_normal.endswith("Normal.jpg")
                if result2:
                    normal_map_exist = True
                    normal_map_file.append(files_list_normal)
                    # here install normal map in case the file for normal map is founded
                    if normal_map_exist:
                        normal_node = cmds.shadingNode("file",name="NormalMap",asTexture=True)
                        bump_normal = cmds.shadingNode("bump2d",asUtility=True)
                        cmds.setAttr(normal_node +".fileTextureName",
                                     SelectDirectory.myDir[0] + '/' + normal_map_file[0], type="string")
                        cmds.connectAttr(normal_node+".outAlpha",bump_normal+".bumpValue",f=True)
                        cmds.connectAttr(bump_normal +".outNormal", Shading.ShaderNode + ".normalCamera")
                        cmds.connectAttr(Shading.My2Dplacer + ".outUV", normal_node + ".uvCoord")
                        cmds.setAttr(bump_normal+".bumpDepth",0.29)
                        del files_list_normal
                        del normal_map_exist

        for files_list_rough in files_list_rough:
            result_files = files_list_rough.startswith(search_name)
            if result_files:
                result2 = files_list_rough.endswith("Roughness.jpg")
                if result2:
                    rough_map_exist = True
                    rough_map_file.append(files_list_rough)
                    # here install roughness map in case the file for normal map is founded
                    if rough_map_exist:
                        rough_node = cmds.shadingNode("file",name="NormalMap",asTexture=True)
                        cmds.setAttr(rough_node +".fileTextureName",
                                     SelectDirectory.myDir[0] + '/' + rough_map_file[0], type="string")
                        cmds.connectAttr(rough_node +".outColor", Shading.ShaderNode + ".ambientColor", f=True)
                        cmds.connectAttr(Shading.My2Dplacer + ".outUV", rough_node + ".uvCoord")
                        del files_list_rough
                        del rough_map_exist

        for files_list_disp in files_list_disp:
            result_files = files_list_disp.startswith(search_name)
            if result_files:
                result2 = files_list_disp.endswith("Displacement.jpg")
                if result2:
                    disp_map_exist = True
                    disp_map_file.append(files_list_disp)
                    # here install Displacement map in case the file for normal map is founded
                    if disp_map_exist:
                        disp_node = cmds.shadingNode("file",name="NormalMap",asTexture=True)
                        cmds.setAttr(disp_node +".fileTextureName",
                                     SelectDirectory.myDir[0] + '/' + disp_map_file[0], type="string")
                        cmds.connectAttr(disp_node +".outColor", Shading.ShaderNode + ".ambientColor", f=True)
                        cmds.connectAttr(Shading.My2Dplacer + ".outUV", disp_node + ".uvCoord")
                        del files_list_disp
                        del disp_map_exist

# ################################    START SCRIPT   #############################

# for loop to check and store the names of groups
for LIST_OF_ROCK_GROUPS in LIST_OF_ROCK_GROUPS:
  IgnoreString="|"
  # returns None if search fails
  result = re.search('.*grp.*', LIST_OF_ROCK_GROUPS)
  if IgnoreString in str(result):
    pass
  elif result:
      # here I store the names
    NEW_ROCK_GROUP_LIST.append(LIST_OF_ROCK_GROUPS)

MainWindow()




