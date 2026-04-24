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


# 🔹 ENUM 
def get_append_presets(self, context):
    return [
        ('NONE', "None", ""),

        ('WINDOWS', "Windows", ""),
        ('DOORS', "Doors", ""),
        ('SHOPFRONTS', "Shopfronts", ""),
        ('ROOFS', "Roofs", ""),
        ('BASE', "Base", ""),
        ('FOUNDATION', "Foundation", ""),
        ('PLINTH', "Plinth", ""),
        ('MOLDINGS', "Moldings", ""),
        ('BALCONIES', "Balconies", ""),
        ('RAILINGS', "Railings", ""),
        ('GATES', "Gates", ""),
        ('SHUTTERS', "Shutters", ""),
        ('COURTYARDS', "Courtyards", ""),
        ('PASSAGES', "Passages", ""),
        ('GARDENS', "Gardens", ""),
        ('FIXTURES', "Fixtures", ""),
        ('URBAN_EQUIPMENT', "Urban Equipment", ""),
    ]


class OBJECT_OT_ObjectMeshRename(bpy.types.Operator):
    """Rename selected objects and their mesh data"""
    bl_idname = "object.objectmesh_rename"
    bl_label = "Rename Object + Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        prefix = scene.rename_prefix.strip()
        preset = scene.rename_append_preset
        custom = scene.rename_append.strip()

        selected = context.selected_objects
        use_numbering = len(selected) > 1

        for i, obj in enumerate(selected, start=1):

            parts = [prefix]

            # Add preset
            if preset != 'NONE':
                parts.append(preset)

            # Add custom text
            if custom:
                parts.append(custom)

            # Add numbering ONLY if multiple objects
            if use_numbering:
                parts.append(str(i).zfill(3))

            new_name = "_".join(parts)

            # Rename object
            obj.name = new_name

            # Rename mesh
            if obj.type == 'MESH' and obj.data:
                obj.data.name = new_name

        return {'FINISHED'}


class OBJECT_PT_ObjectMeshRenamerPanel(bpy.types.Panel):
    bl_label = "ObjectMesh_Renamer"
    bl_idname = "OBJECT_PT_objectmesh_renamer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CustomTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "rename_prefix")

        layout.label(text="Append Category:")
        layout.prop(scene, "rename_append_preset", text="")

        layout.label(text="Custom Append:")
        layout.prop(scene, "rename_append", text="")

        layout.operator("object.objectmesh_rename", text="Rename")


def register():
    bpy.utils.register_class(OBJECT_OT_ObjectMeshRename)
    bpy.utils.register_class(OBJECT_PT_ObjectMeshRenamerPanel)

    bpy.types.Scene.rename_prefix = bpy.props.StringProperty(
        name="Prefix", default="MyObject"
    )

    bpy.types.Scene.rename_append = bpy.props.StringProperty(
        name="Custom", default=""
    )

    bpy.types.Scene.rename_append_preset = bpy.props.EnumProperty(
        name="Preset",
        items=get_append_presets
    )


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ObjectMeshRename)
    bpy.utils.unregister_class(OBJECT_PT_ObjectMeshRenamerPanel)

    del bpy.types.Scene.rename_prefix
    del bpy.types.Scene.rename_append
    del bpy.types.Scene.rename_append_preset


if __name__ == "__main__":
    register()