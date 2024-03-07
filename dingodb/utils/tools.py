from typing import Any, cast

from dingodb.utils.parser import Comparator, Comparison, Operation, Operator, get_parser

DEFAULT_PARSER = get_parser()

value_type_map = {
    int: "INT64",
    str: "STRING",
    float: "DOUBLE",
    bool: "BOOL",
    "unknown": "STRING",
}


def parser_json(actual):
    ori_dict = {}
    for key, value in actual.__dict__.items():
        if key == "operator" or key == "comparator":
            ori_dict["type"] = key
            ori_dict[key] = value.__dict__["_value_"]
        elif key == "arguments":
            ori_dict["arguments"] = []
            for arguments_value in value:
                ori_dict["arguments"].append(parser_json(arguments_value))
        elif key == "value":
            ori_dict[key] = value
            ori_dict["value_type"] = value_type_map.get(type(value), "STRING")
        else:
            ori_dict[key] = value
    return ori_dict


def auto_value_type(value):
    return value_type_map.get(type(value), "STRING")


def auto_expr_type(value):
    if value is None:
        return {}
    elif value.__class__.__name__ == 'Operation' or value.__class__.__name__ == 'Comparison':
        return parser_json(value)
    elif isinstance(value, str):
        return parser_json(DEFAULT_PARSER.parse(value))
    else:
        raise Exception(f"expr type must in [str,Operation, Comparison]")


def convert_dict_to_expr(d):
    conditions = []
    for key, value in d.items():
        condition = f'eq("{key}", "{value}")' if isinstance(value, str) else  f'eq("{key}", {value})'
        conditions.append(condition)
        
    return f'and({", ".join(conditions)})' if len(conditions)  > 1 else conditions[0]

if __name__ == "__main__":
    print(auto_value_type(1))
    print(auto_value_type("1"))
    print(auto_value_type(1.1))
    print(auto_value_type(True))
    print(auto_expr_type(f'eq("x", {100})'))
    print(
        auto_expr_type(
            'and(or(eq("a", "b"), eq("a", "c"), eq("a", "d")), not(eq("z", "foo")))'
        )
    )
    op = 'and(or(eq("a", "b"), eq("a", "c"), eq("a", "d")), not(eq("z", "foo")))'
    actual = DEFAULT_PARSER.parse(op)
    print(auto_expr_type(actual))
    op = f'eq("x", {100})'
    actual = DEFAULT_PARSER.parse(op)
    print(auto_expr_type(actual))
