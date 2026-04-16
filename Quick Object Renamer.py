"""
    11/010/2025 MAN
    This is a blender script that allows you to select multiple
    objects in the View Layer and set a custom prefix title with regex numbering
"""



bl_info = {
    "name": "Quick Object Renamer",
    "author": "Millenne Noel",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Renamer",
    "description": "Batch rename selected objects with custom prefix and numbering",
    "category": "Object",
}

import bpy
import re

class OBJECT_PT_QuickRenamer(bpy.types.Panel):
    bl_label = "Quick Renamer"
    bl_idname = "OBJECT_PT_quick_renamer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Renamer"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "rename_prefix")
        layout.prop(context.scene, "rename_regex")
        layout.operator("object.quick_rename", text="Rename Selected")


class OBJECT_OT_QuickRename(bpy.types.Operator):
    bl_label = "Quick Rename"
    bl_idname = "object.quick_rename"

    def execute(self, context):
        prefix = context.scene.rename_prefix
        regex = context.scene.rename_regex
        
        for obj in context.selected_objects:
            # Split object name into base + optional .001
            match = re.match(r"(.*?)(\.\d+)?$", obj.name)
            if match:
                base = match.group(1)  # everything before .001
                suffix = ''             # keep suffix like _FOUNDATION, _ROOF
                
                 # Detect last underscore for suffix
                if '_' in base[len(regex):]:
                    parts = base.split('_', len(regex))
                    suffix = '_' + '_'.join(parts[1:])
                # Rename the object
                new_name = re.sub(regex, prefix, base) + suffix
                obj.name = new_name
                # Rename the mesh as well (if it has one)
                if obj.type == 'MESH' and obj.data:
                    obj.data.name = new_name
                
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_PT_QuickRenamer)
    bpy.utils.register_class(OBJECT_OT_QuickRename)
    bpy.types.Scene.rename_prefix = bpy.props.StringProperty(name="Prefix", default="MyPrefab")
    bpy.types.Scene.rename_regex = bpy.props.StringProperty(name="Regex", default="(\.\d+)?")


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_QuickRenamer)
    bpy.utils.unregister_class(OBJECT_OT_QuickRename)
    del bpy.types.Scene.rename_prefix
    del bpy.types.Scene.rename_regex


if __name__ == "__main__":
    register()
