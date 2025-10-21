bl_info = {
    "name": "ObjectMesh_Renamer",
    "author": "Millenne Noel",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Renamer",
    "description": "Rename selected objects and their meshes with a prefix and append text",
    "category": "Object",
}

import bpy

class OBJECT_OT_ObjectMeshRename(bpy.types.Operator):
    """Rename selected objects and their mesh data with append text"""
    bl_idname = "object.objectmesh_rename"
    bl_label = "Rename Object + Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefix = context.scene.rename_prefix
        append_text = context.scene.rename_append

        for obj in context.selected_objects:
            new_name = prefix + "_" + append_text
            # Rename object
            obj.name = new_name
            
            # Rename mesh if it exists
            if obj.type == 'MESH' and obj.data:
                obj.data.name = new_name
        
        return {'FINISHED'}


class OBJECT_PT_ObjectMeshRenamerPanel(bpy.types.Panel):
    bl_label = "ObjectMesh_Renamer"
    bl_idname = "OBJECT_PT_objectmesh_renamer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Renamer"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "rename_prefix")
        layout.prop(context.scene, "rename_append")
        layout.operator("object.objectmesh_rename", text="Rename Object + Mesh")


def register():
    bpy.utils.register_class(OBJECT_OT_ObjectMeshRename)
    bpy.utils.register_class(OBJECT_PT_ObjectMeshRenamerPanel)
    bpy.types.Scene.rename_prefix = bpy.props.StringProperty(name="Prefix", default="MyObject")
    bpy.types.Scene.rename_append = bpy.props.StringProperty(name="Append", default="_01")


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ObjectMeshRename)
    bpy.utils.unregister_class(OBJECT_PT_ObjectMeshRenamerPanel)
    del bpy.types.Scene.rename_prefix
    del bpy.types.Scene.rename_append


if __name__ == "__main__":
    register()
