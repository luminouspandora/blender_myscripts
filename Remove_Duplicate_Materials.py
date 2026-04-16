bl_info = {
    "name": "Smart Material Duplicate Cleaner",
    "author": "Millenne Noel",
    "version": (1, 2),
    "blender": (4, 0, 0),
    "location": "Shader Editor > Sidebar > Material Cleaner",
    "description": "Replaces and removes duplicate materials ending with .001, .002, etc.",
    "category": "Material",
}

import bpy
import re

class MATERIAL_OT_RemoveAndReplaceDuplicates(bpy.types.Operator):
    """Replace and remove materials ending with .001, .002, etc."""
    bl_idname = "material.remove_and_replace_duplicates"
    bl_label = "Replace & Remove Duplicates"
    bl_options = {'REGISTER', 'UNDO'}

    force_delete: bpy.props.BoolProperty(
        name="Force Delete",
        description="Delete duplicates even if they're assigned to objects (after replacement if possible)",
        default=True,
    )

    def execute(self, context):
        pattern = re.compile(r"\.(\d{3})$")
        replaced = 0
        removed = 0

        for mat in list(bpy.data.materials):
            match = pattern.search(mat.name)
            if match:
                base_name = pattern.sub("", mat.name)

                # Check if base material exists
                base_mat = bpy.data.materials.get(base_name)
                if base_mat:
                    # Replace all object slots using this duplicate
                    for obj in bpy.data.objects:
                        if not obj.data or not hasattr(obj.data, "materials"):
                            continue
                        for i, slot in enumerate(obj.data.materials):
                            if slot == mat:
                                obj.data.materials[i] = base_mat
                                replaced += 1

                # Delete duplicate if unused or forced
                if self.force_delete or not mat.users:
                    bpy.data.materials.remove(mat)
                    removed += 1

        self.report({'INFO'}, f"Replaced {replaced} slots, removed {removed} duplicates.")
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
        layout.label(text="Duplicate Material Fixer")
        layout.operator("material.remove_and_replace_duplicates", icon='TRASH')

def register():
    bpy.utils.register_class(MATERIAL_OT_RemoveAndReplaceDuplicates)
    bpy.utils.register_class(MATERIAL_PT_RemoveDuplicatePanel)

def unregister():
    bpy.utils.unregister_class(MATERIAL_OT_RemoveAndReplaceDuplicates)
    bpy.utils.unregister_class(MATERIAL_PT_RemoveDuplicatePanel)

if __name__ == "__main__":
    register()
