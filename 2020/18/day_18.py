import math
import sys

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    basic_total = 0
    advanced_total = 0
    for line in read_lines(input_file):
        basic_total += int(evaluate_expression(expression=line))
        advanced_total += int(evaluate_expression(expression=line))
    print(f"Sum of all values is {basic_total} (Basic Math)")
    print(f"Sum of all values is {advanced_total} (Advanced Math)")
    return 0


def evaluate_expression(expression: str):
    # Solve sub-expressions (parentheses) first
    while "(" in expression:
        sub_expression = get_sub_expression(expression)
        expression = expression.replace(sub_expression, evaluate_expression(sub_expression[1:-1]))

    # Get terms from expression
    split_terms = expression.rsplit(" ", maxsplit=2)
    if len(split_terms) == 1:
        return split_terms
    else:
        left, operation, right = split_terms

    # If our left or right hand terms are actually expressions, reduce them before continuing
    while len(left.split(" ")) > 1:
        left = evaluate_expression(left)
    while len(left.split(" ")) > 1:
        right = evaluate_expression(right)

    terms = [int(left), int(right)]
    if operation == "+":
        result = sum(terms)
    elif operation == "*":
        result = math.prod(terms)
    else:
        raise RuntimeError(f"Invalid operation: {operation}")

    return str(result)


def get_sub_expression(expression: str):
    index_start = expression.find("(")
    index_end = None

    if index_start < 0:
        return None

    p_count = 1
    for i, char in enumerate(expression[index_start+1:], start=index_start+1):
        if char == "(":
            p_count += 1
        elif char == ")":
            p_count -= 1
            if p_count == 0:
                index_end = i
                break

    return expression[index_start:index_end+1]


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
