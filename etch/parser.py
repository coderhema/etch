from dataclasses import dataclass, field
from typing import Any
import json

from etch.tokenizer import Token, TokenType


@dataclass
class ChartCommand:
    type: str
    x_field: str
    y_field: str


@dataclass
class ParsedProgram:
    declarations: dict[str, Any] = field(default_factory=dict)
    commands: list[ChartCommand] = field(default_factory=list)


def parse(tokens: list[Token]) -> ParsedProgram:
    """Parse tokens into a ParsedProgram with declarations and commands."""
    program = ParsedProgram()
    i = 0
    n = len(tokens)

    while i < n:
        token = tokens[i]

        # Look for variable declaration: %identifier = value
        if token.type == TokenType.PERCENT and i + 2 < n:
            next_token = tokens[i + 1]
            equals_token = tokens[i + 2]

            if (next_token.type == TokenType.IDENTIFIER and
                equals_token.type == TokenType.EQUALS):
                var_name = next_token.value
                # Get the value (could be JSON or identifier)
                value_token = tokens[i + 3]

                if value_token.type == TokenType.JSON_VALUE:
                    var_value = json.loads(value_token.value)
                elif value_token.type == TokenType.IDENTIFIER:
                    # Reference to another variable
                    var_value = value_token.value
                else:
                    var_value = value_token.value

                program.declarations[var_name] = var_value
                # Skip to after the value (find NEWLINE or end)
                i += 4
                while i < n and tokens[i].type != TokenType.NEWLINE:
                    i += 1
                i += 1  # Skip the NEWLINE
                continue

        # Look for chart command: %chartbar : %sales.month = %sales.price
        # or: %chartpie : %sales.month = %sales.price
        if token.type == TokenType.PERCENT and i + 2 < n:
            next_token = tokens[i + 1]
            colon_token = tokens[i + 2]

            if (next_token.type == TokenType.IDENTIFIER and
                colon_token.type == TokenType.COLON and
                next_token.value in ("chartbar", "chartpie")):
                
                chart_type = next_token.value  # "chartbar" or "chartpie"
                
                # This is a chart command
                # Parse: x_field = y_field
                # Format: PERCENT identifier DOT identifier EQUALS PERCENT identifier DOT identifier

                # Skip past %chartbar : or %chartpie :
                i += 3

                # Now parse %sales.month = %sales.price
                # Expect: PERCENT, IDENTIFIER, DOT, IDENTIFIER, EQUALS, PERCENT, IDENTIFIER, DOT, IDENTIFIER
                if (i + 8 < n and
                    tokens[i].type == TokenType.PERCENT and
                    tokens[i + 1].type == TokenType.IDENTIFIER and
                    tokens[i + 2].type == TokenType.DOT and
                    tokens[i + 3].type == TokenType.IDENTIFIER and
                    tokens[i + 4].type == TokenType.EQUALS and
                    tokens[i + 5].type == TokenType.PERCENT and
                    tokens[i + 6].type == TokenType.IDENTIFIER and
                    tokens[i + 7].type == TokenType.DOT and
                    tokens[i + 8].type == TokenType.IDENTIFIER):

                    x_var = tokens[i + 1].value
                    x_field = tokens[i + 3].value
                    y_var = tokens[i + 6].value
                    y_field = tokens[i + 8].value

                    x_full = f"{x_var}.{x_field}"
                    y_full = f"{y_var}.{y_field}"

                    program.commands.append(ChartCommand(
                        type="pie" if chart_type == "chartpie" else "bar",
                        x_field=x_full,
                        y_field=y_full
                    ))

                # Skip to end of line
                while i < n and tokens[i].type != TokenType.NEWLINE:
                    i += 1
                i += 1  # Skip NEWLINE
                continue

        i += 1

    return program