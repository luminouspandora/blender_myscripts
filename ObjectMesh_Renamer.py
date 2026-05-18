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
        ('BALCONIES', "Balconies", ""),
        ('BASE', "Base", ""),
        ('COURTYARDS', "Courtyards", ""),
        ('DOORS', "Doors", ""),
        ('FIXTURES', "Fixtures", ""),
        ('FOUNDATION', "Foundation", ""),
        ('GATES', "Gates", ""),
        ('GARDENS', "Gardens", ""),
        ('MOLDINGS', "Moldings", ""),
        ('ORNAMENTS', "Ornaments", ""),
        ('PASSAGES', "Passages", ""),
        ('PLINTH', "Plinth", ""),
        ('RAILINGS', "Railings", ""),
        ('ROOFS', "Roofs", ""),
        ('SHOPDOORS', "Shopdoors", ""),
        ('SHOPFRONTS', "Shopfronts", ""),
        ('SHUTTERS', "Shutters", ""),    
        ('URBAN_EQUIPMENT', "Urban Equipment", ""),
        ('WINDOWS', "Windows", ""),
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

        for i, obj in enumerate(sorted(selected, key=lambda o: o.name), start=1):

            parts = []

            if prefix:
                parts.append(prefix)

            if preset != 'NONE':
                parts.append(preset)

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
                mesh_name = new_name
                counter = 1

                while mesh_name in bpy.data.meshes:
                    mesh_name = f"{new_name}_{str(counter).zfill(3)}"
                    counter += 1

                obj.data.name = mesh_name

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