bl_info = {
    "name": "Zen Mode for working peacefully",
    "author": "Satish Goda (iluvblender on BA, satishgoda@gmail.com)",
    "version": (0, 1),
    "blender": (2, 7, 0),
    "location": "Operator Search Menu (type 'Zen')",
    "description": "(Un)Clear the area headers for the current screen",
    "warning": "",
    "category": "System"
}

"""(Un)Clear the area headers for the current screen"""


import bpy

def screen_areas_zen(context, enable=True):
    for area in context.screen.areas:
        if enable:
            area.show_menus = False
            area.header_text_set('')
        else:
            area.show_menus = True
            area.header_text_set()
        area.tag_redraw()

def main(context, enable):
    screen_areas_zen(context, enable)


class ScreenModeZenOperator(bpy.types.Operator):
    """Zennify the Screen areas display"""
    bl_idname = "screen.mode_zen"
    bl_label = "Screen Mode Zen"
    bl_options = {'REGISTER', 'UNDO'}

    enable = bpy.props.BoolProperty(name='Enable', description="Enable/Disable Zen Mode", default=False)    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def execute(self, context):
        main(context, self.enable)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ScreenModeZenOperator)


def unregister():
    bpy.utils.unregister_class(ScreenModeZenOperator)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.screen.mode_zen(enable=False)
    #bpy.ops.screen.mode_zen('INVOKE_DEFAULT')
