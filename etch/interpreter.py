from etch.parser import ParsedProgram, ChartCommand


# Default color palette
COLORS = [
    "#4A90D9", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6",
    "#1ABC9C", "#E67E22", "#3498DB", "#95A5A6", "#D35400"
]


def _get_data(program: ParsedProgram, x_field: str, y_field: str) -> list[dict]:
    """Extract data from declarations based on field references."""
    x_var, x_key = x_field.split('.')
    y_var, y_key = y_field.split('.')
    
    # Use the same variable for x and y (assumes same data source)
    data = program.declarations.get(x_var, [])
    return data, x_key, y_key


def interpret(program: ParsedProgram) -> list[dict]:
    """Interpret a ParsedProgram to produce a scene graph (list of shapes)."""
    scene = []

    for command in program.commands:
        config = command.config
        
        if command.type == "bar":
            data, x_key, y_key = _get_data(program, command.x_field, command.y_field)

            for row in data:
                label = row.get(x_key, "")
                value = row.get(y_key, 0)
                scene.append({
                    "type": "bar",
                    "label": label,
                    "value": value,
                    "config": config
                })
        
        elif command.type == "pie":
            data, x_key, y_key = _get_data(program, command.x_field, command.y_field)
            
            total = sum(row.get(y_key, 0) for row in data)
            
            for idx, row in enumerate(data):
                label = row.get(x_key, "")
                value = row.get(y_key, 0)
                percentage = value / total if total > 0 else 0
                color = COLORS[idx % len(COLORS)]
                scene.append({
                    "type": "pie_slice",
                    "label": label,
                    "value": value,
                    "percentage": percentage,
                    "color": color,
                    "config": config
                })

        elif command.type == "line":
            data, x_key, y_key = _get_data(program, command.x_field, command.y_field)
            
            # Collect all points for line chart
            points = []
            for row in data:
                label = row.get(x_key, "")
                value = row.get(y_key, 0)
                points.append({"label": label, "value": value})
            
            scene.append({
                "type": "line",
                "points": points,
                "config": config
            })
        
        elif command.type == "scatter":
            data, x_key, y_key = _get_data(program, command.x_field, command.y_field)
            
            points = []
            for idx, row in enumerate(data):
                x = row.get(x_key, 0)
                y = row.get(y_key, 0)
                color = COLORS[idx % len(COLORS)]
                points.append({"x": x, "y": y, "color": color})
            
            scene.append({
                "type": "scatter",
                "points": points,
                "config": config
            })

    return scene
