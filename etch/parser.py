from dataclasses import dataclass, field
from typing import Any
import json

from etch.tokenizer import Token, TokenType


# Chart type mapping - supports both long and short forms
CHART_TYPES = {
    "chartbar": "bar",
    "chartpie": "pie",
    "chartline": "line",
    "chartscatter": "scatter",
    "bar": "bar",
    "pie": "pie",
    "line": "line",
    "scatter": "scatter",
    "table": "table",
}


@dataclass
class ChartCommand:
    type: str
    x_field: str
    y_field: str
    config: dict = field(default_factory=dict)


@dataclass
class ParsedProgram:
    declarations: dict[str, Any] = field(default_factory=dict)
    commands: list[ChartCommand] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)  # Global config


def parse(tokens: list[Token]) -> ParsedProgram:
    """Parse tokens into a ParsedProgram with declarations and commands."""
    program = ParsedProgram()
    i = 0
    n = len(tokens)

    while i < n:
        token = tokens[i]

        # Skip newlines
        if token.type == TokenType.NEWLINE:
            i += 1
            continue

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

        # Look for chart/command: %bar :, %pie :, %line :, %scatter :
        # or the longer forms: %chartbar :, %chartpie :, etc.
        if token.type == TokenType.PERCENT and i + 2 < n:
            next_token = tokens[i + 1]
            colon_token = tokens[i + 2]

            if (next_token.type == TokenType.IDENTIFIER and
                colon_token.type == TokenType.COLON and
                next_token.value in CHART_TYPES):
                
                chart_type_raw = next_token.value
                chart_type = CHART_TYPES[chart_type_raw]
                
                # Skip past %bar : or %chartbar :
                i += 3

                # Now parse %sales.month = %sales.price (or more complex expressions)
                # Format: PERCENT identifier DOT identifier = expression
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

                    cmd = ChartCommand(
                        type=chart_type,
                        x_field=x_full,
                        y_field=y_full,
                        config={}
                    )
                    program.commands.append(cmd)
                    
                    # Parse config lines (key: value) until next % or end
                    i += 9
                    while i < n and tokens[i].type != TokenType.NEWLINE:
                        i += 1
                    i += 1  # Skip NEWLINE
                    
                    # Continue parsing config lines
                    while i < n:
                        config_token = tokens[i]
                        
                        # Check for key: value pattern
                        if (config_token.type == TokenType.IDENTIFIER and
                            i + 2 < n and
                            tokens[i + 1].type == TokenType.COLON):
                            
                            key = config_token.value
                            value_token = tokens[i + 2]
                            
                            # Get the value
                            if value_token.type == TokenType.IDENTIFIER:
                                value = value_token.value
                            elif value_token.type == TokenType.JSON_VALUE:
                                try:
                                    value = json.loads(value_token.value)
                                except:
                                    value = value_token.value
                            else:
                                value = value_token.value
                            
                            cmd.config[key] = value
                            
                            # Skip this config line
                            i += 3
                            while i < n and tokens[i].type != TokenType.NEWLINE:
                                i += 1
                            i += 1
                        elif config_token.type == TokenType.PERCENT:
                            # Next command starting - break out
                            break
                        else:
                            # Skip unknown token
                            i += 1
                            if i < n and tokens[i].type == TokenType.NEWLINE:
                                i += 1
                    
                    # Adjust i back by 1 since we'll increment at loop end
                    i -= 1
                    continue

        i += 1

    return program
