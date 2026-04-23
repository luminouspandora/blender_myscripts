bl_info = {
    "name": "Finalize Geometry Tools",
    "author": "Your Studio / You",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > N Panel > Tools",
    "description": "Batch apply modifiers on selected mesh objects",
    "category": "Object",
}

import bpy


def apply_all_modifiers(objects):
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    active_obj = bpy.context.view_layer.objects.active

    for obj in objects:
        if obj.type != 'MESH':
            continue

        bpy.context.view_layer.objects.active = obj

        for mod in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)

    bpy.context.view_layer.objects.active = active_obj


class OBJECT_OT_apply_all_modifiers(bpy.types.Operator):
    bl_idname = "object.apply_all_modifiers"
    bl_label = "Apply All Modifiers"
    bl_description = "Apply all modifiers on selected mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_all_modifiers(context.selected_objects)
        return {'FINISHED'}


class VIEW3D_PT_finalize_geometry(bpy.types.Panel):
    bl_label = "Finalize Geometry"
    bl_idname = "VIEW3D_PT_finalize_geometry"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CustomTools"

    def draw(self, context):
        self.layout.operator("object.apply_all_modifiers", icon='MODIFIER')


classes = (
    OBJECT_OT_apply_all_modifiers,
    VIEW3D_PT_finalize_geometry,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
