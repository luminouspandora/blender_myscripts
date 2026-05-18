bl_info = {
    "name": "Collection Asset Multi Tagger",
    "author": "Millenne Noel",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > CustomTools",
    "description": "Apply multiple tags to the active collection asset",
    "category": "Object",
}

import bpy


# =========================================
# OPERATOR
# =========================================

class COLLECTION_OT_ApplyAssetTags(bpy.types.Operator):
    """Apply comma-separated tags to active collection asset"""
    bl_idname = "collection.apply_asset_tags"
    bl_label = "Apply Collection Asset Tags"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        collection = context.collection

        if not collection:
            self.report({'WARNING'}, "No active collection")
            return {'CANCELLED'}

        raw_tags = context.scene.asset_tags_input

        if not raw_tags.strip():
            self.report({'WARNING'}, "No tags entered")
            return {'CANCELLED'}

        # Mark collection as asset if not already
        if not collection.asset_data:
            collection.asset_mark()

        # Convert:
        # "window, french, shop"
        # -> ["window", "french", "shop"]
        tags = [
            tag.strip().lower()
            for tag in raw_tags.split(",")
            if tag.strip()
        ]

        existing_tags = [t.name for t in collection.asset_data.tags]

        for tag_name in tags:

            # Prevent duplicate tags
            if tag_name not in existing_tags:
                collection.asset_data.tags.new(tag_name)

        self.report(
            {'INFO'},
            f"Applied {len(tags)} tags to '{collection.name}'"
        )

        return {'FINISHED'}


# =========================================
# PANEL
# =========================================

class COLLECTION_PT_AssetMultiTagger(bpy.types.Panel):
    bl_label = "Collection Asset Multi Tagger"
    bl_idname = "COLLECTION_PT_asset_multi_tagger"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CustomTools"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        collection = context.collection

        if collection:
            layout.label(text=f"Active: {collection.name}")
        else:
            layout.label(text="No Active Collection")

        layout.separator()

        layout.label(text="Comma Separated Tags:")

        layout.prop(scene, "asset_tags_input", text="")

        layout.operator(
            "collection.apply_asset_tags",
            icon='ASSET_MANAGER'
        )


# =========================================
# REGISTER
# =========================================

classes = (
    COLLECTION_OT_ApplyAssetTags,
    COLLECTION_PT_AssetMultiTagger,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.asset_tags_input = bpy.props.StringProperty(
        name="Tags",
        description="Example: window, french, 3seg",
        default=""
    )


def unregister():

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.asset_tags_input


if __name__ == "__main__":
    register()