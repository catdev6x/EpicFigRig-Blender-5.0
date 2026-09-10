# Copyright (C) 2020-2023 The EpicFigRig Team
# https://github.com/BlenderBricks/EpicFigRig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#add-on info

bl_info = {
    "name": "The EpicFigRig (Blender 5.0 Fix by catdev6x)",
    "author": "JabLab, IX Productions, Citrine's Animations, Jambo, Owenator Productions, Golden Ninja Ben & catdev6x",
    "version": (1, 3, 2),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > EpicFigRig",
    "description": "An Epic Minifigure Rig for Blender 5.0 — Never gonna give your rig up, never gonna let your bones down.",
    "doc_url": "https://github.com/BlenderBricks/EpicFigRig",
    "category": "Animation",
}

selected_armature = "FinishedRig"

import os
import bpy, mathutils
from bpy.props import BoolProperty, IntProperty
from bpy.types import PropertyGroup, Panel, Scene
import addon_utils

addon_dirc = os.path.dirname(os.path.realpath(__file__))

def set_bone_select(armature_obj, bone_name, state=True):
    if armature_obj:
        if hasattr(armature_obj, "pose") and armature_obj.pose and bone_name in armature_obj.pose.bones:
            pbone = armature_obj.pose.bones[bone_name]
            if hasattr(pbone, "select"):
                pbone.select = state
                return
        if hasattr(armature_obj, "data") and armature_obj.data and hasattr(armature_obj.data, "bones") and bone_name in armature_obj.data.bones:
            bone = armature_obj.data.bones[bone_name]
            if hasattr(bone, "select"):
                bone.select = state

def hide_bone_compat(armature_obj, bone_name, state=True):
    if armature_obj:
        if hasattr(armature_obj, "data") and armature_obj.data and hasattr(armature_obj.data, "bones"):
            bone = armature_obj.data.bones.get(bone_name)
            if bone:
                bone.hide = state
        if hasattr(armature_obj, "pose") and armature_obj.pose:
            pbone = armature_obj.pose.bones.get(bone_name)
            if pbone and hasattr(pbone, "hide"):
                pbone.hide = state
#PANELS

class EpicFigRigPanel(bpy.types.Panel):
    
    bl_label = "The EpicFigRig"
    bl_idname = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        box = layout.box()
        row = box.row()
        row.operator("wm.url_open", text="JabLab User Manual", icon= 'URL', emboss= False).url = "https://docs.google.com/document/d/1DUYLJnJKtjcgSzyi8djITjD8QRpN_i40ziz6wifAG0Q/edit?usp=sharing"
        #row = layout.row()
        #box = layout.box()
        #row = box.row()
        #row.operator("wm.url_open", text="JabLab Roadmap", icon= 'URL', emboss= False).url = "https://docs.google.com/document/d/1kJMUFe73h4Af69KkrOU4y_3KU6dmt_5DmBlqC_X1Q5E/edit?usp=sharing"
        #row = layout.row()
        #row.label(text= "Active: "+ bpy.context.object.data.name, icon= 'RESTRICT_SELECT_OFF')
        #row = layout.row()
        #row.label(text= bpy.context.object.data.name) #emboss= False)
        
        
        row = layout.row(align=True)
        box = layout.box()
        row = box.row()
        row.operator('auto.rig')
        row = layout.row(align=True)
        
        box = layout.box()  
        row = box.row()
        row.label(text="More Rigging:")
        box.prop(scene, "normalize_mini")
        row = box.row()
        row.operator('prox.rig')
        row = box.row(align=True)  
        row.operator('propa.rig')
        row.operator('propb.rig')
        row = box.row()
        row = layout.row()
           
        row = layout.row()
        row.label(text= "Rig Settings:", icon= 'OPTIONS')
        row = layout.row()
        layout = self.layout
        row = layout.row(align=True)        
        row.operator('main.tab')
        row.operator('advanced.tab')
        row = layout.row()

######MAIN TAB######

