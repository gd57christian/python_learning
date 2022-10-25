import maya.cmds as cmds

my_planet = cmds.polySphere(name="world", subdivisionsAxis=12, subdivisionsHeight=12)[0]

my_sun = "sun"
my_light = "pointlight_0"

light_list=[]
light_shape_list=[]

cmds.pointLight(name=my_sun, intensity=5000)
cmds.setAttr(f'{my_sun}.translateX', 10)
cmds.select(my_planet)

cmds.ConvertSelectionToVertices()

# here create a list with all terrain vertices
vertices_selection = cmds.ls(selection=True, objectsOnly=True)[0]

selected_vertices = cmds.ls('{}.vtx[:]'.format(vertices_selection), fl=True)

for i in selected_vertices:
    cmds.select(i)
    vertices_attribute = cmds.xform(i, q=True, t=True)
    vertices_attribute_list = (vertices_attribute[0], vertices_attribute[1], vertices_attribute[2])
    cmds.pointLight()

    # moving the created lights 1% further the position from the vertices
    cmds.move(vertices_attribute[0] + (vertices_attribute[0] * 0.01), vertices_attribute[1] + (vertices_attribute[1] * 0.01), vertices_attribute[2] + (vertices_attribute[2] * 0.01))
    selected_light = cmds.ls(selection=True)#[0]

    # creating a list of lights to use when add constrains
    light_list.append(selected_light)

    # parenting the created lights to the object/planet
    cmds.parent(selected_light, my_planet)

sun_world_dist = cmds.shadingNode("distanceBetween", asUtility=True, name=f"{my_sun}_{my_planet}_distBetween")
cmds.connectAttr(f'{my_sun}.worldMatrix[0]', f'{sun_world_dist}.inMatrix1')
cmds.connectAttr(f'{my_planet}.worldMatrix[0]', f'{sun_world_dist}.inMatrix2')

for light in light_list:
    light_name = light[0]
    sun_light_dist=cmds.shadingNode("distanceBetween", asUtility=True, name=f"{my_sun}_{light_name}_distBetween")
    cmds.connectAttr(f'{my_sun}.worldMatrix[0]',f'{sun_light_dist}.inMatrix2')
    cmds.connectAttr(f'{light_name}.worldMatrix[0]', f'{sun_light_dist}.inMatrix1')

    # creating condition node and connecting, setting to greater than
    condition_node = cmds.shadingNode("condition", asUtility=True, name=f"{light_name}_condition")
    cmds.connectAttr(f'{sun_world_dist}.distance', f'{condition_node}.firstTerm')
    cmds.connectAttr(f'{sun_light_dist}.distance', f'{condition_node}.secondTerm')
    cmds.setAttr(f'{condition_node}.operation', 2)

    # connecting the condition to the intensity of the shape
    light_shape = cmds.listRelatives(light_name, shapes=True)[0]
    cmds.connectAttr(f'{condition_node}.outColorR', f'{light_shape}.intensity')

