bl_info = {
    "name": "Remove Duplicate Materials",
    "author": "Millenne Noel",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Shader Editor > Sidebar > Material Cleaner",
    "description": "Deletes materials ending with .001, .002, etc.",
    "category": "Material",
}

import bpy
import re

class MATERIAL_OT_RemoveDuplicate(bpy.types.Operator):
    """Remove materials ending with .001, .002, etc."""
    bl_idname = "material.remove_duplicate"
    bl_label = "Remove Duplicate Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pattern = re.compile(r"\.\d{3}$")
        removed = 0

        for mat in list(bpy.data.materials):
            if pattern.search(mat.name):
                bpy.data.materials.remove(mat)
                removed += 1

        self.report({'INFO'}, f"Removed {removed} duplicate materials.")
        return {'FINISHED'}

class MATERIAL_PT_RemoveDuplicatePanel(bpy.types.Panel):
    bl_label = "Material Cleaner"
    bl_idname = "MATERIAL_PT_remove_duplicate_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Cleaner"

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout
        layout.operator("material.remove_duplicate", icon='TRASH')

def register():
    bpy.utils.register_class(MATERIAL_OT_RemoveDuplicate)
    bpy.utils.register_class(MATERIAL_PT_RemoveDuplicatePanel)

def unregister():
    bpy.utils.unregister_class(MATERIAL_OT_RemoveDuplicate)
    bpy.utils.unregister_class(MATERIAL_PT_RemoveDuplicatePanel)

if __name__ == "__main__":
    register()
