import argparse
import sys
from pathlib import Path

from etch.tokenizer import tokenize
from etch.parser import parse
from etch.interpreter import interpret
from etch.render_svg import render_svg
from etch.render_html import render_html


def main():
    parser = argparse.ArgumentParser(description="Etch - a language for making charts")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # render command (SVG)
    render_parser = subparsers.add_parser("render", help="Render an Etch file to static SVG")
    render_parser.add_argument("input_file", help="Input .etch file")
    render_parser.add_argument("-o", "--output", required=True, help="Output SVG file")
    
    # interactive command (HTML)
    interactive_parser = subparsers.add_parser("interactive", help="Render an Etch file to interactive HTML")
    interactive_parser.add_argument("input_file", help="Input .etch file")
    interactive_parser.add_argument("-o", "--output", required=True, help="Output HTML file")
    
    args = parser.parse_args()
    
    # Read input file (common to both commands)
    input_path = Path(args.input_file) if args.command else None
    
    if args.command == "render":
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' not found", file=sys.stderr)
            sys.exit(1)
        
        text = input_path.read_text(encoding="utf-8")
        
        # Run the pipeline
        tokens = tokenize(text)
        program = parse(tokens)
        scene = interpret(program)
        svg = render_svg(scene)
        
        # Write output
        output_path = Path(args.output)
        output_path.write_text(svg, encoding="utf-8")
        
        print(f"Created {output_path}")
    
    elif args.command == "interactive":
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' not found", file=sys.stderr)
            sys.exit(1)
        
        text = input_path.read_text(encoding="utf-8")
        
        # Run the pipeline
        tokens = tokenize(text)
        program = parse(tokens)
        scene = interpret(program)
        
        # Extract title from filename
        title = input_path.stem.replace("_", " ").title()
        
        html = render_html(scene, title)
        
        # Write output
        output_path = Path(args.output)
        output_path.write_text(html, encoding="utf-8")
        
        print(f"Created {output_path}")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
