# Etch Examples

A simple DSL for creating interactive charts.

## Quick Start

```bash
# Render interactive HTML
python -m etch interactive your_chart.etch -o output.html
```

## Syntax

```etch
%data = [{"label":"A","value":100},{"label":"B","value":150}]
%chartbar : %data.label = %data.value
%chartpie : %data.label = %data.value
```

## Commands

| Command | Output |
|---------|--------|
| `python -m etch render input.etch -o output.svg` | Static SVG |
| `python -m etch interactive input.etch -o output.html` | Interactive HTML |

## Usage in Obsidian

Embed interactive charts in your Obsidian notes using:

```markdown
![Bar Chart](test.html)
```

Or use iframe embedding:

```html
<iframe src="test.html" width="100%" height="350"></iframe>
```

## Live Charts

![Bar Chart](test.html)
![Pie Chart](pie.html)
