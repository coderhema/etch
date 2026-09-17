import pytest
from etch.tokenizer import tokenize
from etch.parser import parse
from etch.interpreter import interpret
from etch.render_svg import render_svg


def test_end_to_end_example():
    """Test the full pipeline produces valid SVG."""
    text = "%sales = [{\"month\":\"Jan\",\"price\":100},{\"month\":\"Feb\",\"price\":150}]\n%chartbar : %sales.month = %sales.price"
    
    tokens = tokenize(text)
    program = parse(tokens)
    scene = interpret(program)
    svg = render_svg(scene)
    
    # Check it's valid SVG
    assert svg.startswith('<svg')
    assert svg.endswith('</svg>')
    
    # Check contains exactly 2 rect elements (one for background, one per bar = 3 total)
    # Actually we have: 1 background rect + 2 bar rects = 3 rects
    rect_count = svg.count('<rect')
    assert rect_count == 3, f"Expected 3 rect elements, got {rect_count}"
    
    # Check contains the labels
    assert 'Jan' in svg
    assert 'Feb' in svg