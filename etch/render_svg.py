import math


def render_svg(scene: list[dict]) -> str:
    """Render a scene graph to an SVG string."""
    # Find max value for scaling
    max_value = 1
    for shape in scene:
        if shape["type"] == "bar":
            max_value = max(max_value, shape.get("value", 0))

    # Canvas size
    width = 400
    height = 300
    bar_max_height = 250
    bar_width = 50
    padding = 50
    bottom_margin = 40

    svg_parts = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="white"/>'
    ]

    # Calculate bar positions
    num_bars = len([s for s in scene if s["type"] == "bar"])
    if num_bars > 0:
        total_bar_width = num_bars * bar_width
        spacing = (width - 2 * padding - total_bar_width) / (num_bars + 1)
        
        bar_index = 0
        for shape in scene:
            if shape["type"] == "bar":
                label = shape.get("label", "")
                value = shape.get("value", 0)
                
                # Calculate position
                x = padding + spacing + bar_index * (bar_width + spacing)
                bar_height = (value / max_value) * bar_max_height
                y = height - bottom_margin - bar_height
                
                # Add bar (blue)
                svg_parts.append(
                    f'  <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="#4A90D9"/>'
                )
                
                # Add label
                label_x = x + bar_width / 2
                svg_parts.append(
                    f'  <text x="{label_x}" y="{height - 10}" text-anchor="middle" font-family="sans-serif" font-size="12">{label}</text>'
                )
                
                bar_index += 1

    # Render pie charts
    pie_slices = [s for s in scene if s["type"] == "pie_slice"]
    if pie_slices:
        # Pie chart center and radius
        cx = 200
        cy = 150
        radius = 100
        
        # Start from top ( -90 degrees in SVG coordinate system)
        start_angle = -90
        
        legend_x = 320
        legend_y = 80
        
        for slice_data in pie_slices:
            percentage = slice_data.get("percentage", 0)
            color = slice_data.get("color", "#888888")
            label = slice_data.get("label", "")
            value = slice_data.get("value", 0)
            
            # Calculate angles
            sweep_angle = percentage * 360
            end_angle = start_angle + sweep_angle
            
            # Convert to radians for math
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Calculate coordinates
            x1 = cx + radius * math.cos(start_rad)
            y1 = cy + radius * math.sin(start_rad)
            x2 = cx + radius * math.cos(end_rad)
            y2 = cy + radius * math.sin(end_rad)
            
            # Determine if the arc is large (> 180 degrees)
            large_arc = 1 if sweep_angle > 180 else 0
            
            # Create path for pie slice
            if percentage < 1.0:
                path = f"M {cx} {cy} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z"
            else:
                # Full circle
                path = f"M {cx} {cy-radius} A {radius} {radius} 0 1 1 {cx} {cy+radius} A {radius} {radius} 0 1 1 {cx} {cy-radius}"
            
            svg_parts.append(f'  <path d="{path}" fill="{color}" stroke="white" stroke-width="1"/>')
            
            # Add legend entry
            svg_parts.append(
                f'  <rect x="{legend_x}" y="{legend_y}" width="15" height="15" fill="{color}"/>'
            )
            svg_parts.append(
                f'  <text x="{legend_x + 20}" y="{legend_y + 12}" font-family="sans-serif" font-size="11">{label}</text>'
            )
            
            legend_y += 20
            
            # Move to next slice
            start_angle = end_angle

    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)