class EpicButtons(bpy.types.Panel):
        
    bl_idname = "EPIC_PT_BUTTONS"
    bl_label = "Epic Buttons"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'
    
    @classmethod
    def poll(cls, context):
        #if bpy.context.object.data["RigTabs"] == 0:
        if bpy.context.scene.EpicRigTabs == 0:
            return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        row = layout.row()
        row.label(text= "Accessory Snapping:", icon= 'SNAP_ON')
        row = layout.row(align=True)
        row.operator('snap_left.add')
        row.operator('snap_right.add')
        row = layout.row(align=True)
        row.operator('snap_head.add')
        #pivot buttons
        layout.label(text="Pivot Foot Switch:", icon= 'ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.operator('pivot.left')
        row.operator('pivot.right')
        row = layout.row()
        row.operator('reset.pivot')
        layout.label(text="Pivot Body Switch:", icon='CON_PIVOT')
        row = layout.row(align=True)
        row.operator('pivot_body.enable', text="Enable")
        row.operator('pivot_body.disable', text="Disable")
        row = layout.row(align=True)
        row.label(text= "Master Bone Control:")
        row = layout.row()
        row.operator('rig.reset')
        row = layout.row()
        row.operator('snap.masterbone') 

class SmearSlider(bpy.types.Panel):
    
    bl_label = "Smears"
    bl_idname = "EPIC_PT_smear_slider"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        if context.scene.EpicRigTabs != 1:
            return False
        obj = context.active_object
        return bool(obj and obj.type == 'ARMATURE' and obj.pose and "MasterBone" in obj.pose.bones)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["LLegSmear"]', slider=True)
        row = layout.row() 
        row.prop(context.active_object.pose.bones["MasterBone"], '["RLegSmear"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["LArmSmear"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["RArmSmear"]', slider=True)

class ArmMenu(bpy.types.Panel):
    bl_label = "Arm Menu"
    bl_idname = "EPIC_PT_arm_menu"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "EpicFigRig"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        sub = row.row()
        sub.enabled = True

        check_prop = False
        for obj in bpy.context.selected_objects:
            if obj.type == 'ARMATURE':
                global selected_armature
                selected_armature = obj.name
                check_prop = True
                break

        if not check_prop or not context.active_object or context.active_object.type != 'ARMATURE' or not context.active_object.pose:
            row.label(text="(Select an Armature for Settings)")
        else:
            if bpy.context.active_object.pose.bones["MasterBone"]["Hand Menu"] == 0:
                sub.enabled = True
                sub = row.row()
                row = layout.row()
                row = layout.row(align=True)
                row.operator('left_hand.menu', icon='EVENT_L')
                row.operator('right_hand.menu')
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["LeftArmIK"]', slider=True)

                if bpy.context.active_object.pose.bones["MasterBone"]["LeftArmIK"] == 0:
                    sub.enabled = True
                    row = self.layout.row()
                    sub = row.row()
                    row = layout.row(align=True)
                    row.operator('fk_to.ik_larm')
                    row = layout.row()
                else:
                    sub.enabled = True
                    row = self.layout.row()
                    sub = row.row()
                    row = layout.row(align=True)
                    row.operator('ik_to.fk_larm')
                    row = layout.row()

                row.prop(context.active_object.pose.bones["MasterBone"], '["IK Arm Socket Lock"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["Invert Left Arm"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["Mirror Left Arm"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["LArmSmear"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["Clay Left Arm Visibility"]', slider=True)

            else:
                sub.enabled = True
                sub = row.row()
                row = layout.row()
                row = layout.row(align=True)
                row.operator('left_hand.menu')
                row.operator('right_hand.menu', icon='EVENT_R')
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["RightArmIK"]', slider=True)

                if bpy.context.active_object.pose.bones["MasterBone"]["RightArmIK"] == 0:
                    sub.enabled = True
                    row = self.layout.row()
                    sub = row.row()
                    row = layout.row(align=True)
                    row.operator('fk_to.ik_rarm')
                    row = layout.row()
                else:
                    sub.enabled = True
                    row = self.layout.row()
                    sub = row.row()
                    row = layout.row(align=True)
                    row.operator('ik_to.fk_rarm')
                    row = layout.row()

                row.prop(context.active_object.pose.bones["MasterBone"], '["IK Arm Socket Lock"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["Invert Right Arm"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["Mirror Right Arm"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["RArmSmear"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["Clay Right Arm Visibility"]', slider=True)

            row = layout.row()
            row.prop(context.active_object.pose.bones["MasterBone"], '["Lepin Hands"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.pose.bones["MasterBone"], '["Auto Arm Rotation"]', slider=True)


class LeftHandMenu(bpy.types.Operator):
    """Left Hand Menu"""
    bl_label = "Left Hand"
    bl_idname = 'left_hand.menu'
    
    def execute(self, context):
        bpy.context.active_object.pose.bones["MasterBone"]["Hand Menu"] = 0
        return {'FINISHED'}
    
class RightHandMenu(bpy.types.Operator):
    """Right Hand Menu"""
    bl_label = "Right Hand"
    bl_idname = 'right_hand.menu'
    
    def execute(self, context):
        bpy.context.active_object.pose.bones["MasterBone"]["Hand Menu"] = 1
        return {'FINISHED'}
               
class LegMenu(bpy.types.Panel):
    bl_label = "Leg Menu"
    bl_idname = "EPIC_PT_leg_menu"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.EpicRigTabs == 0

    def draw(self, context):
        layout = self.layout

        check_prop = False
        for obj in bpy.context.selected_objects:
            if obj.type == 'ARMATURE':
                global selected_armature
                selected_armature = obj.name
                check_prop = True
                break
                
        if not check_prop or not context.active_object or context.active_object.type != 'ARMATURE' or not context.active_object.pose:
            row.label(text = "(Select an Armature for Settings)")
        else:
            if bpy.context.active_object.pose.bones["MasterBone"]["Leg Menu"] == 0:
                row = layout.row()
                row = layout.row(align=True)
                row.operator('left_leg.menu', icon= 'EVENT_L')
                row.operator('right_leg.menu')    
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["LeftLegIK"]', slider=True)
                if bpy.context.active_object.pose.bones["MasterBone"]["LeftLegIK"] == 0:
                    sub.enabled = True
                    row = self.layout.row()
                    sub = row.row()
                    row = layout.row(align=True)
                    row.operator('fk_to.ik_lleg')
                    row = layout.row()
                else:
                    sub.enabled = True
                    row = self.layout.row()
                    sub = row.row()
                    row = layout.row(align=True)
                    row.operator('ik_to.fk_lleg')
                    row = layout.row()
                      
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["Invert Left Leg"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["LLegSmear"]', slider=True)
                row = layout.row()           
            else:
                row = layout.row()
                row = layout.row(align=True)
                row.operator('left_leg.menu')
                row.operator('right_leg.menu', icon= 'EVENT_R')
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["RightLegIK"]', slider=True)
                if bpy.context.active_object.pose.bones["MasterBone"]["RightLegIK"] == 0:
                    sub.enabled = True
                    row = self.layout.row()
                    sub = row.row()
                    row = layout.row(align=True)
                    row.operator('fk_to.ik_rleg')
                    row = layout.row()
                else:
                    sub.enabled = True
                    row = self.layout.row()
                    sub = row.row()
                    row = layout.row(align=True)
                    row.operator('ik_to.fk_rleg')
                    row = layout.row()

                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["Invert Right Leg"]', slider=True)
                row = layout.row()
                row.prop(context.active_object.pose.bones["MasterBone"], '["RLegSmear"]', slider=True)
                row = layout.row()
                
class LeftLegMenu(bpy.types.Operator):
    """Left Leg Menu"""
    bl_label = "Left Leg"
    bl_idname = 'left_leg.menu'
    
    def execute(self, context):
        bpy.context.active_object.pose.bones["MasterBone"]["Leg Menu"] = 0
        return {'FINISHED'}
    
class RightLegMenu(bpy.types.Operator):
    """Right Leg Menu"""
    bl_label = "Right Leg"
    bl_idname = 'right_leg.menu'
    
    def execute(self, context):
        bpy.context.active_object.pose.bones["MasterBone"]["Leg Menu"] = 1
        return {'FINISHED'}

######ADVANCED TAB######

class BoneAdjust(bpy.types.Panel):
    
    bl_label = "Bone Adjustments"
    bl_idname = "EPIC_PT_bone_adjust"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        if context.scene.EpicRigTabs != 1:
            return False
        obj = context.active_object
        return bool(obj and obj.type == 'ARMATURE' and obj.pose and "MasterBone" in obj.pose.bones)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Head Accessory Bone Scale"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Head Bone Scale"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Head Bone Transform"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Torso Bone Scale"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Leg Height"]', slider=True)
        row = layout.row()
        
class BoneVis(bpy.types.Panel):
    
    bl_label = "Bone Visibility"
    bl_idname = "EPIC_PT_bone_visibility"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        if context.scene.EpicRigTabs != 1:
            return False
        obj = context.active_object
        return bool(obj and obj.type == 'ARMATURE' and obj.pose and "MasterBone" in obj.pose.bones)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Second Master Bone"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Locators"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Clay Right Arm Visibility"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Clay Left Arm Visibility"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Prop Bone A Visibility"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Prop Bone B Visibility"]', slider=True)
        
        

class BoneShapes(bpy.types.Panel):
    
    bl_label = "Bone Shapes"
    bl_idname = "EPIC_PT_bone_shapes"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        if context.scene.EpicRigTabs != 1:
            return False
        obj = context.active_object
        return bool(obj and obj.type == 'ARMATURE' and obj.pose and "MasterBone" in obj.pose.bones)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Left Hand Shape"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Right Hand Shape"]', slider=True)

class Props(bpy.types.Panel):
    
    bl_label = "Props"
    bl_idname = "EPIC_PT_props"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        if context.scene.EpicRigTabs != 1:
            return False
        obj = context.active_object
        return bool(obj and obj.type == 'ARMATURE' and obj.pose and "MasterBone" in obj.pose.bones)
        
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Prop A"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Prop A Transform"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Prop A Rotation"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Prop B"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Prop B Transform"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.pose.bones["MasterBone"], '["Prop B Rotation"]', slider=True)
        row = layout.row()        
        row.prop(context.active_object.pose.bones["MasterBone"], '["Back Hip Parent"]', slider=True)
        
        
#BUTTONS 

#Auto Rig
class AutoRig(bpy.types.Operator):
    """Autorig Selected Minifgure - YOU MUST DELETE THE EMPTY!"""
    bl_label = "  Rig Selected Minifigure  "
    bl_idname = 'auto.rig'
    
    #mininame: bpy.props.StringProperty(name = "Minifigure Name:", default= "")
    
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if len(context.selected_objects) < 2:
            self.report({'ERROR'}, "Select the minifigure parts and the empty before rigging")
            return {'CANCELLED'}
        
        child = True
        
        #turns on Copy attributes add-on if not enabled
        if addon_utils.check("space_view3d_copy_attributes") == (False, False):
            addon_utils.enable("space_view3d_copy_attributes")
            addon_utils.check("space_view3d_copy_attributes")
        
        #Naming()
        
        #mname = self.mininame
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[1]
        col = bpy.context.active_object.users_collection[0]
        mname = col.name
        
        collections = bpy.context.view_layer.layer_collection.children

        for collection in collections:
            if collection.name == mname:
                bpy.context.view_layer.active_layer_collection = collection
        
        
        def driverCreate(context, object, armatures, path, Bo_nus, path2, expression, x, y, xx, yy):
            if not Bo_nus:
                return

            obj = bpy.data.objects.get(object)
            rig_obj = bpy.data.objects.get(armatures)
            if not obj or not rig_obj:
                return

            prop_name = path2.replace("[", "").replace("]", "").replace('"', "").replace("'", "")

            for prop in ("hide_viewport", "hide_render"):
                dwive = obj.driver_add(prop)
                for mod in list(dwive.modifiers):
                    dwive.modifiers.remove(mod)
                driver = dwive.driver
                driver.type = 'SCRIPTED'
                for v in list(driver.variables):
                    driver.variables.remove(v)

                var = driver.variables.new()
                var.type = 'SINGLE_PROP'
                var.name = "smear"
                target = var.targets[0]
                target.id_type = 'OBJECT'
                target.id = rig_obj
                target.data_path = f'pose.bones["MasterBone"]["{prop_name}"]'
                driver.expression = "1 if smear > 0.001 else 0"
        
        #remove empty
        if bpy.context.selected_objects[0].parent:
            empty_name = bpy.context.selected_objects[0].parent.name
            empty = bpy.data.objects[empty_name]
            bpy.data.objects.remove(empty)

        def append_rig():
            path = addon_dirc + "/Append.blend/Collection/"
            object_name = "The EpicFigRig"
            bpy.ops.wm.append(filename = object_name, directory = path)

        def append_cape():
            path = addon_dirc + "/Cape_Rig.blend/Collection/"
            object_name = "CapeRig"
            bpy.ops.wm.append(filename = object_name, directory = path)
            #path = addon_dirc + "/Cape_Rig.blend/Object/"
            #bpy.ops.wm.append(filename = currentcape, directory = path)
            
        def append_skirt():
            path = addon_dirc + "/Skirt_Rig.blend/Collection/"
            object_name = "SkirtRig"
            bpy.ops.wm.append(filename = object_name, directory = path)
        

        leg_l = ["77338", "3817", "20926", "24083", "37364p2", "37366", "LEGL"]
        leg_r = ["77337", "3816", "20932", "24082", "37364p1", "2532", "LEGR"]
        head_epic = ["24581", "3626", "28621", "94590", "28650", "28649", "26683", "93248",
        "30480", "30378", "98103", "64804", "92743", "1735", "24601", "24629", "98365", 
        "98384", "93068", "19729", "20613", "41201", "18828", "65431", "HEADEPIC"]
        arm_r = ["16000", "3818", "62691","ARMR"]
        arm_l = ["16001", "3819", "62691","ARML"]
        torso = ["3814","TORSO"]
        torso_gear = ["95348", "61976", "6132", "93223", "93069", "10052", "10065", "42446", "48724", "92590", "4523", "2524", "12397", "4498", "2526", "30133", "2610", "97895", "38781", "3838", "3840", "2587", "72326",  "11260", "15339", "30091", "15490", "15428", "34685", "24135", "18986", "15423", "98132", "24097", "22402", "28350", "12618", "19723", "4524", "11097", "26966", "93250", "99250", "26073", "4736", "11438", "15406", "18827", "27325", "10183", "6158", "27148", "27151", "27147", "98722", "64802", "23983", "28716", "25376", "30174", "24588", "15086", "13791", "20566", "24217", "88295", "39260", "41637", "34706", "41811", "39796", "41162", "41202", "37822", "65183", "79786", "34721p2"]
        hand_epic = ["3820", "2531", "9532"]
        child_leg = ["37365", "37366", "16709", "37679", "41879"]
        child_leg_single = ["16709", "37679", "41879"]
        dress_brick = ["3678", "75103", "98376", "19859"]
        regular_dress = ["36036", "95351"]
        head_accessory = ["64798", "64807", "85974", "87990", "87991", "87995", "88283", "88286", "92081", "92083", "93217", "93562", "93563", "18228", "99240", "11908", "99930", "99248",
        "98726", "10301", "10166", "10048", "10048", "10055", "10066", "11256", "12893", "13768", "13251", "13664", "13785", "13750", "13765", "13766", "15443", "15427", "15491", "15500",
        "15485", "17346", "17630", "18858", "21787", "20688", "20877", "20595", "20597", "20596", "21777", "21268", "21269", "21778", "23186", "23187", "24072", "25775", "28798", "25378",
        "25379", "26139", "25972", "27186", "27385", "27160", "28551", "28144", "28149", "27323", "28664", "28432", "28432", "25411", "25412", "25409", "28430", "34316", "25405", "34693", 
        "36060", "36489", "37823", "40938", "3901", "62810", "40239", "3625", "96859", "62711", "6093", "62696", "59363", "95225", "6025", "99245", "92746", "61183", "40240", "98371", "20603", 
        "21788", "21789", "92756", "40233", "24071", "28139", "65425", "35182", "35620", "49362", "92259", "18637", "15675", "18640", "92255", "19196", "65471", "65463", "66912", "3842", "50665", "16599", "30124", "49663",          "36293", "93560", "35458",
        "15851", "3834", "90541", "4505", "26079", "4506", "2338", "3844", "3896", "48493",
        "30273", "89520", "4503", "71015", "2544", "2528", "2543", "23973", "30048", "93554",
        "2545", "40235", "18822", "3629", "30167", "61506", "15424", "13565",  "13788", "13746",
        "6131", "4485", "86035", "11303", "93219", "35660", "11258", "3878", "3624", "41334",
        "3898", "30287", "95678", "36933", "62537", "46303", "3833", "16178", "16175", "98289",
        "99254", "43057", "22380", "85975", "90386", "98381", "30370", "61189", "11217", "15308",
        "30369", "23947", "20904", "20905", "20950", "98119", "21829", "30561", "16497", "57900",
        "52345", "20908", "20954", "21557", "19916", "19917", "87610", "87571", "60768", "92761",
        "6030", "10051", "10056d1", "13767", "10173", "30171", "15530", "17351", "99244", "25971",
        "18831", "66972", "18819", "24076", "25977", "29575", "35697", "20695", "95674", "95319",
        "13789", "30381", "10113", "27161", "18987", "98729", "27326", "10907", "10908", "28631",
        "20917", "17016", "11620", "10909", "15554", "33862", "18936", "19303", "25264", "19026",
        "65589", "19730", "18962", "98130", "96034", "98133", "19857", "24496", "24504", "40925",
        "65072", "93059", "26007", "98128", "25407", "25742", "25743", "25748", "25113", "25114",
        "28679", "30668", "96204", "18984", "90388", "24073", "19861", "90392", "98366", "25978",
        "15404", "98378", "22425", "13792", "13787", "11265", "30172", "27955", "37038", "10164",
        "34704", "54001", "52684", "93557", "65532", "30926", "67145", "66917", "11420"]

        head_clothing_accessories = ["91190", "64647", "30126", "98379", "12886", "33322",
        "25974", "14045", "25634", "13665", "24131", "44553", "41944", "54568", "87696",
        "87695", "11437", "22411", "88964", "39262", "35183"]

        head_clothing_visors = ["2447", "41805", "23318", "89159", "30170", "6119", "30090", 
        "15446", "2594", "22393", "22395", "22400", "22401", "22394", "23851", "28976",]
        
        capes = ["20547","23901","29453","34721p1","50231","50525","56630","56630","65384","99464",]
        
        skirts = ["txt2","txt3","33426","26697","68054"]

        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH' and obj.data]
        if not selected_objects:
            self.report({'ERROR'}, "No mesh objects found in selection")
            return {'CANCELLED'}
        loc = selected_objects[0]

        child = False 
        for fig in selected_objects:
            for num in child_leg:
                if num[:5] in fig.data.name:
                    child = True
           
        append_rig()      
        
        all_objects = bpy.data.objects
        rig = all_objects['Rig']
        arma = bpy.data.objects['Rig']
        arma_edit = arma.data.edit_bones
        
        #Moves rig to the location of the hips
        for y in selected_objects:
            if "3814" in y.data.name:
                if context.scene.normalize_mini == True:
                    bpy.data.objects[y.name].matrix_world = bpy.data.objects["Hip Empty"].matrix_world.copy()
                loc = y
            
        rig.location = loc.location

        collections = bpy.data.collections
        h = collections['BoneShapes']
        h.hide_viewport = True
        h.hide_render = True

        

        def parent( Bone_name, Dou_ble, Smear_prop, Empty_name):

            fig.select_set(True)
            fig.data = fig.data.copy()
            if Dou_ble == True:
                driverCreate(bpy.context, fig.name, rig.name, '["SmearsTest"]', True, Smear_prop, "hide + hide2", 0, 0, 1, 1)
            else:
                driverCreate(bpy.context, fig.name, rig.name, '["SmearsTest"]', False, Smear_prop, "hide", 0, 0, 1, 1)
            
            #Normalize Transforms
            if context.scene.normalize_mini == True:
                bpy.data.objects[fig.name].matrix_world = bpy.data.objects[Empty_name].matrix_world.copy()

            
            rig.select_set(True)
            bpy.context.view_layer.objects.active = rig
            rig.data.bones.active = rig.data.bones[Bone_name]
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)
            bpy.ops.object.select_all(action='DESELECT')
            
        
        for fig in selected_objects:

            #CHILD_LEG
            for num in child_leg_single:
                if num in fig.data.name:
                    parent("Torso", False, '["LLegSmear"]', "Hip Empty")
                    hide_bone_compat(rig, "RightFootIK", True)
                    hide_bone_compat(rig, "LeftFootIK", True)
                    hide_bone_compat(rig, "RightLeg", True)
                    hide_bone_compat(rig, "LeftLeg", True)

            #DRESS_BRICK
            for num in dress_brick:
                if num in fig.data.name:
                    parent("Torso", False, '["LLegSmear"]', "Hip Empty")
                    hide_bone_compat(rig, "RightFootIK", True)
                    hide_bone_compat(rig, "LeftFootIK", True)
                    hide_bone_compat(rig, "RightLeg", True)
                    hide_bone_compat(rig, "LeftLeg", True)

            #REGULAR_DRESS
            for num in regular_dress:
                if num in fig.data.name:
                    parent("Torso", False, '["LLegSmear"]', "Hip Empty")
                    hide_bone_compat(rig, "RightFootIK", True)
                    hide_bone_compat(rig, "LeftFootIK", True)
                    hide_bone_compat(rig, "RightLeg", True)
                    hide_bone_compat(rig, "LeftLeg", True)

            #LEFT_LEG
            for num in leg_l:
                if num in fig.data.name:
                    parent("LeftLegInvert", True, '["LLegSmear"]', "Left Leg Empty")
                    bpy.data.objects["LlegS"].material_slots[0].material = fig.material_slots[0].material


            #RIGHT_LEG
            for num in leg_r:
                if num in fig.data.name:
                    parent("RightLegInvert", True, '["RLegSmear"]', "Right Leg Empty")
                    bpy.data.objects["RlegS"].material_slots[0].material = fig.material_slots[0].material

            #IK_HIP
            if "3815" in fig.data.name:
                parent("Torso", False, '["LLegSmear"]', "Hip Empty")

            #TORSO_GEAR
            for num in torso_gear:
                if num in fig.data.name:
                    parent("Torso Rock", False, '["LLegSmear"]', "Head Empty")
                    bpy.data.objects["Rig"].pose.bones["MasterBone"]["Head Bone Transform"] = 1.5
                    bpy.data.objects["Rig"].pose.bones["MasterBone"]["Torso Bone Scale"] = .75

            #TORSO
            for num in torso:
                if num in fig.data.name:
                    parent("Torso Rock", False, '["LLegSmear"]', "Hip Empty")

            #LEFT_ARM
            for num in arm_l:
                if num in fig.data.name:
                    parent("Left Arm", True, '["LArmSmear"]', "Left Arm Empty")
                    bpy.data.objects["LarmS"].material_slots[0].material = fig.material_slots[0].material

            #RIGHT_ARM
            for num in arm_r:
                if num in fig.data.name:
                    parent("Right Arm", True, '["RArmSmear"]', "Right Arm Empty")
                    bpy.data.objects["RarmS"].material_slots[0].material = fig.material_slots[0].material
            
            #HEAD
            for num in head_epic:
                if num in fig.data.name:
                    parent("Head", False, '["LLegSmear"]', "Head Empty")

            #HEAD_ACCESSORY
            for num in head_accessory:
                if num in fig.data.name:
                    parent("Head Accessory", False, '["LLegSmear"]', "Hair Empty")
                    bpy.data.objects["Rig"].pose.bones["MasterBone"]["Head Bone Scale"] = .85
                    bpy.data.objects["Rig"].pose.bones["MasterBone"]["Head Accessory Bone Scale"] = 1.0
                    break
            
            #HEAD_CLOTHING.ACCESSORIES
            for num in head_clothing_accessories:
                if num in fig.data.name:
                    parent("Head Accessory", False, '["LLegSmear"]', "Hair Empty")

            #HEAD_CLOTHING.VISORS
            for num in head_clothing_visors:
                if num in fig.data.name:
                    parent("Head Accessory", False, '["LLegSmear"]', "Hair Empty")
            
            #CAPE
            for num in capes:
                if num in fig.data.name:
                    currentcape = fig.data.name[:5] + ".append"
                    #renamecape = fig.data.name[:7] + ".001"
                    #fig.data.name = renamecape
                    if currentcape == "34721.append":
                        currentcape = "34721p1.append"
                        
                    append_cape()
                    rigcape = bpy.data.objects['CapeRig']
                    rigcape.location = fig.location

                    LFarm = rigcape.pose.bones['LL'].constraints['Transformation']

                    LFarm.target = rig
                    LFarm.subtarget = "Left Arm"

                    LFarm2 = rigcape.pose.bones['LL'].constraints['Transformation.001']

                    LFarm2.target = rig
                    LFarm2.subtarget = "Left Arm Socket Control"

                    
                    RFarm = rigcape.pose.bones['RR'].constraints['Transformation']

                    RFarm.target = rig
                    RFarm.subtarget = "Right Arm"

                    RFarm2 = rigcape.pose.bones['RR'].constraints['Transformation.001']

                    RFarm2.target = rig
                    RFarm2.subtarget = "Right Arm Socket Control"

                    bpy.data.objects[currentcape].material_slots[0].material = fig.material_slots[0].material

                    bpy.ops.object.select_all(action='DESELECT')
                    fig.select_set(True)
                    bpy.context.view_layer.objects.active = fig
                    bpy.ops.object.delete() 
                    fig = rigcape
                    parent("Torso Rock", False, '["LLegSmear"]', "Head Empty")
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = None

                    #bpy.data.objects[currentcape].name = "FinishedCape"
                    bpy.context.scene.objects[currentcape].select_set(True)
                    for obj in bpy.context.selected_objects:
                        bpy.context.view_layer.objects.active = obj
                    obj = bpy.context.active_object                    
                    bpy.data.collections['CapeRig'].objects.link(obj)
                    bpy.data.collections['Cape Appends'].objects.unlink(obj)
                    bpy.ops.object.select_all(action='DESELECT')
                                
                    collection = bpy.data.collections.get('Cape Appends')
                    for obj in collection.objects:
                        bpy.data.objects.remove(obj, do_unlink=True)
    
                    bpy.data.collections.remove(collection)
                    
                    r = " Rig"
                    c = " Cape"
                    bpy.data.objects[currentcape].name = mname + c
                    bpy.data.objects['CapeRig'].name = mname + c + r
                    bpy.data.collections['CapeRig'].name = mname + c + r
                    bpy.data.collections['ShapesBones'].hide_viewport = True
                    bpy.data.collections['ShapesBones'].hide_render = True
                    #bpy.data.collections['ShapesBones'].name = 'FinishedShapesBones'
                                            
            #SKIRTS
            for num in skirts:
                if num in fig.data.name:
                    currentcape = f"{num}.append"
                        
                    append_skirt()
                    rigcape = bpy.data.objects['SkirtRig']
                    rigcape.location = fig.location

                    LFleg = rigcape.pose.bones['Front.L'].constraints['Transformation']

                    LFleg.target = rig
                    LFleg.subtarget = "LeftLeg"

                    LFleg2 = rigcape.pose.bones['Back.L'].constraints['Transformation']

                    LFleg2.target = rig
                    LFleg2.subtarget = "LeftLeg"

                    
                    RFleg = rigcape.pose.bones['Front.R'].constraints['Transformation']

                    RFleg.target = rig
                    RFleg.subtarget = "RightLeg"

                    RFleg2 = rigcape.pose.bones['Back.R'].constraints['Transformation']

                    RFleg2.target = rig
                    RFleg2.subtarget = "RightLeg"

                    bpy.data.objects[currentcape].material_slots[0].material = fig.material_slots[0].material

                    bpy.ops.object.select_all(action='DESELECT')
                    fig.select_set(True)
                    bpy.context.view_layer.objects.active = fig
                    bpy.ops.object.delete() 
                    fig = rigcape
                    parent("Torso", False, '["LLegSmear"]', "Skirt Empty")
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = None

                    #bpy.data.objects[currentcape].name = "FinishedCape"
                    bpy.context.scene.objects[currentcape].select_set(True)
                    for obj in bpy.context.selected_objects:
                        bpy.context.view_layer.objects.active = obj
                    obj = bpy.context.active_object                    
                    bpy.data.collections['SkirtRig'].objects.link(obj)
                    bpy.data.collections['Skirt Appends'].objects.unlink(obj)
                    bpy.ops.object.select_all(action='DESELECT')
                                
                    collection = bpy.data.collections.get('Skirt Appends')
                    for obj in collection.objects:
                        bpy.data.objects.remove(obj, do_unlink=True)
    
                    bpy.data.collections.remove(collection)
                    
                    r = " Rig"
                    c = " Cape"
                    bpy.data.objects[currentcape].name = mname + c
                    bpy.data.objects['SkirtRig'].name = mname + c + r
                    bpy.data.collections['SkirtRig'].name = mname + c + r
                    bpy.data.collections['SkirtShapes'].hide_viewport = True
                    bpy.data.collections['SkirtShapes'].hide_render = True
                    #bpy.data.collections['ShapesBones'].name = 'FinishedShapesBones'
                                    
            #HAND
            for num in hand_epic:
                if num in fig.data.name:
                    
                    shortestDist = float('inf')
                    handname = 'Right Hand'
                    for bname in ('Left Hand', 'Right Hand'):
                        pbone = rig.pose.bones.get(bname)
                        if pbone:
                            matrix_final = rig.matrix_world @ pbone.matrix
                            location = matrix_final.translation
                            handloc = (location - fig.location).length
                            if handloc < shortestDist:
                                shortestDist = handloc
                                handname = bname

                    if handname == 'Left Hand':
                        fig.select_set(True)
                        bpy.context.view_layer.objects.active = fig
                        bpy.context.active_object.modifiers.new("Boolean", 'BOOLEAN')
                        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["RLBool"]
                        fig.select_set(False)

                        obj = bpy.data.objects[fig.name]
                        dwive = obj.modifiers["Boolean"].driver_add("show_viewport")
                        driver = dwive.driver
                        
                        var = driver.variables.new()
                        
                        var.type = 'SINGLE_PROP'
                        var.name = "hide"

                        target = var.targets[0]

                        target.id_type = 'ARMATURE'

                        b = bpy.data.armatures[rig.name]

                        target.id = b

                        target.data_path = '["Lepin Hands"]'

                        driver.expression = "hide"

                        #2

                        obj = bpy.data.objects[fig.name]
                        dwive = obj.modifiers["Boolean"].driver_add("show_render")
                        driver = dwive.driver
                        
                        var = driver.variables.new()
                        
                        var.type = 'SINGLE_PROP'
                        var.name = "hide"

                        target = var.targets[0]

                        target.id_type = 'ARMATURE'

                        b = bpy.data.armatures[rig.name]

                        target.id = b

                        target.data_path = '["Lepin Hands"]'

                        driver.expression = "hide"
                        
                        parent(handname, False, '["LLegSmear"]', "Left Hand Empty")
                    else:
                        fig.select_set(True)
                        bpy.context.view_layer.objects.active = fig
                        bpy.context.active_object.modifiers.new("Boolean", 'BOOLEAN')
                        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["RHBool"]
                        
                        obj = bpy.data.objects[fig.name]
                        dwive = obj.modifiers["Boolean"].driver_add("show_viewport")
                        driver = dwive.driver
                        
                        var = driver.variables.new()
                        
                        var.type = 'SINGLE_PROP'
                        var.name = "hide"

                        target = var.targets[0]

                        target.id_type = 'ARMATURE'

                        b = bpy.data.armatures[rig.name]

                        target.id = b

                        target.data_path = '["Lepin Hands"]'

                        driver.expression = "hide"

                        #2

                        obj = bpy.data.objects[fig.name]
                        dwive = obj.modifiers["Boolean"].driver_add("show_render")
                        driver = dwive.driver
                        
                        var = driver.variables.new()
                        
                        var.type = 'SINGLE_PROP'
                        var.name = "hide"

                        target = var.targets[0]

                        target.id_type = 'ARMATURE'

                        b = bpy.data.armatures[rig.name]

                        target.id = b

                        target.data_path = '["Lepin Hands"]'

                        driver.expression = "hide"
                        
                        #fig.select_set(False)

                        parent(handname, False, '["LLegSmear"]', "Right Hand Empty")

                
        #Turn Rig into Child                    
        rig.select_set(True)
        if child == True:
            bpy.data.objects["Rig"].pose.bones["MasterBone"]["Leg Height"] = 2.0
            
            bpy.data.objects["Rig"].pose.bones["MasterBone"]["Prop Bones Transform"] = 2.0

        else:

            bpy.data.objects["Rig"].pose.bones["MasterBone"]["Leg Height"] = 0.0
        
        #hides Prop Bones    
        bpy.data.objects["Rig"].pose.bones["MasterBone"]["Prop Bone A Visibility"] = 0
        bpy.data.objects["Rig"].pose.bones["MasterBone"]["Prop Bone B Visibility"] = 0
        # Body pivot is enabled by default
        torso_rock = bpy.data.objects["Rig"].pose.bones.get("Torso Rock")
        if torso_rock:
            for c in torso_rock.constraints:
                if c.type == 'PIVOT':
                    c.mute = False
        
        #renames rigs
        r = " Rig"
        b = " Bone Shapes"
        bpy.data.armatures["Rig"].name = mname + r
        rig.name = mname + r
        collections["BoneShapes"].name = mname + b
        collections["The EpicFigRig"].name = mname + r

        objectsfsmear = bpy.data.objects
        
        #fix Lepin Hands
        bpy.context.view_layer.objects['RHBool'].hide_viewport = True
        bpy.context.view_layer.objects['RLBool'].hide_viewport = True
        
        objectsfsmear["LlegS"].name = "FinishedLlegS"
        objectsfsmear["RlegS"].name = "FinishedRlegS"
        objectsfsmear["LarmS"].name = "FinishedLarmS"
        objectsfsmear["RarmS"].name = "FinishedRarmS"
        objectsfsmear["RHBool"].name = "FinishedRHBool"
        objectsfsmear["RLBool"].name = "FinishedRLBool"

        #turns off copy menu if you didn't have it on
        if addon_utils.check("space_view3d_copy_attributes") == (False, True):
            addon_utils.disable("space_view3d_copy_attributes")
            addon_utils.check("space_view3d_copy_attributes")
            
        #create global varibles for iksnap
        global mainfkbone
        mainfkbone = "RightLeg"    
        global snapfkbone
        snapfkbone = "RightLegSnap"
        global mainikbone
        mainikbone = "RightFootIK"
        global snapikbone
        snapikbone = "RightFootIKSnap"
        global toggleikslider
        toggleikslider ="RightLegIK"
        global keyframeikslider
        keyframeikslider ='["RightLegIK"]'
        
        self.report({'INFO'}, "Never gonna give your rig up, never gonna let your bones down!")
        return {'FINISHED'}
    
    """def invoke(self, context, event):
        
        self.actname = bpy.context.active_object.users_collection
        return context.window_manager.invoke_props_dialog(self)"""

