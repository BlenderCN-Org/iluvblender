# -*- coding: utf-8 -*-
bl_info = {
    "name": "Suite of Tools to abet RBD Workflow",
    "author": "Satish Goda (iluvblender on BA, satishgoda@gmail.com)",
    "version": (0, 1),
    "blender": (2, 7, 0),
    "location": "Operator Search Menu (Tools start with RBD)",
    "description": "Suite of Tools to abet RBD Workflow",
    "warning": "",
    "category": "System"}   

"""Suite of Tools to abet RBD Workflow"""

import bpy
from bpy.props import IntProperty

def _update_attr(self, context, name):
    scene = context.scene
    point_cache = scene.rigidbody_world.point_cache
    value = getattr(self, name)
    for bobject in (scene, point_cache):
        setattr(bobject, name, value)
    bpy.ops.time.view_all()

def _update_frame_start(self, context):
    _update_attr(self, context, 'frame_start')

def _update_frame_end(self, context):
    _update_attr(self, context, 'frame_end')

class RBDChangeFrangeOperator(bpy.types.Operator):
    """Modify the frame range for the RBD simulation"""
    bl_idname = "object.rbd_change_frange"
    bl_label = "RBD Change Frange"

    frame_start = IntProperty(name="Start Frame", update=_update_frame_start,
                              default=1,
                              min=1,
                              soft_min=1,
                              step=1
                              )
    frame_end = IntProperty(name="End Frame", update=_update_frame_end,
                              default=1,
                              min=1,
                              soft_min=1,
                              step=1
                              )

    @classmethod
    def poll(cls, context):
        rbdworld = context.scene.rigidbody_world
        predicates = (context.area.type == 'TIMELINE',
                      rbdworld,
                      not rbdworld.point_cache.is_baking,
                      not rbdworld.point_cache.is_baked)
        return all(predicates)

    def invoke(self, context, event):
        wm = context.window_manager
        scene = context.scene
        self.frame_start = scene.frame_start
        self.frame_end = scene.frame_end
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        return {'FINISHED'}

class RBDView3DPoll():
    @classmethod
    def poll(cls, context):
        predicates = (context.area.type == 'VIEW_3D',)
        return all(predicates)

class RBDSelectMacro(bpy.types.Macro, RBDView3DPoll):
    """TODO"""
    bl_idname = "object.rbd_select"
    bl_label = "RBD Select"
    bl_options = {'REGISTER', 'UNDO'}


class RBDSelectAndHideMacro(bpy.types.Macro, RBDView3DPoll):
    """TODO"""
    bl_idname = "object.rbd_select_hide"
    bl_label = "RBD Select and Hide"
    bl_options = {'REGISTER', 'UNDO'}

class View3DQuadViewCustom(bpy.types.Operator):
    """Toggle the quad view and also set lock and sync properties"""
    bl_idname = "view3d.quad_view"
    bl_label = "V3D Quad View"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        predicates = (context.area.spaces.active.type == 'VIEW_3D',)
        return all(predicates)

    def execute(self, context):
        space_data = context.area.spaces.active
        quad_view = space_data.region_quadview
        bpy.ops.screen.region_quadview()
        if quad_view is None:
            for attr in ('lock_rotation', 'show_sync_view'):
                setattr(space_data.region_quadview, attr, True)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(RBDChangeFrangeOperator)
    bpy.utils.register_class(View3DQuadViewCustom)
    
    bpy.utils.register_class(RBDSelectMacro)
    op = RBDSelectMacro.define("OBJECT_OT_select_linked")
    op.properties.type = 'OBDATA'

    bpy.utils.register_class(RBDSelectAndHideMacro)
    op = RBDSelectAndHideMacro.define("OBJECT_OT_select_linked")
    op.properties.type = 'OBDATA'
    op = RBDSelectAndHideMacro.define("OBJECT_OT_hide_view_set")
    op.properties.unselected = False


def unregister():
    bpy.utils.unregister_class(RBDChangeFrangeOperator)
    bpy.utils.unregister_class(View3DQuadViewCustom)
    bpy.utils.unregister_class(RBDSelectAndHideMacro)
    bpy.utils.unregister_class(RBDSelectMacro)

if __name__ == '__main__':
    register()
