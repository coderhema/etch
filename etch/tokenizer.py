from dataclasses import dataclass
from enum import Enum, auto
import re
import json


class TokenType(Enum):
    PERCENT = auto()
    COLON = auto()
    EQUALS = auto()
    DOT = auto()
    IDENTIFIER = auto()
    JSON_VALUE = auto()
    NEWLINE = auto()


@dataclass
class Token:
    type: TokenType
    value: str


def tokenize(text: str) -> list[Token]:
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        char = text[i]

        # Whitespace (skip, except for newlines)
        if char.isspace():
            if char == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n'))

                # Handle \r\n by consuming the \r
                if i + 1 < n and text[i + 1] == '\r':
                    i += 1
            i += 1
            continue

        # % symbol
        if char == '%':
            tokens.append(Token(TokenType.PERCENT, '%'))
            i += 1
            continue

        # : colon
        if char == ':':
            tokens.append(Token(TokenType.COLON, ':'))
            i += 1
            continue

        # = equals
        if char == '=':
            tokens.append(Token(TokenType.EQUALS, '='))
            i += 1
            continue

        # . dot
        if char == '.':
            tokens.append(Token(TokenType.DOT, '.'))
            i += 1
            continue

        # JSON array or object - find complete JSON
        if char == '[' or char == '{':
            # Find the matching closing bracket
            json_str, end_idx = extract_json(text, i)
            if json_str:
                try:
                    json.loads(json_str)  # Validate JSON
                    tokens.append(Token(TokenType.JSON_VALUE, json_str))
                    i = end_idx
                    continue
                except json.JSONDecodeError:
                    pass  # Not valid JSON, fall through

        # Identifier (letter, underscore, or anything that's not a special char)
        if char.isalpha() or char == '_':
            ident = ''
            while i < n and (text[i].isalnum() or text[i] == '_'):
                ident += text[i]
                i += 1
            tokens.append(Token(TokenType.IDENTIFIER, ident))
            continue

        # Unknown character - skip
        i += 1

    # Add final newline if not present
    if not tokens or tokens[-1].type != TokenType.NEWLINE:
        tokens.append(Token(TokenType.NEWLINE, ''))

    return tokens


def extract_json(text: str, start: int) -> tuple[str, int]:
    """Extract a complete JSON array or object from text starting at index."""
    open_char = text[start]
    if open_char == '[':
        close_char = ']'
    elif open_char == '{':
        close_char = '}'
    else:
        return '', start

    depth = 0
    in_string = False
    escaped = False
    json_str = ''

    for i in range(start, len(text)):
        char = text[i]

        if escaped:
            json_str += char
            escaped = False
            continue

        if char == '\\':
            json_str += char
            escaped = True
            continue

        if char == '"':
            in_string = not in_string
            json_str += char
            continue

        if not in_string:
            if char == open_char:
                depth += 1
            elif char == close_char:
                depth -= 1

        json_str += char

        if depth == 0 and not in_string and i > start:
            return json_str, i + 1

    return '', start