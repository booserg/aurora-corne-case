import cadquery as cq
import os

# Paths
# dxf_path = "resources/Aurora Corne/Aurora Corne Bottom Plate - No kerf.dxf"
dxf_path = "resources/Aurora Corne/Aurora Corne Bottom Plate - No kerf - no holes.dxf"
output_dir = "output"
output_file = "aurora_corne_bottom_plate.step"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Import DXF to get the shape
imported_shape = cq.importers.importDXF(dxf_path)

# Debug: Print what we got from DXF
print(f"Imported shape type: {type(imported_shape)}")
print(f"Number of objects: {len(imported_shape.objects)}")

# Try to consolidate wires and create faces
consolidated = imported_shape.consolidateWires()
print(f"Consolidated wires: {len(consolidated.objects)}")

# Check what we have after consolidation
shape_obj = consolidated.objects[0]
print(f"Shape object type: {type(shape_obj)}")

# Since we have a Face object, create a solid using CadQuery's Solid.extrudeLinear
from cadquery.occ_impl.shapes import Face

if isinstance(shape_obj, Face):
    # Get the outer wire and offset it
    outer_wire = shape_obj.outerWire()
    offset_wire = outer_wire.offset2D(1.0)
    
    # Create a new face from the offset wire and extrude
    result = cq.Workplane("XY").add(offset_wire).toPending().extrude(6)
    print("Successfully offset face by 1mm and extruded to create solid")
else:
    raise ValueError(f"Unexpected shape type: {type(shape_obj)}")

# Save as STEP file
output_path = os.path.join(output_dir, output_file)
cq.exporters.export(result, output_path)

print(f"Successfully created 3D model and saved to: {output_path}")
