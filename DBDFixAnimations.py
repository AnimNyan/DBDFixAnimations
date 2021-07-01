import bpy

class fix_dbd_animations_properties(bpy.types.PropertyGroup):
    is_problem_jaw_bone: bpy.props.BoolProperty(name="Fix Jaw Bone", default = False)


class PSKPSA_PT_fix_dbd_animations_import_panel_2(bpy.types.Panel):
    bl_label = "Fix DBD Animations"
    bl_idname = " PSKPSA_PT_fix_skeletons_import_panel_2"
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
        layout.label(text ="Animations > Press Fix Dead By Daylight Killer Animation")
        layout.operator("pskpsa.use_fix_dbd_active_animation_operator")
        layout.label(text ="To fix ALL Actions > Press Fix ALL Dead By Daylight Killer Actions")
        layout.operator("pskpsa.fix_all_dbd_actions_operator")


class PSKPSA_OT_fix_dbd_active_animation(bpy.types.Operator):
    bl_label = "Fix Dead By Daylight Killer Animation"
    bl_description = "Reset transforms for problem bones for one active Action"
    bl_idname = "pskpsa.use_fix_dbd_active_animation_operator"

    def execute(self, context):
        #store active scene to variable
        scene = context.scene
        #allow access to user inputted properties through pointer
        #to properties
        fixdbdanimtool = scene.fixdbdanim_tool

        is_problem_jaw_bone = fixdbdanimtool.is_problem_jaw_bone

        active_object = bpy.context.active_object
        if (active_object.type == "ARMATURE"):
            remove_problem_bones_animations(active_object, is_problem_jaw_bone)
            success_message = "The Problem Animation has been fixed successfully!"
            bpy.ops.fuseskeletons.show_message(message = success_message)
            log(success_message)

        #throw error message if active object is not a skeleton
        else:
            error_message = "Error: Active Object is not an Armature, ensure the active object is the Skeleton with problem animations."
            bpy.ops.fuseskeletons.show_message(message = error_message)
            log(error_message)
        
        return {'FINISHED'}


class PSKPSA_OT_fix_all_dbd_actions(bpy.types.Operator):
    bl_label = "Fix ALL Dead By Daylight Killer Actions"
    bl_description = "Reset transforms for problem bones for all actions on the skeleton"
    bl_idname = "pskpsa.fix_all_dbd_actions_operator"

    def execute(self, context):
        #store active scene to variable
        scene = context.scene
        #allow access to user inputted properties through pointer
        #to properties
        fixdbdanimtool = scene.fixdbdanim_tool

        is_problem_jaw_bone = fixdbdanimtool.is_problem_jaw_bone

        active_object = bpy.context.active_object
        if (active_object.type == "ARMATURE"):
            #iterate through all actions on the skeleton
            #and remove the animations on problem bones for every action
            for current_action in bpy.data.actions:
                #switch active action to the next action
                active_object.animation_data.action = current_action
                remove_problem_bones_animations(active_object, is_problem_jaw_bone)

            success_message = "All Problem Animations have been fixed successfully!"
            bpy.ops.fuseskeletons.show_message(message = success_message)
            log(success_message)

        #throw error message if active object is not a skeleton
        else:
            error_message = "Error: Active Object is not an Armature, ensure the active object is the Skeleton with problem animations."
            bpy.ops.fuseskeletons.show_message(message = error_message)
            log(error_message)
        
        return {'FINISHED'}


#this function will remove animations from problem bones and
#reset their transforms to default
def remove_problem_bones_animations(active_object, is_problem_jaw_bone):
    armature = active_object

    bpy.ops.object.mode_set(mode='POSE')

    #deselect all the bones as they will start 
    #off selected when going to pose mode
    bpy.ops.pose.select_all(action='DESELECT')

    #set the current frame to frame 0
    #so the playback head is on frame 0
    #the reason why is so that any keyframes
    #used to correct the broken animations are on frame zero
    bpy.context.scene.frame_set(0)

    for bone in armature.pose.bones:
        #use lowercase to catch bones 
        #which have mixed case names
        lowercase_bone_name = bone.name.lower()

        #the problem bones are bones which have roll and ik in their names
        if("roll" in lowercase_bone_name or "ik" in lowercase_bone_name):
            remove_animations_from_bone(armature, bone)
        
        #the jaw bone sometimes has problems but only on some dbd killer
        #skeletons and not others so we give the user the option to clear
        #transforms or not

        #if the user has selected to clear transforms
        #on the jaw bone because the animations are not
        #working for it and the current bone name is joint_jaw01
        #accounting for mixed case
        #then remove all animations from this bone
        if(is_problem_jaw_bone and lowercase_bone_name == "joint_jaw01"):
            remove_animations_from_bone(armature, bone)
    
    #set back to object mode so the user can go about their business
    bpy.ops.object.mode_set(mode='OBJECT')



def remove_animations_from_bone(armature, bone):
    #deselect all the bones between each loop of clear
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




#--------------------------------Show feedback to user functions

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
PSKPSA_OT_fix_dbd_active_animation, PSKPSA_OT_fix_all_dbd_actions,
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