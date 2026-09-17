# Etch

A simple domain-specific language for creating interactive charts, written in Python.

## Overview

Etch lets you define charts using a declarative text syntax. Render to static SVG or interactive HTML with Chart.js.

## Installation

```bash
# Clone or navigate to the project
cd etch

# No additional dependencies needed (uses Python standard library)
```

## Quick Start

```bash
# Static SVG
python -m etch render example.etch -o output.svg

# Interactive HTML (Chart.js)
python -m etch interactive example.etch -o output.html
```

## Syntax

### Variable Declaration

Define data as a JSON array:

```
%sales = [{"month":"Jan","price":100},{"month":"Feb","price":150}]
```

### Bar Chart

```
%chartbar : %sales.month = %sales.price
```

### Pie Chart

```
%chartpie : %sales.month = %sales.price
```

## Output Formats

| Command | Output | Use Case |
|---------|--------|----------|
| `render` | SVG | Static, embeddable charts |
| `interactive` | HTML | Interactive with tooltips, hover |

## Architecture

```
Input (.etch) → Tokenizer → Parser → Interpreter → Renderer (SVG/HTML)
```

| Stage | File |
|-------|------|
| Tokenize | `tokenizer.py` |
| Parse | `parser.py` |
| Interpret | `interpreter.py` |
| Render SVG | `render_svg.py` |
| Render HTML | `render_html.py` |

## Running Tests

```bash
pytest tests/
```

## Extending Etch

- **New token types** — edit `tokenizer.py`
- **New chart types** — edit `parser.py` and `interpreter.py`
- **New renderers** — add new `render_*.py` files
