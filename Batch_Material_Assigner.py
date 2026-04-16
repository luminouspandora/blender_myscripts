"""
Batch Material Assigner v1.0
Author: Millenne Noel
Date: 2025-10-15

Allows you to create a list of materials and assign all of them at once
to all selected objects. Appears in the Sidebar under the “Materials” tab.
"""

bl_info = {
    "name": "Batch Material Assigner",
    "author": "Millenne Noel",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Materials",
    "description": "Assign multiple chosen materials to selected objects",
    "category": "Material",
}

import bpy


# ------------------------------------------------------------------------
# Data structure for a single material entry
# ------------------------------------------------------------------------
class MaterialListItem(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(
        name="Material",
        type=bpy.types.Material,
    )


# ------------------------------------------------------------------------
# Operators to manage the list
# ------------------------------------------------------------------------
class MATERIAL_OT_AddToList(bpy.types.Operator):
    bl_idname = "material.add_to_list"
    bl_label = "Add Material to List"

    def execute(self, context):
        context.scene.material_list.add()
        return {'FINISHED'}


class MATERIAL_OT_RemoveFromList(bpy.types.Operator):
    bl_idname = "material.remove_from_list"
    bl_label = "Remove Material from List"

    def execute(self, context):
        idx = context.scene.material_list_index
        if context.scene.material_list and idx < len(context.scene.material_list):
            context.scene.material_list.remove(idx)
            context.scene.material_list_index = max(0, idx - 1)
        return {'FINISHED'}


# ------------------------------------------------------------------------
# Operator to apply materials
# ------------------------------------------------------------------------
class MATERIAL_OT_ApplyList(bpy.types.Operator):
    """Assign all materials in the list to selected objects"""
    bl_idname = "material.apply_list"
    bl_label = "Apply to Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        materials = [item.material for item in context.scene.material_list if item.material]
        if not materials:
            self.report({'WARNING'}, "No materials in list to assign.")
            return {'CANCELLED'}

        selected = context.selected_objects
        count = 0

        for obj in selected:
            if obj.type == 'MESH':
                obj.data.materials.clear()
                for mat in materials:
                    obj.data.materials.append(mat)
                count += 1

        self.report({'INFO'}, f"Assigned {len(materials)} material(s) to {count} object(s).")
        return {'FINISHED'}


# ------------------------------------------------------------------------
# UIList to show materials
# ------------------------------------------------------------------------
class MATERIAL_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        row.prop(item, "material", text="", emboss=True, icon='MATERIAL')


# ------------------------------------------------------------------------
# Panel
# ------------------------------------------------------------------------
class MATERIAL_PT_BatchAssigner(bpy.types.Panel):
    bl_label = "Batch Material Assigner"
    bl_idname = "MATERIAL_PT_batch_assigner"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Materials"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.template_list("MATERIAL_UL_List", "", scene, "material_list", scene, "material_list_index")

        col = row.column(align=True)
        col.operator("material.add_to_list", icon='ADD', text="")
        col.operator("material.remove_from_list", icon='REMOVE', text="")

        layout.separator()
        layout.operator("material.apply_list", icon='CHECKMARK')


# ------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------
classes = (
    MaterialListItem,
    MATERIAL_OT_AddToList,
    MATERIAL_OT_RemoveFromList,
    MATERIAL_OT_ApplyList,
    MATERIAL_UL_List,
    MATERIAL_PT_BatchAssigner,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.material_list = bpy.props.CollectionProperty(type=MaterialListItem)
    bpy.types.Scene.material_list_index = bpy.props.IntProperty(default=0)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.material_list
    del bpy.types.Scene.material_list_index


if __name__ == "__main__":
    register()