class PropRigA(bpy.types.Operator):
    """Rig Selected Object(s) to Prop A (Default Right Hand)"""
    bl_label = "  Prop A  "
    bl_idname = 'propa.rig'
    
    def execute(self, context):
        
        for obj in bpy.context.selected_objects:
        
            if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
                    
            if obj.type == 'MESH':
                    bpy.context.view_layer.objects.active = obj
        
        bpy.data.objects[selected_armature].pose.bones["MasterBone"]["Prop Bone A Visibility"] = 1
        ob= bpy.context.active_object
        arma = bpy.data.objects[selected_armature]

        bpy.ops.object.select_all(action='DESELECT')

        arma.select_set(True)
        bpy.context.view_layer.objects.active = arma
        
        bpy.data.objects[selected_armature].pose.bones["MasterBone"]["Prop Bone A Visibility"] = 1        
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.object.mode_set(mode='EDIT')


        parent_bone = 'AP Bone Transform'  # choose the bone name which you want to be the parent

        arma.data.edit_bones.active = arma.data.edit_bones[parent_bone]

        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')  # deselect all objects
        ob.select_set(True)
        arma.select_set(True)
        bpy.context.view_layer.objects.active = arma
        # the active object will be the parent of all selected object

        bpy.ops.object.parent_set(type='BONE', keep_transform=True)
        
        return {'FINISHED'}
    
