# Etch

A simple domain-specific language for creating charts (bar and pie), written in Python.

## Overview

Etch lets you define charts using a declarative text syntax. Write your data and chart specifications in an `.etch` file, then render it to SVG.

## Installation

```bash
# Clone or navigate to the project
cd etch

# No additional dependencies needed (uses Python standard library)
```

## Quick Start

```bash
# Render an .etch file to SVG
python -m etch render example.etch -o output.svg
```

## Syntax

### Variable Declaration

Define data as a JSON array:

```
%sales = [{"month":"Jan","price":100},{"month":"Feb","price":150}]
```

### Bar Chart Command

Create a bar chart by specifying which fields to use for labels and values:

```
%chartbar : %sales.month = %sales.price
```

- Left of `=` — the field for X-axis labels
- Right of `=` — the field for Y-axis values

### Pie Chart Command

Create a pie chart using the same field syntax:

```
%chartpie : %sales.month = %sales.price
```

The pie chart automatically:
- Calculates percentages from the total
- Assigns colors from a palette
- Displays a legend

### Full Examples

**Bar Chart:**
```etch
%sales = [{"month":"Jan","price":100},{"month":"Feb","price":150}]
%chartbar : %sales.month = %sales.price
```

**Pie Chart:**
```etch
%budget = [{"category":"Rent","amount":1200},{"category":"Food","amount":600}]
%chartpie : %budget.category = %budget.amount
```

## Architecture

```
Input (.etch) → Tokenizer → Parser → Interpreter → SVG
```

| Stage | File | Purpose |
|-------|------|---------|
| Tokenize | `etch/tokenizer.py` | Lex input into tokens |
| Parse | `etch/parser.py` | Convert tokens to declarations + commands |
| Interpret | `etch/interpreter.py` | Resolve data into a scene graph |
| Render | `etch/render_svg.py` | Generate SVG string |

## Running Tests

```bash
pytest tests/
```

## Example Files

- `example.etch` - Sample bar chart definition
- `example.svg` - Rendered bar chart
- `pie.etch` - Sample pie chart definition
- `pie.svg` - Rendered pie chart

## Extending Etch

The project structure makes it easy to add new features:

- **New token types** — edit `tokenizer.py`
- **New chart types** — edit `parser.py` and `interpreter.py`
- **New render styles** — edit `render_svg.py`
