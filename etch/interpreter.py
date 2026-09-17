from etch.parser import ParsedProgram, ChartCommand


def interpret(program: ParsedProgram) -> list[dict]:
    """Interpret a ParsedProgram to produce a scene graph (list of shapes)."""
    scene = []

    for command in program.commands:
        if command.type == "bar":
            # Resolve x and y fields from declarations
            x_field = command.x_field  # e.g., "sales.month"
            y_field = command.y_field  # e.g., "sales.price"

            # Parse the field references: variable.field
            x_var, x_key = x_field.split('.')
            y_var, y_key = y_field.split('.')

            # Get the data from declarations
            data = program.declarations.get(x_var, [])

            # Build bar shapes for each data row
            for row in data:
                label = row.get(x_key, "")
                value = row.get(y_key, 0)
                scene.append({
                    "type": "bar",
                    "label": label,
                    "value": value
                })
        
        elif command.type == "pie":
            # Resolve x and y fields from declarations
            x_field = command.x_field
            y_field = command.y_field

            # Parse the field references: variable.field
            x_var, x_key = x_field.split('.')
            y_var, y_key = y_field.split('.')

            # Get the data from declarations
            data = program.declarations.get(x_var, [])
            
            # Calculate total for percentages
            total = sum(row.get(y_key, 0) for row in data)
            
            # Assign colors from a palette
            colors = [
                "#4A90D9", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6",
                "#1ABC9C", "#E67E22", "#3498DB", "#95A5A6", "#D35400"
            ]
            
            # Build pie slice shapes for each data row
            for idx, row in enumerate(data):
                label = row.get(x_key, "")
                value = row.get(y_key, 0)
                percentage = value / total if total > 0 else 0
                color = colors[idx % len(colors)]
                scene.append({
                    "type": "pie_slice",
                    "label": label,
                    "value": value,
                    "percentage": percentage,
                    "color": color
                })

    return scene
