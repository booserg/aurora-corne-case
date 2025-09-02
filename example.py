import cadquery as cq
import os

def draw_rectangle_sketch(wp: cq.Workplane) -> cq.Workplane:
    """Draw rectangle sketch on the given workplane."""
    wp = wp.moveTo(-10, -25)  # Start at corner
    wp = wp.lineTo(10, -25)   # Bottom edge
    wp = wp.lineTo(10, 25)    # Right edge  
    wp = wp.lineTo(-10, 25)   # Top edge
    wp = wp.close()           # Close back to start
    return wp

def main():
    try:
        # Step 1: Create outer rectangle (20x50mm) using the method
        wp = draw_rectangle_sketch(cq.Workplane("XY"))
        
        # Step 2: Extrude to 11mm
        body = wp.extrude(11)
        
        # Step 3: Create inner rectangle (10x40mm) on top face
        inner_sketch = draw_rectangle_sketch(body.faces(">Z").workplane()).offset2D(-1)
        
        # Step 4: Cut 10mm deep pocket
        result = inner_sketch.cutBlind(-10)
        
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        
        # Export result
        output_path = "output/example_result.step"
        cq.exporters.export(result, output_path)
        
        print("Successfully created example with:")
        print("- 20x50mm base rectangle (11mm thick)")
        print("- 10x40mm pocket (10mm deep)")
        print("- 1mm floor thickness")
        print(f"3D model saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
