import bpy

#property group to store options that the user can
#make true or false
class fix_dbd_animations_properties(bpy.types.PropertyGroup):
    is_problem_jaw_bone: bpy.props.BoolProperty(name="Fix Jaw Bone for Killer Actions", default = False)

#this is panel 2 as it is the second panel in the psk/psa panel
class PSKPSA_PT_fix_dbd_animations_import_panel_2(bpy.types.Panel):
    bl_label = "Fix DBD Animations"
    bl_idname = "PSKPSA_PT_fix_skeletons_import_panel_2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PSK / PSA"

    def draw(self, context):
        layout = self.layout
        #store active/selected scene to variable
        scene = context.scene
        #allow access to user inputted properties through pointer
        #to properties
        fixdbdanimtool = scene.fixdbdanim_tool

        layout.prop(fixdbdanimtool, "is_problem_jaw_bone")
        
        layout.label(text ="Select the Dead By Daylight Skeleton with problem")
        layout.label(text ="For Killer skeletons > Press Fix ONE Dead By Daylight Killer Action")
        layout.label(text ="To fix ALL Actions > Press Fix ALL Dead By Daylight Killer Actions")
        layout.label(text ="For Survivor skeletons > Press Fix ALL Dead By Daylight Survivor Facial Animations")
        layout.label(text ="Fix Dead By Daylight Killer Animations")
        layout.operator("pskpsa.fix_dbd_killer_active_action_operator")
        layout.operator("pskpsa.fix_all_dbd_killer_actions_operator")
        
        layout.separator()
        layout.label(text ="Fix Dead By Daylight Survivor Animations")
        layout.operator("pskpsa.fix_dbd_survivor_active_action_operator")
        layout.operator("pskpsa.fix_all_dbd_survivor_actions_operator")

#---------------fix the active action (only one) for killer and survivor 
class PSKPSA_OT_fix_dbd_killer_active_action(bpy.types.Operator):
    bl_label = "Fix ONE Dead By Daylight Killer Action"
    bl_description = "Reset transforms for problem bones for one Killer active Action"
    bl_idname = "pskpsa.fix_dbd_killer_active_action_operator"

    def execute(self, context):
        fix_dbd_killer_active_action()
        
        return {'FINISHED'}

class PSKPSA_OT_fix_dbd_survivor_facial_anim(bpy.types.Operator):
    bl_label = "Fix ALL Dead By Daylight Survivor Facial Animations"
    bl_description = "Create offset facial action to fix survivor facial animations"
    bl_idname = "pskpsa.fix_dbd_survivor_active_action_operator"

    def execute(self, context):
        fix_dbd_survivor_active_action()
        
        return {'FINISHED'}

def fix_dbd_killer_active_action():
    is_problem_jaw_bone = get_is_problem_jaw_bone_var()

    active_object = bpy.context.active_object
    if (active_object.type == "ARMATURE"):
        remove_problem_bones_transform_keyframes(active_object, is_problem_jaw_bone)
        success_message = "The Problem Animation has been fixed successfully!"
        bpy.ops.pskpsa.show_message_operator(message = success_message)
        log(success_message)

    #throw error message if active object is not a skeleton
    else:
        error_message = "Error: Active Object is not an Armature, ensure the active object is the Skeleton with problem animations."
        bpy.ops.pskpsa.show_message_operator(message = error_message)
        log(error_message)