class PropRigB(bpy.types.Operator):
    """Rig Selected Object(s) to Prop B (Default Left Hand)"""
    bl_label = "  Prop B  "
    bl_idname = 'propb.rig'
    
    def execute(self, context):
        
        for obj in bpy.context.selected_objects:
        
            if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
                    
            if obj.type == 'MESH':
                    bpy.context.view_layer.objects.active = obj
                
        bpy.data.objects[selected_armature].pose.bones["MasterBone"]["Prop Bone B Visibility"] = 1
        ob= bpy.context.active_object
        arma = bpy.data.objects[selected_armature]

        bpy.ops.object.select_all(action='DESELECT')

        arma.select_set(True)
        bpy.context.view_layer.objects.active = arma
        
        bpy.data.objects[selected_armature].pose.bones["MasterBone"]["Prop Bone B Visibility"] = 1        
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.object.mode_set(mode='EDIT')


        parent_bone = 'AP Bone B Transform'  # choose the bone name which you want to be the parent

        arma.data.edit_bones.active = arma.data.edit_bones[parent_bone]

        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')  # deselect all objects
        ob.select_set(True)
        arma.select_set(True)
        bpy.context.view_layer.objects.active = arma
        # the active object will be the parent of all selected object

        bpy.ops.object.parent_set(type='BONE', keep_transform=True)
        
        return {'FINISHED'}

