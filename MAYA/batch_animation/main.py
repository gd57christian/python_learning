#importing libraries
import maya.cmds as cmds
import maya.mel as mel

#setting a confirm dialog to turn on or off the debug
DEBUG_BUTTON = cmds.confirmDialog(message='Do you want debug mode on?', button=["yes", "no"], defaultButton="1", cancelButton="0", title="Debug ON/OFF", backgroundColor=[0, 1, 1])
DEBUG = DEBUG_BUTTON

# batch Animation Exporter  - select files to export after running the script
print('batch Animation Exporter Start')

# open a file dialogue to select the animation files
scenes = cmds.fileDialog2(fm = 4)
if DEBUG == 'yes':
    print (scenesSel)
for myScene in scenes:
    if DEBUG == 'yes':
        print (myScene)
    # open the scene/anim scene
    cmds.file(myScene, open=True)
    
    # invremental saving the opened file
    mel.eval('incrementalSaveScene;')
    cmds.file(save=True)
    
    # create export file
    tempName1 = (myScene.split('/')[-1].split('.')[0]+".fbx")
    if DEBUG == 'yes':
        print ('>>> The temp name is >>>' + str(tempName1))
    active_work_space = cmds.workspace(rd=True, query=True)

    if DEBUG == 'yes':
        print ('>>> The workspace is >>>' + str(active_work_space))
    final_file_name = (active_work_space + 'clips/' + tempName1)

    if DEBUG == 'yes':
        print ('>>> The final file is >>>' + str(final_file_name))
    
    def DeleteUnwanted():
        # importing files from reference
        cmds.select(clear=True)
        reference_nodes = cmds.file(reference=True, query=True)

        if DEBUG == 'yes':
            print ('>>> ref nodes is >>>' + str(reference_nodes))

        for ref in reference_nodes:
            cmds.file(ref, ir=True)
        
        # remove namespaces
        name_spaces = cmds.namespaceInfo(lon=True, r=True)

        for ns in name_spaces:
            if ns not in ['UI', 'shared']:
                cmds.namespace(removeNamespace=ns, mnr=True)
        if DEBUG == 'yes':
            print ('>>> names spaces is >>>' + str(name_spaces))

        remaining_name_spaces = cmds.namespaceInfo(lon=True, r=True)

        if DEBUG == 'yes':
            print ('>>> remaining names spaces is >>>' + str(remaining_name_spaces))
        
        # baking the animation
        min_time = cmds.playbackOptions(minTime=True, query=True)
        max_time = cmds.playbackOptions(maxTime=True, query=True)
        '''print (minTime, maxTime)'''

        cmds.bakeResults('WorldRoot_joint', t=(min_time, max_time), simulation=True, hi='below', sampleBy=1,
                         disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False,
                         removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, controlPoints=False, shape=True)
        
        # delete the rig and the reference
        mel.eval('doEnableNodeItems true all;')
        
        if cmds.objExists('world_Zero'):
            cmds.delete('world_Zero')
        if cmds.objExists('Reference'):
            cmds.delete('Reference')
        
        skin_clusters = cmds.ls(type='skinCluster')
        for sc in skin_clusters:
            skin_shape = cmds.skinCluster(sc, geometry=True, query=True)
            for ss in skin_shape:
                related_xform = cmds.listRelatives(ss, parent=True, typ='transform')
                cmds.delete(related_xform)
        
        # delete the constraints
        cmds.select(clear=True)
        all_constraints = cmds.ls(type='parentConstraint')

        if DEBUG == 'yes':
            print('>>> All Constraints is >>>' + str(all_constraints))

        cmds.delete(all_constraints)
        
        mel.eval('doEnableNodeItems false all;')
            
    # exporting the clean skeleton as FBX
    def ExportAnimFile():
        cmds.select("WorldRoot_joint", hi=True)
        cmds.file(final_file_name, f=True, exportSelected=True, type='FBX export')
        mel.eval('FBXUICallBack -1 exportButton;')
        print ('Done Exporting')
    
    DeleteUnwanted()
    ExportAnimFile()
    
    cmds.file(f=1, new=1)