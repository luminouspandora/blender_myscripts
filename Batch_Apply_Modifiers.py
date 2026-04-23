bl_info = {
    "name": "Finalize Geometry Tools",
    "author": "Millenne Noel",
    "version": (1, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > N Panel > CustomTools",
    "description": "Batch apply modifiers on selected mesh objects",
    "category": "Object",
}

import bpy


def apply_all_modifiers(context, objects):
    if context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    active_obj = context.view_layer.objects.active
    applied_count = 0

    for obj in objects:
        if obj.type != 'MESH':
            continue

        context.view_layer.objects.active = obj

        # Copy list to avoid skipping
        for mod in list(obj.modifiers):
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
                applied_count += 1
            except RuntimeError:
                print(f"Could not apply modifier: {mod.name} on {obj.name}")

    context.view_layer.objects.active = active_obj
    return applied_count


class OBJECT_OT_apply_all_modifiers(bpy.types.Operator):
    bl_idname = "object.apply_all_modifiers"
    bl_label = "Apply All Modifiers"
    bl_description = "Apply all modifiers on selected mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = apply_all_modifiers(context, context.selected_objects)

        self.report({'INFO'}, f"Applied {count} modifiers")
        return {'FINISHED'}


class VIEW3D_PT_finalize_geometry(bpy.types.Panel):
    bl_label = "Finalize Geometry"
    bl_idname = "VIEW3D_PT_finalize_geometry"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CustomTools"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Modifiers:")
        layout.operator("object.apply_all_modifiers", icon='MODIFIER')


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