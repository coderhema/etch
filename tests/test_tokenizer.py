import pytest
from etch.tokenizer import tokenize, TokenType


def test_tokenize_example_input():
    """Test tokenizer with the example input."""
    text = "%sales = [{\"month\":\"Jan\",\"price\":100},{\"month\":\"Feb\",\"price\":150}]\n%chartbar : %sales.month = %sales.price"
    
    tokens = tokenize(text)
    token_types = [t.type for t in tokens]
    
    # Expected sequence of token types
    expected = [
        TokenType.PERCENT,
        TokenType.IDENTIFIER,
        TokenType.EQUALS,
        TokenType.JSON_VALUE,
        TokenType.NEWLINE,
        TokenType.PERCENT,
        TokenType.IDENTIFIER,
        TokenType.COLON,
        TokenType.PERCENT,
        TokenType.IDENTIFIER,
        TokenType.DOT,
        TokenType.IDENTIFIER,
        TokenType.EQUALS,
        TokenType.PERCENT,
        TokenType.IDENTIFIER,
        TokenType.DOT,
        TokenType.IDENTIFIER,
        TokenType.NEWLINE,
    ]
    
    assert token_types == expected
    
    # Check specific values
    assert tokens[1].value == "sales"
    assert tokens[2].value == "="
    json_token = tokens[3]
    assert json_token.type == TokenType.JSON_VALUE
    assert "Jan" in json_token.value
    assert "Feb" in json_token.value
    assert tokens[6].value == "chartbar"
    assert tokens[11].value == "month"
    assert tokens[16].value == "price"
