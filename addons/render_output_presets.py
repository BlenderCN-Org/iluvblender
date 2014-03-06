# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "Render Output Presets",
    "author": "Satish Goda (iluvblender on BA, satishgoda@gmail.com)",
    "version": (0, 1),
    "blender": (2, 7, 0),
    "location": "Properties Editor : Render Context : Output Panel",
    "description": "Save preset consisting of properties from RenderSettings, ImageFormatSettings and FFmpegSettings",
    "warning": "",
    "category": "Render"
}

import bpy

from bl_operators import presets


class RENDER_MT_output(bpy.types.Menu):
    bl_label = "Output Presets"
    preset_subdir = "render/output"
    preset_operator = "script.execute_preset"
    draw = bpy.types.Menu.draw_preset


class AddPresetOutput(presets.AddPresetBase, bpy.types.Operator):
    """Add or remove a Output Preset"""
    bl_idname = "render.output_preset_add"
    bl_label = "Add Render Output Preset"
    preset_menu = "RENDER_MT_output"

    preset_defines = [
        "scene = bpy.context.scene",
        "render = scene.render",
        "image_settings = render.image_settings",
        "ffmpeg = render.ffmpeg",
    ]

    preset_values = [
        "render.filepath",
        "image_settings.file_format",
        "image_settings.color_mode",
        "image_settings.color_depth",
        "image_settings.compression",
        "ffmpeg.format",
        "ffmpeg.codec",
        "ffmpeg.use_lossless_output",
    ]

    preset_subdir = "output"

    def add(self, context, filepath):
        print("I has total control now")
        print(filepath)

    def post_cb(self, context):
        print("post_cb")
        render = context.scene.render
        preset_filepath = render.filepath
        if preset_filepath.startswith('{'):
            blend_filepath = context.blend_data.filepath
            if blend_filepath:
                filename = bpy.path.display_name_from_filepath(blend_filepath)
                render.filepath = '//' + preset_filepath.format(filename=filename)
            else:
                render.filepath = '/tmp/' + preset_filepath.format(filename='untitled')
        else:
            print("Unsupported markup")



def RENDER_PT_output_draw_presets(self, context):
    layout = self.layout
    
    row = layout.row(align=True)
    
    row.menu("RENDER_MT_output", text=bpy.types.RENDER_MT_output.bl_label)
    row.operator("render.output_preset_add", text="", icon='ZOOMIN')
    opprops = row.operator("render.output_preset_add", text="", icon='ZOOMOUT')
    opprops.remove_active = True


def register():
    bpy.utils.register_class(AddPresetOutput)
    bpy.utils.register_class(RENDER_MT_output)
    bpy.types.RENDER_PT_output.prepend(RENDER_PT_output_draw_presets)


def unregister():
    bpy.types.RENDER_PT_output.remove(RENDER_PT_output_draw_presets)
    bpy.utils.unregister_class(AddPresetOutput)
    bpy.utils.unregister_class(RENDER_MT_output)


if __name__ == '__main__':
    register()
