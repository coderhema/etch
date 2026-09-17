import json


def render_html(scene: list[dict], title: str = "Etch Chart") -> str:
    """Render a scene graph to an interactive HTML page with Chart.js."""
    
    # Separate bar and pie chart data
    bar_data = [s for s in scene if s["type"] == "bar"]
    pie_data = [s for s in scene if s["type"] == "pie_slice"]
    
    html_parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "  <meta charset='utf-8'>",
        f"  <title>{title}</title>",
        "  <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>",
        "  <style>",
        "    * { margin: 0; padding: 0; box-sizing: border-box; }",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 12px; }",
        "    .chart-container { position: relative; height: 250px; width: 100%; }",
        "    h2 { font-size: 14px; margin-bottom: 8px; color: #333; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h2>{title}</h2>",
    ]
    
    # Render bar chart if present
    if bar_data:
        labels = json.dumps([s["label"] for s in bar_data])
        values = json.dumps([s["value"] for s in bar_data])
        
        html_parts.extend([
            "  <div class='chart-container'>",
            "    <canvas id='barChart'></canvas>",
            "  </div>",
            "  <script>",
            f"    new Chart(document.getElementById('barChart'), {{",
            "      type: 'bar',",
            f"      data: {{",
            f"        labels: {labels},",
            "        datasets: [",
            "          {",
            "            label: 'Value',",
            f"            data: {values},",
            "            backgroundColor: 'rgba(74, 144, 217, 0.7)',",
            "            borderColor: 'rgba(74, 144, 217, 1)',",
            "            borderWidth: 1",
            "          }",
            "        ]",
            "      },",
            "      options: {",
            "        responsive: true,",
            "        scales: {",
            "          y: { beginAtZero: true }",
            "        }",
            "      }",
            "    }});",
            "  </script>",
        ])
    
    # Render pie chart if present
    if pie_data:
        labels = json.dumps([s["label"] for s in pie_data])
        values = json.dumps([s["value"] for s in pie_data])
        colors = json.dumps([s["color"] for s in pie_data])
        
        html_parts.extend([
            "  <div class='chart-container'>",
            "    <canvas id='pieChart'></canvas>",
            "  </div>",
            "  <script>",
            f"    new Chart(document.getElementById('pieChart'), {{",
            "      type: 'pie',",
            f"      data: {{",
            f"        labels: {labels},",
            "        datasets: [",
            "          {",
            "            label: 'Distribution',",
            f"            data: {values},",
            f"            backgroundColor: {colors},",
            "          }",
            "        ]",
            "      }},",
            "      options: {{",
            "        responsive: true,",
            "        plugins: {{",
            "          legend: {{ position: 'bottom' }},",
            "          tooltip: {{",
            "            callbacks: {{",
            "              label: function(context) {{",
            "                let value = context.raw;",
            "                let total = context.dataset.data.reduce((a, b) => a + b, 0);",
            "                let percentage = Math.round((value / total) * 100);",
            "                return context.label + ': ' + value + ' (' + percentage + '%)';",
            "              }}",
            "            }}",
            "          }}",
            "        }}",
            "      }}",
            "    }});",
            "  </script>",
        ])
    
    html_parts.extend([
        "</body>",
        "</html>",
    ])
    
    return "\n".join(html_parts)


def render_interactive(input_file: str, output_file: str):
    """Render an Etch file to interactive HTML."""
    from pathlib import Path
    from etch.tokenizer import tokenize
    from etch.parser import parse
    from etch.interpreter import interpret
    
    # Read input
    text = Path(input_file).read_text(encoding="utf-8")
    
    # Run pipeline
    tokens = tokenize(text)
    program = parse(tokens)
    scene = interpret(program)
    
    # Extract title from filename
    title = Path(input_file).stem.replace("_", " ").title()
    
    # Render HTML
    html = render_html(scene, title)
    
    # Write output
    Path(output_file).write_text(html, encoding="utf-8")
    print(f"Created {output_file}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Etch - render interactive charts")
    parser.add_argument("input_file", help="Input .etch file")
    parser.add_argument("-o", "--output", required=True, help="Output HTML file")
    args = parser.parse_args()
    render_interactive(args.input_file, args.output)