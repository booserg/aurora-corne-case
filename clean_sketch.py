import cadquery as cq
import os

def draw_keyboard_sketch(wp: cq.Workplane) -> cq.Workplane:
    """Draw keyboard sketch on the given workplane."""
    wp = wp.moveTo(82.250, -65.750)
    
    # Add all line segments in order
    wp = wp.lineTo(81.750, -66.250)  # Line 1
    wp = wp.lineTo(81.750, -67.500)  # Line 2
    wp = wp.lineTo(81.250, -68.000)  # Line 3
    wp = wp.lineTo(61.500, -68.000)  # Line 4
    wp = wp.lineTo(61.000, -68.500)  # Line 5
    wp = wp.lineTo(61.000, -128.500)  # Line 6
    wp = wp.lineTo(74.950, -152.800)  # Line 7
    wp = wp.lineTo(76.180, -153.030)  # Line 8
    wp = wp.lineTo(91.000, -144.500)  # Line 9
    wp = wp.lineTo(128.000, -139.000)  # Line 10
    wp = wp.lineTo(128.352, -138.855)  # Line 11
    wp = wp.lineTo(138.896, -124.396)  # Line 12
    wp = wp.lineTo(139.250, -124.250)  # Line 13
    wp = wp.lineTo(175.250, -124.250)  # Line 14
    wp = wp.lineTo(194.250, -124.250)  # Line 15
    wp = wp.lineTo(194.750, -123.750)  # Line 16
    wp = wp.lineTo(194.750, -68.500)  # Line 17
    wp = wp.lineTo(194.250, -68.000)  # Line 18
    wp = wp.lineTo(157.250, -68.000)  # Line 19
    wp = wp.lineTo(156.750, -67.500)  # Line 20
    wp = wp.lineTo(156.750, -63.750)  # Line 21
    wp = wp.lineTo(156.250, -63.250)  # Line 22
    wp = wp.lineTo(138.250, -63.250)  # Line 23
    wp = wp.lineTo(137.750, -62.750)  # Line 24
    wp = wp.lineTo(137.750, -61.500)  # Line 25
    wp = wp.lineTo(137.250, -61.000)  # Line 26
    wp = wp.lineTo(120.250, -61.000)  # Line 27
    wp = wp.lineTo(119.750, -61.500)  # Line 28
    wp = wp.lineTo(119.750, -62.750)  # Line 29
    wp = wp.lineTo(119.250, -63.250)  # Line 30
    wp = wp.lineTo(101.250, -63.250)  # Line 31
    wp = wp.lineTo(100.750, -63.750)  # Line 32
    wp = wp.lineTo(100.750, -65.250)  # Line 33
    wp = wp.lineTo(100.250, -65.750)  # Line 34
    # Line 35 closes back to start point
    
    return wp.close()

def draw_controller_wall_sketch(wp: cq.Workplane) -> cq.Workplane:
    """Draw keyboard sketch on the given workplane."""
    wp = wp.moveTo(61.500, -68.000)
    
    # Add all line segments in order
    wp = wp.lineTo(61.500 + 18, -68.000)  # Line 1
    wp = wp.lineTo(61.500 + 18, -68.000 + 1)  # Line 1

    # External corner
    wp = wp.lineTo(61.500, -68.000 + 1)
    wp = wp.lineTo(60.793, -67.293)
    wp = wp.lineTo(60.293, -67.793)
    wp = wp.lineTo(60.000, -68.500)

    wp = wp.lineTo(60.000, -128.500)
    wp = wp.lineTo(61.000, -128.500)
    wp = wp.lineTo(61.000, -68.500)
    wp = wp.lineTo(61.500, -68.000)
    
    return wp.close()

def draw_controller_roof_sketch(wp: cq.Workplane) -> cq.Workplane:
    """Draw keyboard sketch on the given workplane."""
    wp = wp.moveTo(79.5, -67)
    
    # Add all line segments in order
    wp = wp.lineTo(61.5, -67)
    wp = wp.lineTo(60.793, -67.293)
    wp = wp.lineTo(60.293, -67.793)
    wp = wp.lineTo(60, -68.5)
    wp = wp.lineTo(60, -128.5)
    wp = wp.lineTo(61, -128.5)
    wp = wp.lineTo(79.5, -128.5 + 10)
    wp = wp.lineTo(79.5, -68)
    
    return wp.close()

if __name__ == "__main__":
    try:
        # Step 1: Create base with 1mm outward offset and extrude 6mm
        base_sketch = draw_keyboard_sketch(cq.Workplane("XY")).offset2D(1.0)
        body = base_sketch.extrude(6)
        
        # Step 2: Create pocket using original sketch on top face
        pocket_sketch = draw_keyboard_sketch(body.faces(">Z").workplane())
        
        # Step 3: Cut 5mm deep pocket
        result = pocket_sketch.cutBlind(-5)
        
        controller_wall_sketch = draw_controller_wall_sketch(result.faces(">Z").workplane())
        wall = controller_wall_sketch.extrude(6)

        controller_roof_sketch = draw_controller_roof_sketch(wall.faces(">Z").workplane())
        cover = controller_roof_sketch.extrude(1)

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        
        # Export result
        output_path = "output/clean_sketch_result.step"
        cq.exporters.export(cover, output_path)
        
        print("Successfully created case with:")
        print("- 1mm offset base (6mm thick)")
        print("- 5mm deep pocket using original outline")  
        print("- 1mm wall thickness and 1mm floor thickness")
        print(f"3D model saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
