import ezdxf
from typing import List, Tuple

def list_dxf_lines(dxf_path: str) -> List[Tuple[Tuple[float, float], Tuple[float, float], str]]:
    """Load and list all straight line segments from DXF file, ignoring circles and arcs."""
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    
    lines = []
    print("DXF entities found:")
    
    for entity in msp:
        print(f"  - {entity.dxftype()}")
        
        if entity.dxftype() == 'LINE':
            start = (entity.dxf.start.x, entity.dxf.start.y)
            end = (entity.dxf.end.x, entity.dxf.end.y)
            lines.append((start, end, "LINE"))
            
        elif entity.dxftype() == 'LWPOLYLINE':
            # Handle polylines by extracting line segments
            points = entity.get_points()
            for i in range(len(points) - 1):
                start = (points[i][0], points[i][1])
                end = (points[i+1][0], points[i+1][1])
                lines.append((start, end, "POLYLINE"))
            # Close the polyline if it's closed
            if entity.closed:
                start = (points[-1][0], points[-1][1])
                end = (points[0][0], points[0][1])
                lines.append((start, end, "POLYLINE"))
    
    return lines

if __name__ == "__main__":
    dxf_path = "resources/Aurora Corne/Aurora Corne Bottom Plate - No kerf.dxf"
    
    try:
        lines = list_dxf_lines(dxf_path)
        
        print(f"\nFound {len(lines)} straight line segments:")
        for i, (start, end, source_type) in enumerate(lines):
            print(f"  Line {i+1} ({source_type}): ({start[0]:.3f}, {start[1]:.3f}) -> ({end[0]:.3f}, {end[1]:.3f})")
        
        # Check for disconnected lines
        print("\nChecking line connectivity:")
        disconnections = []
        tolerance = 0.001
        
        for i in range(len(lines) - 1):
            current_end = lines[i][1]  # end point of current line
            next_start = lines[i+1][0]  # start point of next line
            
            distance = ((current_end[0] - next_start[0])**2 + (current_end[1] - next_start[1])**2)**0.5
            
            if distance > tolerance:
                gap_info = f"  Gap between Line {i+1} and Line {i+2}: {distance:.3f} units"
                print(gap_info)
                print(f"    Line {i+1} ends at: ({current_end[0]:.3f}, {current_end[1]:.3f})")
                print(f"    Line {i+2} starts at: ({next_start[0]:.3f}, {next_start[1]:.3f})")
                disconnections.append((i+1, i+2, distance))
        
        # Check if last line connects back to first line (closed loop)
        if lines:
            last_end = lines[-1][1]
            first_start = lines[0][0]
            distance = ((last_end[0] - first_start[0])**2 + (last_end[1] - first_start[1])**2)**0.5
            
            if distance > tolerance:
                gap_info = f"  Gap between last line ({len(lines)}) and first line (1): {distance:.3f} units"
                print(gap_info)
                print(f"    Last line ends at: ({last_end[0]:.3f}, {last_end[1]:.3f})")
                print(f"    First line starts at: ({first_start[0]:.3f}, {first_start[1]:.3f})")
                disconnections.append((len(lines), 1, distance))
        
        if not disconnections:
            print("  All lines are properly connected!")
        
    except Exception as e:
        print(f"Error: {e}")