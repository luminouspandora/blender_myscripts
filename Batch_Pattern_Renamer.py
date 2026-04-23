bl_info = {
    "name": "Batch Pattern Renamer",
    "author": "Millenne Noel",
    "version": (1, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Custom Tools",
    "description": "Replace parts of object names using regex patterns",
    "category": "Object",
}

import bpy
import re


class OBJECT_PT_PatternRenamer(bpy.types.Panel):
    bl_label = "Batch Pattern Renamer"
    bl_idname = "OBJECT_PT_pattern_renamer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CustomTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "rename_prefix")
        layout.prop(scene, "rename_regex")

        layout.operator("object.pattern_rename", text="Apply Rename")


class OBJECT_OT_PatternRename(bpy.types.Operator):
    bl_label = "Pattern Rename"
    bl_idname = "object.pattern_rename"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefix = context.scene.rename_prefix
        pattern = context.scene.rename_regex

        for obj in context.selected_objects:
            original_name = obj.name

            try:
                new_name = re.sub(pattern, prefix, original_name)
            except re.error:
                self.report({'ERROR'}, "Invalid regex pattern")
                return {'CANCELLED'}

            obj.name = new_name

            if obj.type == 'MESH' and obj.data:
                obj.data.name = new_name

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_PT_PatternRenamer)
    bpy.utils.register_class(OBJECT_OT_PatternRename)

    bpy.types.Scene.rename_prefix = bpy.props.StringProperty(
        name="Replace With",
        default="MyPrefab"
    )

    bpy.types.Scene.rename_regex = bpy.props.StringProperty(
        name="Find (Regex)",
        default="Cube"
    )


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_PatternRenamer)
    bpy.utils.unregister_class(OBJECT_OT_PatternRename)

    del bpy.types.Scene.rename_prefix
    del bpy.types.Scene.rename_regex


if __name__ == "__main__":
    register()