#Proximity Rig
class ProxRig(bpy.types.Operator):
    """Use after Rigging with the main Method. and This feature is not 100% reliable with non-standard Minifgure bricks or the hip bricks"""
    bl_idname = "prox.rig"
    bl_label = "Addtional Objects"
    #bl_options = {'REGISTER', 'UNDO'}
    
    def bone_envelope(self, bone, armature):
        bone_head = armature.matrix_world @ bone.head_local
        bone_tail = armature.matrix_world @ bone.tail_local
        return bone_head, bone_tail

    def closest_bone(self, armature, obj, allowed_bones):
        """Find the closest bone to the object's location based on the bone's envelope."""
        closest_bone = None
        min_distance = float('inf')  # Initialize with a high value

        # Get the world-space position of the object
        obj_location = obj.matrix_world.translation

        # Loop through each bone in the armature
        for bone in armature.pose.bones:
            # Check if the bone is in the allowed list
            if bone.name not in allowed_bones:
                continue

            # Get the bone's envelope (head and tail positions)
            bone_head, bone_tail = self.bone_envelope(bone.bone, armature)

            # Calculate the distance from the object to the bone's head and tail
            distance_to_head = (obj_location - bone_head).length
            distance_to_tail = (obj_location - bone_tail).length

            # Get the minimum distance to this bone's envelope
            min_bone_distance = min(distance_to_head, distance_to_tail)

            # If the bone is closer than the current minimum, update
            if min_bone_distance < min_distance:
                min_distance = min_bone_distance
                closest_bone = bone

        return closest_bone

    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type != 'ARMATURE']

        # Check if there are selected objects
        if not selected_objects:
            self.report({'ERROR'}, "No valid objects selected.")
            return {'CANCELLED'}

        # Ensure the active object is an armature
        armature = context.active_object
        if armature and armature.type == 'ARMATURE':
            # Get the allowed bones (as per the predefined names)
            #allowed_bones = allowed_bones()
            allowed_bones = ["Right Hand", "Left Hand", "Right Arm", "Left Arm", "Torso", "Torso Rock", "Head", "Head Accessory","RightLegInvert", "LeftLegInvert"]

            for obj in selected_objects:
                #Skips object if already parented
                if obj.parent == armature:
                    self.report({'INFO'}, f"'{obj.name}' is already parented to '{armature.name}', skipping.")
                    continue  

                # Find the closest allowed bone to the object
                closest_bone = self.closest_bone(armature, obj, allowed_bones)

                if closest_bone:
                    # Store the object's current world matrix before parenting
                    obj_matrix_world = obj.matrix_world.copy()

                    # Set the object as the active object
                    context.view_layer.objects.active = obj

                    # Parent the object to the armature and the closest bone
                    obj.parent = armature
                    obj.parent_bone = closest_bone.name
                    obj.parent_type = 'BONE'

                    # Reapply the stored matrix to keep the object's world transform intact
                    obj.matrix_world = obj_matrix_world

                    self.report({'INFO'}, f"Parented '{obj.name}' to bone '{closest_bone.name}'")
                else:
                    self.report({'WARNING'}, f"No bones found nearby object '{obj.name}'.")
        else:
            self.report({'ERROR'}, "Active object is not the rig.")

        return {'FINISHED'}
    
