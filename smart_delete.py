"""
    11/010/2025 MAN
    This is a blender script that allows you to select objects
    on the View Layer and delete both their Object and Mesh Data
"""

bl_info = {
    "name": "Quick Object Deleter",
    "author": "Millenne Noel",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Deleter",
    "description": "Deletes selected objects and their mesh data safely",
    "category": "Object",
}


import bpy


class OBJECT_OT_QuickDelete(bpy.types.Operator):
    """Delete selected objects and their mesh data"""
    bl_idname = "object.quick_delete"
    bl_label = "Delete Selected + Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = list(context.selected_objects)
        deleted_count = 0

        for obj in selected:
            mesh = obj.data if obj.type == 'MESH' else None

            # Unlink object first
            bpy.data.objects.remove(obj, do_unlink=True)
            deleted_count += 1

            # Now safely remove the mesh if no longer used
            if mesh and mesh.users == 0:
                bpy.data.meshes.remove(mesh)

        self.report({'INFO'}, f"Deleted {deleted_count} object(s) and their mesh data.")
        return {'FINISHED'}


class OBJECT_PT_QuickDeleter(bpy.types.Panel):
    bl_label = "Quick Deleter"
    bl_idname = "OBJECT_PT_quick_deleter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Deleter"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.quick_delete", text="Delete Selected + Mesh", icon='TRASH')


def register():
    bpy.utils.register_class(OBJECT_OT_QuickDelete)
    bpy.utils.register_class(OBJECT_PT_QuickDeleter)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_QuickDelete)
    bpy.utils.unregister_class(OBJECT_PT_QuickDeleter)


if __name__ == "__main__":
    register()