def fix_dbd_survivor_active_action():
    active_object = bpy.context.active_object

    #only proceed to try and create an action with reset rotation and 
    #location for bones if the selected object is an armature
    if (active_object.type == "ARMATURE"):
        #before anything else push down current active action down to an NLA track
        push_active_action_to_nla_track(active_object)

        bpy.ops.object.mode_set(mode='POSE')

        #deselect all the bones as all bones will start off 
        #selected when going to pose mode
        bpy.ops.pose.select_all(action='DESELECT')

        #make a new action
        fix_surv_face_action = bpy.data.actions.new('FixSurvivorFacialAnimations')
        #switch the active action to the newly created action
        active_object.animation_data.action = fix_surv_face_action

        #select the face bones
        #remember joint_Head_01 is not included 
        #because otherwise the character will not rotate their head correctly 
        survivor_problem_face_bones = ["joint_FacialGroup", "cheek_LT_01", "cheek_RT_01", "cheekbone_LT_01", "cheekbone_LT_02", "cheekbone_LT_03", "cheekbone_LT_04", "cheekbone_RT_01", "cheekbone_RT_02", "cheekbone_RT_03", "cheekbone_RT_04", "eye_LT", "eye_RT", "eyebrows_LT_01", "eyebrows_LT_02", "eyebrows_LT_03", "eyebrows_LT_04", "eyebrows_RT_01", "eyebrows_RT_02", "eyebrows_RT_03", "eyebrows_RT_04", "eyelids_down_LT", "eyelids_down_RT", "eyelids_up_LT", "eyelids_up_RT", "forehead_LT", "forehead_RT", "jaw", "chin", "tongue_01", "tongue_02", "tongue_03", "sneer_RT_04", "sneer_LT_04", "lips_down_RT_03", "lips_down_RT_02", "lips_down_RT_01", "lips_down_LT_03", "lips_down_LT_02", "lips_down_LT_01", "lips_down_mid", "nose", "sneer_LT_01", "sneer_LT_02", "sneer_LT_03", "sneer_RT_01", "sneer_RT_02", "sneer_RT_03", "lips_up_mid", "lips_up_RT_01", "lips_up_RT_02", "lips_up_LT_01", "lips_up_LT_02", "lips_up_LT_03", "lips_up_RT_03"]
        
        #select all bones from the survivor_problem_face_bones list
        for bone_name in survivor_problem_face_bones:
            #get the bone if the bone with the bone_name
            #exists: returns pose bone
            #does not exist: returns None
            bone_to_select = active_object.pose.bones.get(bone_name)

            #if bone with current bone name exists
            #select it
            if bone_to_select is not None:
                #select bone
                #because it is a pose bone you need to turn it
                #into a bone with .bone as the pose bone does not 
                #have a select attribute
                bone_to_select.bone.select = True

            #otherwise if bone with current bone name does not exist
            #do nothing as you cannot select a non existent bone
        

        #clear the location, rotation, scale transforms
        #for the problem bones which should now be selected
        bpy.ops.pose.loc_clear()
        bpy.ops.pose.rot_clear()
        bpy.ops.pose.scale_clear()

        #make a keyframe and push it down to an NLA track
        bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')

        #push the offset facial keyframe down to nla track
        #on top of any other currently active action
        push_active_action_to_nla_track(active_object)


def push_active_action_to_nla_track(active_object):
        action = active_object.animation_data.action
        #safety measure check there is a keyframe before trying to push down
        #the action to an Non Linear Animation track
        if action is not None:
            track = active_object.animation_data.nla_tracks.new()
            track.strips.new(action.name, action.frame_range[0], action)
            #set the active action to be something else
            active_object.animation_data.action = None
            


#---------------fix all the actions action for killer and survivor 
class PSKPSA_OT_fix_all_dbd_killer_actions(bpy.types.Operator):
    bl_label = "Fix ALL Dead By Daylight Killer Actions"
    bl_description = "Reset transforms for problem bones for all actions on the Killer skeleton"
    bl_idname = "pskpsa.fix_all_dbd_killer_actions_operator"

    def execute(self, context):
        fix_all_dbd_killer_actions()       

        return {'FINISHED'}


def fix_all_dbd_killer_actions():
    is_problem_jaw_bone = get_is_problem_jaw_bone_var()
    active_object = bpy.context.active_object
    if (active_object.type == "ARMATURE"):
        #record the action the user was on to return them to the action when
        #all actions have been fixed
        first_action_user = active_object.animation_data.action

        #iterate through all actions on the skeleton
        #and remove the animations on problem bones for every action
        for current_action in bpy.data.actions:
            #switch active action to the next action
            active_object.animation_data.action = current_action
            remove_problem_bones_transform_keyframes(active_object, is_problem_jaw_bone)

        success_message = "All Problem Animations have been fixed successfully!"
        bpy.ops.pskpsa.show_message_operator(message = success_message)
        log(success_message)

        #switch active action back to the first selected user action so it doesn't confuse users 
        active_object.animation_data.action = first_action_user

    #throw error message if active object is not a skeleton
    else:
        error_message = "Error: Active Object is not an Armature, ensure the active object is the Skeleton with problem animations."
        bpy.ops.pskpsa.show_message_operator(message = error_message)
        log(error_message)

#----------------common shared functions between fix one active action and all actions 

def get_is_problem_jaw_bone_var():
    #store active scene to variable
    scene = bpy.context.scene
    #allow access to user inputted properties through pointer
    #to properties
    fixdbdanimtool = scene.fixdbdanim_tool

    return fixdbdanimtool.is_problem_jaw_bone

