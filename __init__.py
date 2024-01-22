'''
    Copyright (C) 2024  Andrei Suvorau

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Purge Empties",
    "author": "Andrei Suvorau",
    "version": (1, 0, 1),
    "blender": (3, 00, 0),
    "location": "3D View > UI (Right Panel) > Tools",
    "description": ("Purge Empties"),
    "warning": "",
    "wiki_url": "https://github.com/suVrik/PurgeEmpties/wiki",
    "tracker_url": "https://github.com/suVrik/PurgeEmpties/issues" ,
    "category": "Object"
}

import bpy
import mathutils


class PurgeEmpties_OT_purge(bpy.types.Operator):
    bl_label = 'Purge Empties'
    bl_idname = 'purgeempties.purge'
    
    def execute(self, context):
        bpy.ops.ed.undo_push(message = 'Purge Empties')
        
        empties = [obj for obj in bpy.data.objects if obj.type == 'EMPTY']

        for obj in empties:
          if obj.instance_collection is None:
            for child in obj.children:
              child.matrix_local = obj.matrix_local @ child.matrix_local
              
              child.parent = obj.parent

            bpy.data.objects.remove(obj, do_unlink = True)

        self.report({'INFO'}, 'Empties were purged.')

        return {'FINISHED'}


class PurgeEmpties_PT_panel(bpy.types.Panel):
    bl_label = 'Purge Empties'
    bl_idname = 'PurgeEmpties_PT_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        self.layout.operator('purgeempties.purge', icon = 'EMPTY_AXIS')


classes = [PurgeEmpties_PT_panel, PurgeEmpties_OT_purge]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