#Master Bone   
class ResetMasterBone(bpy.types.Operator):
    """Reverts Masterbone to Default Values"""
    bl_label = "Reset Master Bone"
    bl_idname = 'rig.reset'
    
    def execute(self, context):
        bpy.context.object.data.name = bpy.context.object.name
        if context.mode == 'POSE':
            if len(context.selected_objects) == 1:
                for obj in bpy.context.selected_objects:
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name

            arm = bpy.data.objects[selected_armature]
            master_bone_snap = arm.pose.bones["Master Bone Snap"]
            master_bone = arm.data.bones["MasterBone"]
            cur_frame = bpy.context.scene.frame_current

            #insert locrot on pivot bone and master bone frame -1
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1) 
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            set_bone_select(arm, "MasterBone", True)
            set_bone_select(arm, "BodyControlBoneIK", True)
            set_bone_select(arm, "LeftFootIK", True)
            set_bone_select(arm, "RightFootIK", True)
            set_bone_select(arm, "Center of Mass", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #reset hip loc and height
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "MasterBone", True)
            hip_height = arm.pose.bones["BodyControlBoneIK"].location.z
            hip_rot = arm.pose.bones["BodyControlBoneIK"].rotation_quaternion.x 
            arm.pose.bones["BodyControlBoneIK"].location.z = 0
            arm.pose.bones["BodyControlBoneIK"].rotation_quaternion.x = 0
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #gets world matrix of the snap bone
            obj = master_bone_snap.id_data
            matrix_final = obj.matrix_world @ master_bone_snap.matrix

            #moves snap empty to snap bone
            obj_empty = bpy.data.objects["Master Bone Snap"]
            obj_empty.matrix_world = matrix_final

            #resets pivot bone locrot
            arm.pose.bones["Pivot"].rotation_euler.x = 0
            arm.pose.bones["Pivot"].location.x = 0
            arm.pose.bones["Pivot"].location.y = 0
            arm.pose.bones["Pivot"].location.z = 0
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #reset center of mass rotation
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Center of Mass", True)
            arm.pose.bones["Center of Mass"].rotation_euler.z = 0
            
            #reset IK Hip Bone 
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "BodyControlBoneIK", True)
            ik_distance = arm.pose.bones["BodyControlBoneIK"].location.y
            arm.pose.bones["BodyControlBoneIK"].location.y = 0

            #reset IK Legs   
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "LeftFootIK", True)
            set_bone_select(arm, "RightFootIK", True)
            bpy.ops.transform.translate(value=(0.0, ik_distance, 0.0), orient_type='LOCAL', orient_matrix=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1.0, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_target='CLOSEST', snap_point=(0.0, 0.0, 0.0), snap_align=False, snap_normal=(0.0, 0.0, 0.0), gpencil_strokes=False, cursor_transform=False, texture_space=False, remove_on_cancel=False, release_confirm=False, use_accurate=False)

            #moves master bone to snap empty
            snap_empty_xloc = bpy.data.objects["Master Bone Snap"].location.x
            snap_empty_yloc = bpy.data.objects["Master Bone Snap"].location.y
            snap_empty_zrot = bpy.data.objects["Master Bone Snap"].rotation_euler.z

            arm.pose.bones["MasterBone"].location.x = snap_empty_xloc
            arm.pose.bones["MasterBone"].location.z = snap_empty_yloc
            arm.pose.bones["MasterBone"].rotation_euler.y = -snap_empty_zrot

            #reset hip height and rot
            arm.pose.bones["BodyControlBoneIK"].location.z = hip_height
            arm.pose.bones["BodyControlBoneIK"].rotation_quaternion.x = hip_rot

            #insert locrot
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "BodyControlBoneIK", True)
            set_bone_select(arm, "LeftFootIK", True)
            set_bone_select(arm, "RightFootIK", True)
            set_bone_select(arm, "MasterBone", True)
            set_bone_select(arm, "Center of Mass", True)
            set_bone_select(arm, "Pivot", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #switch custom property
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            arm.pose.bones['MasterBone'].keyframe_insert(data_path='["Pivot Slide"]')
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
            arm.pose.bones["MasterBone"]["Pivot Slide"] = 0
            arm.pose.bones['MasterBone'].keyframe_insert(data_path='["Pivot Slide"]')
            
            #update the scene
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")

        return {'FINISHED'}

class SnapMasterBone(bpy.types.Operator):
    bl_label = "Snap Master Bone"
    bl_idname = 'snap.masterbone'
    
    def execute(self, context): 
        bpy.context.object.data.name = bpy.context.object.name 
        if context.mode == 'POSE':
            if len(context.selected_objects) == 1:
                for obj in bpy.context.selected_objects:
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name

            arm = bpy.data.objects[selected_armature]
            master_bone_snap = arm.pose.bones["Master Bone Snap"]
            cur_frame = bpy.context.scene.frame_current

            #insert locrot on flip bone and master bone frame -1
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1) 
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "MasterBone", True)
            set_bone_select(arm, "Center of Mass", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #reset hip loc and height
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "MasterBone", True)
            hip_height = arm.pose.bones["BodyControlBoneIK"].location.z
            hip_rot = arm.pose.bones["BodyControlBoneIK"].rotation_quaternion.x 
            arm.pose.bones["BodyControlBoneIK"].location.z = 0
            arm.pose.bones["BodyControlBoneIK"].rotation_quaternion.x = 0
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')

            #gets world matrix of the snap bone
            obj = master_bone_snap.id_data
            matrix_final = obj.matrix_world @ master_bone_snap.matrix

            #moves snap empty to snap bone
            obj_empty = bpy.data.objects["Master Bone Snap"]
            obj_empty.matrix_world = matrix_final
            
            #reset center of mass rotation
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Center of Mass", True)
            arm.pose.bones["Center of Mass"].rotation_euler.z = 0
            
            #moves master bone to snap empty
            snap_empty_xloc = bpy.data.objects["Master Bone Snap"].location.x
            snap_empty_yloc = bpy.data.objects["Master Bone Snap"].location.y
            snap_empty_zrot = bpy.data.objects["Master Bone Snap"].rotation_euler.z

            arm.pose.bones["MasterBone"].location.x = snap_empty_xloc
            arm.pose.bones["MasterBone"].location.z = snap_empty_yloc
            arm.pose.bones["MasterBone"].rotation_euler.y = -snap_empty_zrot
            
            #reset hip height and rot
            arm.pose.bones["BodyControlBoneIK"].location.z = hip_height
            arm.pose.bones["BodyControlBoneIK"].rotation_quaternion.x = hip_rot
            
            #insert locrot on flip bone and master bone frame current 
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "MasterBone", True)
            set_bone_select(arm, "Center of Mass", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #update scene
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")
        return {'FINISHED'}  

#Pivot
class SwitchPivottoLeft(bpy.types.Operator):
    """Changes the Pivot Bone to the Left Leg"""
    bl_label = "Left"
    bl_idname = 'pivot.left'
    
    def execute(self, context):
        if context.mode == 'POSE':
            if len(context.selected_objects) == 1:
                for obj in bpy.context.selected_objects:
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name
                        bpy.context.object.data.name = bpy.context.object.name

            arm = bpy.data.objects[selected_armature]
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            set_bone_select(arm, "LeftFootIK", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            arm.pose.bones['MasterBone'].keyframe_insert(data_path='["Pivot Slide"]')
            
            #turn on Armature Pivot Collection
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
            if "Pivot Contols" in bpy.data.armatures[selected_armature].collections_all:
                bpy.data.armatures[selected_armature].collections_all["Pivot Contols"].is_visible = True
            
            #reset IK Foot Loc
            arm.pose.bones["LeftFootIK"].location.x = 0
            arm.pose.bones["LeftFootIK"].location.y = 0
            arm.pose.bones["LeftFootIK"].location.z = 0

            #Move Pivot to Left Foot
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot lock L", True)
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
            
            #switch custom property
            arm.pose.bones["MasterBone"]["Pivot Slide"] = 1
            arm.pose.bones['MasterBone'].keyframe_insert(data_path='["Pivot Slide"]')
    
            #turn off Armature Pivot Collection
            if "Pivot Contols" in bpy.data.armatures[selected_armature].collections_all:
                bpy.data.armatures[selected_armature].collections_all["Pivot Contols"].is_visible = False
            
            #insert keyframes
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            set_bone_select(arm, "LeftFootIK", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #update scene
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")

        return {'FINISHED'}

class SwitchPivottoRight(bpy.types.Operator):
    """Changes the Pivot Bone to the Right Leg""" 
    bl_label = "Right"
    bl_idname = 'pivot.right'
    
    def execute(self, context):
        if context.mode == 'POSE':
            if len(context.selected_objects) == 1:
                for obj in bpy.context.selected_objects:
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name
                        bpy.context.object.data.name = bpy.context.object.name
                        
            arm = bpy.data.objects[selected_armature]
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            set_bone_select(arm, "RightFootIK", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            arm.pose.bones['MasterBone'].keyframe_insert(data_path='["Pivot Slide"]')
            
            #turn on Armature Pivot Collection
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1) 
            if "Pivot Contols" in bpy.data.armatures[selected_armature].collections_all:
                bpy.data.armatures[selected_armature].collections_all["Pivot Contols"].is_visible = True
            
            arm.pose.bones["RightFootIK"].location.x = 0
            arm.pose.bones["RightFootIK"].location.y = 0
            arm.pose.bones["RightFootIK"].location.z = 0

            #Move to Right Foot
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot lock R", True)
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
            
            #switch custom property
            arm.pose.bones["MasterBone"]["Pivot Slide"] = 0
            arm.pose.bones['MasterBone'].keyframe_insert(data_path='["Pivot Slide"]')
    
            #turn off Armature Pivot Collection
            if "Pivot Contols" in bpy.data.armatures[selected_armature].collections_all:
                bpy.data.armatures[selected_armature].collections_all["Pivot Contols"].is_visible = False
            
            #insert keyframes
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            set_bone_select(arm, "RightFootIK", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #update scene
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")

        return {'FINISHED'}

class ResetPivot(bpy.types.Operator):
    """Reverts Pivot Bone to Default Values""" 
    bl_label = "Reset Pivot"
    bl_idname = 'reset.pivot'
    
    def execute(self, context):
        if context.mode == 'POSE':
            if len(context.selected_objects) == 1:
                for obj in bpy.context.selected_objects:
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name
                        bpy.context.object.data.name = bpy.context.object.name
                        
            arm = bpy.data.objects[selected_armature]
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.ops.pose.select_all(action='DESELECT')
            set_bone_select(arm, "Pivot", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            arm.pose.bones['MasterBone'].keyframe_insert(data_path='["Pivot Slide"]')
            
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)            
            arm.pose.bones["Pivot"].location.x = 0
            arm.pose.bones["Pivot"].location.y = 0
            arm.pose.bones["Pivot"].location.z = 0
            arm.pose.bones["Pivot"].rotation_euler.x = 0
            arm.pose.bones["RightFootIK"].location.x = 0
            arm.pose.bones["RightFootIK"].location.y = 0
            arm.pose.bones["RightFootIK"].location.z = 0
            set_bone_select(arm, "RightFootIK", True)
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #switch custom property
            arm.pose.bones["MasterBone"]["Pivot Slide"] = 0
            arm.pose.bones['MasterBone'].keyframe_insert(data_path='["Pivot Slide"]')
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")
        return {'FINISHED'}
class PivotBodyEnable(bpy.types.Operator):
    """Enable Torso Pivot (body tilts on waist edge)"""
    bl_label = "Enable Body Pivot"
    bl_idname = 'pivot_body.enable'
    
    def execute(self, context):
        arm = context.active_object if (context.active_object and context.active_object.type == 'ARMATURE') else None
        if not arm:
            for obj in context.selected_objects:
                if obj.type == 'ARMATURE':
                    arm = obj
                    break
        if arm:
            torso_rock = arm.pose.bones.get("Torso Rock")
            if torso_rock:
                for c in torso_rock.constraints:
                    if c.type == 'PIVOT':
                        c.mute = False
                self.report({'INFO'}, "Body Pivot: Enabled (Edge Tilt)")
                return {'FINISHED'}
        self.report({'ERROR'}, "Select an Armature first")
        return {'FINISHED'}

class PivotBodyDisable(bpy.types.Operator):
    """Disable Torso Pivot (body rotates smoothly around center)"""
    bl_label = "Disable Body Pivot"
    bl_idname = 'pivot_body.disable'
    
    def execute(self, context):
        arm = context.active_object if (context.active_object and context.active_object.type == 'ARMATURE') else None
        if not arm:
            for obj in context.selected_objects:
                if obj.type == 'ARMATURE':
                    arm = obj
                    break
        if arm:
            torso_rock = arm.pose.bones.get("Torso Rock")
            if torso_rock:
                for c in torso_rock.constraints:
                    if c.type == 'PIVOT':
                        c.mute = True
                self.report({'INFO'}, "Body Pivot: Disabled (Smooth Center)")
                return {'FINISHED'}
        self.report({'ERROR'}, "Select an Armature first")
        return {'FINISHED'}

#Snap Bones  
class SnapRight(bpy.types.Operator):
    """Snap Selected Accessory to the Right Hand""" 
    bl_label = "Right Hand"
    bl_idname = 'snap_right.add'
    
    def execute(self, context):
        cur_frame = bpy.context.scene.frame_current
        if len(context.selected_objects) == 2:
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
                if obj.type == 'MESH':
                    global selected_object
                    selected_object = obj.name

            arm = bpy.data.objects[selected_armature]
            set_bone_select(arm, "Right Hand Snap Bone", False)
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
            
            selected_object_keyframe = bpy.data.objects[selected_object].keyframe_insert
            bpy.data.objects[selected_object].select_set(True)
            target_mesh = bpy.data.objects[selected_object]
            bpy.context.view_layer.objects.active = target_mesh
            selected_object_keyframe(data_path='location', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame=(cur_frame - 1))
            
            o = bpy.context.selected_objects[0]
            o.constraints.new('COPY_TRANSFORMS')
            copy_transform = bpy.data.objects[selected_object].constraints['Copy Transforms']
            copy_transform.target = arm
            copy_transform.subtarget = "Right Hand Snap Bone"
            
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame - 1)
            copy_transform.influence = 1
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame)
            
            selected_object_keyframe(data_path='location', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame=(cur_frame - 1))
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRot')
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1) 
        else:
            self.report({'ERROR'}, "Select both Armature and Object")
        return {'FINISHED'}
    
class SnapLeft(bpy.types.Operator):
    """Snap Selected Accessory to the Left Hand"""
    bl_label = "Left Hand"
    bl_idname = 'snap_left.add'
    
    def execute(self, context):
        cur_frame = bpy.context.scene.frame_current
        if len(context.selected_objects) == 2:
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
                if obj.type == 'MESH':
                    global selected_object
                    selected_object = obj.name

            arm = bpy.data.objects[selected_armature]
            set_bone_select(arm, "Left Hand Snap Bone", False)
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
            
            selected_object_keyframe = bpy.data.objects[selected_object].keyframe_insert
            bpy.data.objects[selected_object].select_set(True)
            target_mesh = bpy.data.objects[selected_object]
            bpy.context.view_layer.objects.active = target_mesh
            selected_object_keyframe(data_path='location', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame=(cur_frame - 1))
            
            o = bpy.context.selected_objects[0]
            o.constraints.new('COPY_TRANSFORMS')
            copy_transform = bpy.data.objects[selected_object].constraints['Copy Transforms']
            copy_transform.target = arm
            copy_transform.subtarget = "Left Hand Snap Bone"
            
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame - 1)
            copy_transform.influence = 1
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame)
            
            selected_object_keyframe(data_path='location', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame=(cur_frame - 1))
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRot')
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Select both Armature and Object")
        return {'FINISHED'}
    