#this function will remove keyframes from problem bones and
#reset their transforms to default for one action
def remove_problem_bones_transform_keyframes(active_object, is_problem_jaw_bone):
    armature = active_object

    bpy.ops.object.mode_set(mode='POSE')

    #deselect all the bones as all bones will start off 
    #selected when going to pose mode
    bpy.ops.pose.select_all(action='DESELECT')

    #set the current frame to frame 0
    #so the playback head is on frame 0
    #the reason why is so that any keyframes
    #used to correct the broken animations are on frame zero
    bpy.context.scene.frame_set(0)
    
    #----------define problem bones arrays outside for loop over all pose bones
    #so arrays are not constantly redefined

    #the problem bones for broken killer animations are bones 
    #which have roll and ik in their names
    killer_problem_bones_array = ["roll", "ik"]

    #this iterates through all the bones
    #removing keyframes and transforms from every bone that
    #is a problem bone meaning it contains the substring roll and ik
    for bone in armature.pose.bones:
        #use lowercase to catch bones 
        #which have mixed case names
        lowercase_bone_name = bone.name.lower()

        #if this is for killer animations 
        #remove animations from ik and roll bones

        #iterate over all problem bones
        #check if lowercase_bone_name contains the substring problem bone
        for problem_bone in killer_problem_bones_array:
            #check if lowercase_bone_name contains the substring
            if(problem_bone in lowercase_bone_name):
                remove_animations_from_bone(armature, bone)
            
                #break from for loop if found
                #as the bone has now lost
                #all keyframes and transforms
                #there is no need to check if the problem_bone
                #is in 
                #is the keyframes
                #need to be removed again
                break
        

        #the jaw bone sometimes has problems on some dbd killer
        #skeletons and not others so we give the user the option to clear
        #transforms or not
        #if the user has selected to clear transforms
        #on the jaw bone because the animations are not
        #working for it and the current bone name contains jaw in it
        #accounting for mixed case
        #then remove all animations from this bone
        if(is_problem_jaw_bone and "jaw" in lowercase_bone_name):
            remove_animations_from_bone(armature, bone)

        
    
    #set back to object mode so the user can go about their business
    bpy.ops.object.mode_set(mode='OBJECT')


#this function will remove all keyframes
#and clear transforms for one bone
def remove_animations_from_bone(armature, bone):
    #deselect all the bones between each loop of clearing keyframes
    bpy.ops.pose.select_all(action='DESELECT')

    #select the bone in pose mode so the transforms can be cleared
    #off the selected bone
    armature.data.bones[bone.name].select = True

    #clear the location, rotation, scale transforms
    #for the problem bones
    bpy.ops.pose.loc_clear()
    bpy.ops.pose.rot_clear()
    bpy.ops.pose.scale_clear()

    #clear the keyframes for the selected animation
    bpy.ops.anim.keyframe_clear_v3d()

    #make one keyframe otherwise when you move the playback head
    #it will revert to the broken animations
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')




#--------------------------------Show feedback to user class and function

#class that is shown when a message needs to 
#pop up for the user as feedback
class PSKPSA_OT_show_message(bpy.types.Operator):
    bl_idname = "pskpsa.show_message_operator"
    bl_label = ""
    bl_description = "Show Message for PSK PSA importer"
    bl_options = {'REGISTER'}
    message: bpy.props.StringProperty(default="Message Dummy")
    called: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=700)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=self.message)

    def execute(self, context):
        if not self.called:
            wm = context.window_manager
            self.called = True
            return wm.invoke_props_dialog(self, width=700)
        return {'FINISHED'}

#function used to log to console success and error messages
def log(msg):
    print("[PSK/PSA DBD Fix]:", msg)


classes = [fix_dbd_animations_properties, PSKPSA_PT_fix_dbd_animations_import_panel_2,

PSKPSA_OT_fix_dbd_killer_active_action, PSKPSA_OT_fix_dbd_survivor_facial_anim,
PSKPSA_OT_fix_all_dbd_killer_actions,

PSKPSA_OT_show_message]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    #register fixdbdanim_tool as a type which has all
    #the user input properties from the properties class
    #use a unique name so you don't stop other add ons
    #working which also register pointer properties
    bpy.types.Scene.fixdbdanim_tool = bpy.props.PointerProperty(type = fix_dbd_animations_properties)
 
def unregister():
    #unregister in reverse order to registered so classes relying on other classes
    #will not lead to an error
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    #unregister fixdbdanim_tool as a type
    del bpy.types.Scene.fixdbdanim_tool
 
 
if __name__ == "__main__":
    register()