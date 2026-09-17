import pytest
from etch.tokenizer import tokenize, TokenType
from etch.parser import parse, ParsedProgram, ChartCommand


def test_parser_example_input():
    """Test parser with the example input."""
    text = "%sales = [{\"month\":\"Jan\",\"price\":100},{\"month\":\"Feb\",\"price\":150}]\n%chartbar : %sales.month = %sales.price"
    
    tokens = tokenize(text)
    program = parse(tokens)
    
    # Check declarations
    assert isinstance(program, ParsedProgram)
    assert "sales" in program.declarations
    sales_data = program.declarations["sales"]
    assert len(sales_data) == 2
    assert sales_data[0]["month"] == "Jan"
    assert sales_data[0]["price"] == 100
    assert sales_data[1]["month"] == "Feb"
    assert sales_data[1]["price"] == 150
    
    # Check commands
    assert len(program.commands) == 1
    cmd = program.commands[0]
    assert isinstance(cmd, ChartCommand)
    assert cmd.type == "bar"
    assert cmd.x_field == "sales.month"
    assert cmd.y_field == "sales.price"