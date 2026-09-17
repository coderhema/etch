import argparse
import sys
from pathlib import Path

from etch.tokenizer import tokenize
from etch.parser import parse
from etch.interpreter import interpret
from etch.render_svg import render_svg


def main():
    parser = argparse.ArgumentParser(description="Etch - a language for making charts")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # render command
    render_parser = subparsers.add_parser("render", help="Render an Etch file to SVG")
    render_parser.add_argument("input_file", help="Input .etch file")
    render_parser.add_argument("-o", "--output", required=True, help="Output SVG file")
    
    args = parser.parse_args()
    
    if args.command == "render":
        # Read input file
        input_path = Path(args.input_file)
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
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()