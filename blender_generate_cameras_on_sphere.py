bl_info = {
    "name": "Generate Cameras on Sphere",
    "description": "Generate n cameras on sphere radius r",
    "blender": (3, 6, 0),
    "version": (0, 0, 1),
    "category": "Object",
    "author": "dwkim / wooni",
    "wiki_url": "https://github.com/wooni-github/blender-gen-cams-on-sphere-addons",
    "tracker_url": "https://github.com/wooni-github/blender-gen-cams-on-sphere-addons/issues",
}

import bpy
import math
from mathutils import Vector

class SimpleInputProperties(bpy.types.PropertyGroup):
    num_cameras: bpy.props.IntProperty(
        name="Number of Cameras",
        description="An integer input for the number of cameras",
        default=100,
    )
    radius: bpy.props.FloatProperty(
        name="Radius",
        description="A float input for the radius",
        default=10.0,
    )
    clip_start: bpy.props.FloatProperty(
        name="Clip Start",
        description="Clip start value",
        default=0.1,
    )
    clip_end: bpy.props.FloatProperty(
        name="Clip End",
        description="Clip end value",
        default=10.0,
    )

class SimpleInputPanel(bpy.types.Panel):
    bl_label = "Generate Camers On Sphere"
    bl_idname = "OBJECT_PT_simple_input"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Camers On Sphere'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        simple_input = scene.simple_input

        layout.prop(simple_input, "num_cameras")
        layout.prop(simple_input, "radius")
        layout.prop(simple_input, "clip_start")
        layout.prop(simple_input, "clip_end")
        layout.operator("object.generate_cameras", text="Generate Cameras")

class GenerateCamerasOperator(bpy.types.Operator):
    bl_idname = "object.generate_cameras"
    bl_label = "Generate Cameras"

    def execute(self, context):
        scene = context.scene
        simple_input = scene.simple_input

        num_cameras = simple_input.num_cameras
        radius = simple_input.radius
        clip_start = simple_input.clip_start
        clip_end = simple_input.clip_end

        # Delete all existing cameras
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='CAMERA')
        bpy.ops.object.delete()

        # Create cameras using the Fibonacci lattice method
        for i in range(num_cameras):
            # Calculate the spherical coordinates using Fibonacci lattice
            offset = 2.0 / num_cameras
            increment = math.pi * (3.0 - math.sqrt(5.0))
            y = ((i * offset) - 1) + (offset / 2)
            r = math.sqrt(1 - y * y)
            theta = i * increment

            # Convert spherical coordinates to Cartesian coordinates
            x = r * math.cos(theta) * radius
            y = y * radius
            z = r * math.sin(theta) * radius

            # Create a new camera
            bpy.ops.object.camera_add(location=(x, y, z))
            camera = bpy.context.object

            # Set the clip start and end values
            camera.data.clip_start = clip_start
            camera.data.clip_end = clip_end
            
            # Point the camera towards the origin
            direction = Vector((0, 0, 0)) + Vector((x, y, z))
            camera.rotation_mode = 'QUATERNION'
            camera.rotation_quaternion = direction.to_track_quat('Z', 'Y')

            # Optionally, rename the camera for better identification
            camera.name = f'Camera_{i+1}'
        
        self.report({'INFO'}, "Cameras created successfully!")
        print("Cameras created successfully!")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(SimpleInputProperties)
    bpy.utils.register_class(SimpleInputPanel)
    bpy.utils.register_class(GenerateCamerasOperator)
    bpy.types.Scene.simple_input = bpy.props.PointerProperty(type=SimpleInputProperties)

def unregister():
    bpy.utils.unregister_class(SimpleInputProperties)
    bpy.utils.unregister_class(SimpleInputPanel)
    bpy.utils.unregister_class(GenerateCamerasOperator)
    del bpy.types.Scene.simple_input

if __name__ == "__main__":
    register()