class SnapHead(bpy.types.Operator):
    """Snap Selected Accessory to the Head"""
    bl_label = "Head"
    bl_idname = 'snap_head.add'
    
    def execute(self, context):
        cur_frame = bpy.context.scene.frame_current
        if len(context.selected_objects) == 2:
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
                if obj.type == 'MESH':
                    global selected_object
                    selected_object = obj.name

            arm = bpy.data.objects[selected_armature]
            set_bone_select(arm, "Head Accessory", False)
            for obj in bpy.context.selected_objects:
                obj.select_set(False)

            selected_object_keyframe = bpy.data.objects[selected_object].keyframe_insert
            bpy.data.objects[selected_object].select_set(True)
            target_mesh = bpy.data.objects[selected_object]
            bpy.context.view_layer.objects.active = target_mesh
            selected_object_keyframe(data_path='location', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame=(cur_frame - 1))
            
            o = bpy.context.selected_objects[0]
            o.constraints.new('COPY_TRANSFORMS')
            copy_transform = bpy.data.objects[selected_object].constraints['Copy Transforms']
            copy_transform.target = arm
            copy_transform.subtarget = "Head Accessory"
            
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame - 1)
            copy_transform.influence = 1
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame)
            
            selected_object_keyframe(data_path='location', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame=(cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame=(cur_frame - 1))
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRot')
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path="influence", frame=cur_frame)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Select both Armature and Object")
        return {'FINISHED'}

def iktofk():
    if addon_utils.check("space_view3d_copy_attributes") == (False, False):
        addon_utils.enable("space_view3d_copy_attributes")
        addon_utils.check("space_view3d_copy_attributes")
        
    arm = bpy.data.objects[selected_armature]
    arm.pose.bones["MasterBone"]["SnapVis"] = 1
    active_obj = bpy.context.view_layer.objects.active
    set_bone_select(active_obj, mainfkbone, True)
    set_bone_select(active_obj, snapfkbone, True)
    set_bone_select(active_obj, mainikbone, True)
    set_bone_select(active_obj, snapikbone, True)
            
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    bpy.ops.pose.select_all(action='DESELECT')
    
    set_bone_select(active_obj, snapfkbone, True)
    bpy.context.object.data.bones.active = arm.pose.bones[mainfkbone].bone
    bpy.ops.pose.copy_pose_vis_rot()
    bpy.ops.pose.copy_pose_vis_loc()
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")

    arm.pose.bones["MasterBone"][toggleikslider] = 0
    arm.pose.bones['MasterBone'].keyframe_insert(data_path=keyframeikslider)
    bpy.ops.pose.select_all(action='DESELECT')

    set_bone_select(active_obj, mainfkbone, True)
    bpy.context.object.data.bones.active = arm.pose.bones[snapfkbone].bone
    bpy.ops.pose.copy_pose_vis_loc()
    bpy.ops.pose.copy_pose_vis_rot()
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    bpy.ops.pose.select_all(action='DESELECT')

    if addon_utils.check("space_view3d_copy_attributes") == (False, True):
        addon_utils.disable("space_view3d_copy_attributes")
        addon_utils.check("space_view3d_copy_attributes")

    arm.pose.bones["MasterBone"]["SnapVis"] = 0
    bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
    bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
    bpy.ops.pose.select_all(action='DESELECT')         

def fktoik():
    if addon_utils.check("space_view3d_copy_attributes") == (False, False):
        addon_utils.enable("space_view3d_copy_attributes")
        addon_utils.check("space_view3d_copy_attributes")
        
    arm = bpy.data.objects[selected_armature]
    arm.pose.bones["MasterBone"]["SnapVis"] = 1
    active_obj = bpy.context.view_layer.objects.active
    set_bone_select(active_obj, mainfkbone, True)
    set_bone_select(active_obj, snapfkbone, True)
    set_bone_select(active_obj, mainikbone, True)
    set_bone_select(active_obj, snapikbone, True)
            
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    bpy.ops.pose.select_all(action='DESELECT')
    
    set_bone_select(active_obj, snapfkbone, True)
    bpy.context.object.data.bones.active = arm.pose.bones[mainfkbone].bone
    bpy.ops.pose.copy_pose_vis_rot()
    bpy.ops.pose.copy_pose_vis_loc()
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")

    arm.pose.bones["MasterBone"][toggleikslider] = 1
    arm.pose.bones['MasterBone'].keyframe_insert(data_path=keyframeikslider)
    bpy.ops.pose.select_all(action='DESELECT')

    set_bone_select(active_obj, mainikbone, True)
    bpy.context.object.data.bones.active = arm.pose.bones[snapikbone].bone
    bpy.ops.pose.copy_pose_vis_loc()
    bpy.ops.pose.copy_pose_vis_rot()
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    bpy.ops.pose.select_all(action='DESELECT')

    if addon_utils.check("space_view3d_copy_attributes") == (False, True):
        addon_utils.disable("space_view3d_copy_attributes")
        addon_utils.check("space_view3d_copy_attributes")

    arm.pose.bones["MasterBone"]["SnapVis"] = 0
    bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
    bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
    bpy.ops.pose.select_all(action='DESELECT')

class iktofkRleg(bpy.types.Operator):
    """Keyframes the Current Values and changes the Right Leg to FK"""
    bl_label = "Snap IK to FK"
    bl_idname = 'ik_to.fk_rleg'

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
            global mainfkbone, snapfkbone, mainikbone, snapikbone, toggleikslider, keyframeikslider
            mainfkbone = "RightLeg"    
            snapfkbone = "RightLegSnap"
            mainikbone = "RightFootIK"
            snapikbone = "RightFootIKSnap"
            toggleikslider = "RightLegIK"
            keyframeikslider = '["RightLegIK"]'
    
            iktofk()
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        return {'FINISHED'}

class iktofkLleg(bpy.types.Operator):
    """Keyframes the Current Values and changes the Left Leg to FK"""
    bl_label = "Snap IK to FK"
    bl_idname = 'ik_to.fk_lleg'

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
            global mainfkbone, snapfkbone, mainikbone, snapikbone, toggleikslider, keyframeikslider
            mainfkbone = "LeftLeg"    
            snapfkbone = "LeftLegSnap"
            mainikbone = "LeftFootIK"
            snapikbone = "LeftFootIKSnap"
            toggleikslider = "LeftLegIK"
            keyframeikslider = '["LeftLegIK"]'
    
            iktofk()
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        return {'FINISHED'}

class iktofkLarm(bpy.types.Operator):
    """Keyframes the Current Values and changes the Left Arm to FK"""
    bl_label = "Snap IK to FK"
    bl_idname = 'ik_to.fk_larm'

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
            global mainfkbone, snapfkbone, mainikbone, snapikbone, toggleikslider, keyframeikslider
            mainfkbone = "Left Arm Socket Control"    
            snapfkbone = "Left Arm Snap"
            mainikbone = "Left Arm IK"
            snapikbone = "Left Arm IK Snap"
            toggleikslider = "LeftArmIK"
            keyframeikslider = '["LeftArmIK"]'
    
            iktofk()
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        return {'FINISHED'}

class iktofkRarm(bpy.types.Operator):
    """Keyframes the Current Values and changes the Right Arm to FK"""
    bl_label = "Snap IK to FK"
    bl_idname = 'ik_to.fk_rarm'

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
            global mainfkbone, snapfkbone, mainikbone, snapikbone, toggleikslider, keyframeikslider
            mainfkbone = "Right Arm Socket Control"    
            snapfkbone = "Right Arm Snap"
            mainikbone = "Right Arm IK"
            snapikbone = "Right Arm IK Snap"
            toggleikslider = "RightArmIK"
            keyframeikslider = '["RightArmIK"]'
    
            iktofk()
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        return {'FINISHED'}     

class fktoikRleg(bpy.types.Operator):
    """Keyframes the Current Values and changes the Right Leg to IK"""
    bl_label = "Snap FK to IK"
    bl_idname = 'fk_to.ik_rleg'

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
            global mainfkbone, snapfkbone, mainikbone, snapikbone, toggleikslider, keyframeikslider
            mainfkbone = "RightLeg"    
            snapfkbone = "RightLegSnap"
            mainikbone = "RightFootIK"
            snapikbone = "RightFootIKSnap"
            toggleikslider = "RightLegIK"
            keyframeikslider = '["RightLegIK"]'
    
            fktoik()
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        return {'FINISHED'}

class fktoikLleg(bpy.types.Operator):
    """Keyframes the Current Values and changes the Left Leg to IK"""
    bl_label = "Snap FK to IK"
    bl_idname = 'fk_to.ik_lleg'

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
            global mainfkbone, snapfkbone, mainikbone, snapikbone, toggleikslider, keyframeikslider
            mainfkbone = "LeftLeg"    
            snapfkbone = "LeftLegSnap"
            mainikbone = "LeftFootIK"
            snapikbone = "LeftFootIKSnap"
            toggleikslider = "LeftLegIK"
            keyframeikslider = '["LeftLegIK"]'
    
            fktoik()
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        return {'FINISHED'}

class fktoikLarm(bpy.types.Operator):
    """Keyframes the Current Values and changes the Left Arm to IK"""
    bl_label = "Snap FK to IK"
    bl_idname = 'fk_to.ik_larm'

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
            global mainfkbone, snapfkbone, mainikbone, snapikbone, toggleikslider, keyframeikslider
            mainfkbone = "Left Arm Socket Control"    
            snapfkbone = "Left Arm Snap"
            mainikbone = "Left Arm IK"
            snapikbone = "Left Arm IK Snap"
            toggleikslider = "LeftArmIK"
            keyframeikslider = '["LeftArmIK"]'
    
            fktoik()
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        return {'FINISHED'}

class fktoikRarm(bpy.types.Operator):
    """Keyframes the Current Values and changes the Right Arm to IK"""
    bl_label = "Snap FK to IK"
    bl_idname = 'fk_to.ik_rarm'

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
            global mainfkbone, snapfkbone, mainikbone, snapikbone, toggleikslider, keyframeikslider
            mainfkbone = "Right Arm Socket Control"    
            snapfkbone = "Right Arm Snap"
            mainikbone = "Right Arm IK"
            snapikbone = "Right Arm IK Snap"
            toggleikslider = "RightArmIK"
            keyframeikslider = '["RightArmIK"]'
    
            fktoik()
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        return {'FINISHED'}

class MainTab(bpy.types.Operator):
    """Main Rig Settings"""
    bl_label = "Main"
    bl_idname = 'main.tab'

    def execute(self, context):
        context.scene.EpicRigTabs = 0
        return {'FINISHED'}

class AdvancedTab(bpy.types.Operator):
    """Advanced Rig Settings - More to Come!"""
    bl_label = "Advanced"
    bl_idname = 'advanced.tab'

    def execute(self, context):
        context.scene.EpicRigTabs = 1
        return {'FINISHED'}

#REGISTRATION

def register():
    
    bpy.utils.register_class(EpicFigRigPanel)
    bpy.utils.register_class(EpicButtons)
    bpy.utils.register_class(SmearSlider)
    bpy.utils.register_class(BoneAdjust)
    bpy.utils.register_class(BoneVis)
    bpy.utils.register_class(BoneShapes)
    bpy.utils.register_class(ResetMasterBone)
    bpy.utils.register_class(SwitchPivottoLeft)
    bpy.utils.register_class(SwitchPivottoRight)
    bpy.utils.register_class(ResetPivot)
    bpy.utils.register_class(PivotBodyEnable)
    bpy.utils.register_class(PivotBodyDisable)
    bpy.utils.register_class(SnapMasterBone)
    bpy.utils.register_class(SnapRight)
    bpy.utils.register_class(SnapLeft)
    bpy.utils.register_class(SnapHead)
    bpy.utils.register_class(AutoRig)
    bpy.utils.register_class(PropRigA)
    bpy.utils.register_class(PropRigB)
    bpy.utils.register_class(iktofkRleg)
    bpy.utils.register_class(iktofkLleg)
    bpy.utils.register_class(iktofkRarm)
    bpy.utils.register_class(iktofkLarm)
    bpy.utils.register_class(fktoikRarm)
    bpy.utils.register_class(fktoikLarm)
    bpy.utils.register_class(fktoikRleg)
    bpy.utils.register_class(fktoikLleg)
    bpy.utils.register_class(ArmMenu)
    bpy.utils.register_class(LegMenu)
    bpy.utils.register_class(MainTab)
    bpy.utils.register_class(AdvancedTab)
    bpy.utils.register_class(Props)
    bpy.utils.register_class(ProxRig)
    bpy.utils.register_class(LeftHandMenu)
    bpy.utils.register_class(RightHandMenu)
    bpy.utils.register_class(LeftLegMenu)
    bpy.utils.register_class(RightLegMenu)
    
    bpy.types.Scene.normalize_mini = bpy.props.BoolProperty(name="Normalize Minifigure", description="Normalize object transforms when enabled", default=False)
    bpy.types.Scene.EpicRigTabs = IntProperty(name="Epic Rig Tabs", default=0, min=0, max=3)

def unregister():

    bpy.utils.unregister_class(EpicFigRigPanel)
    bpy.utils.unregister_class(EpicButtons)
    bpy.utils.unregister_class(SmearSlider)
    bpy.utils.unregister_class(BoneAdjust)
    bpy.utils.unregister_class(BoneVis)
    bpy.utils.unregister_class(BoneShapes)
    bpy.utils.unregister_class(ResetMasterBone)
    bpy.utils.unregister_class(SwitchPivottoLeft)
    bpy.utils.unregister_class(SwitchPivottoRight)
    bpy.utils.unregister_class(ResetPivot)
    bpy.utils.unregister_class(PivotBodyEnable)
    bpy.utils.unregister_class(PivotBodyDisable)
    bpy.utils.unregister_class(SnapMasterBone)
    bpy.utils.unregister_class(SnapRight)
    bpy.utils.unregister_class(SnapLeft)
    bpy.utils.unregister_class(SnapHead)
    bpy.utils.unregister_class(AutoRig)
    bpy.utils.unregister_class(PropRigA)
    bpy.utils.unregister_class(PropRigB)
    bpy.utils.unregister_class(iktofkRleg)
    bpy.utils.unregister_class(iktofkLleg)
    bpy.utils.unregister_class(iktofkRarm)
    bpy.utils.unregister_class(iktofkLarm)
    bpy.utils.unregister_class(fktoikRarm)
    bpy.utils.unregister_class(fktoikLarm)
    bpy.utils.unregister_class(fktoikRleg)
    bpy.utils.unregister_class(fktoikLleg)
    bpy.utils.unregister_class(ArmMenu)
    bpy.utils.unregister_class(LegMenu)
    bpy.utils.unregister_class(MainTab)
    bpy.utils.unregister_class(AdvancedTab)
    bpy.utils.register_class(Props)
    bpy.utils.unregister_class(LeftHandMenu)
    bpy.utils.unregister_class(RightHandMenu)
    bpy.utils.unregister_class(LeftLegMenu)
    bpy.utils.unregister_class(RightLegMenu)
    bpy.utils.unregister_class(ProxRig)
    
    del bpy.types.Scene.EpicRigTabs
    del bpy.types.Scene.normalize_mini

if __name__ == "__main__":
    register()
