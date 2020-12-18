import math
import sys
from enum import Enum
from typing import List

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


SUM = "+"
PRODUCT = "*"


def main(input_file: str) -> int:
    basic_total = 0
    advanced_total = 0
    for line in read_lines(input_file):
        basic_total += int(evaluate_expression(expression=line, advanced=False))
        advanced_total += int(evaluate_expression(expression=line, advanced=True))
    print(f"Sum of all values is {basic_total} (Basic Math)")
    print(f"Sum of all values is {advanced_total} (Advanced Math)")
    return 0


def evaluate_expression(expression: str, advanced: bool) -> str:
    # Solve sub-expressions (parentheses) first
    while "(" in expression:
        sub_expression = get_sub_expression(expression)
        expression = expression.replace(sub_expression, evaluate_expression(sub_expression[1:-1], advanced=advanced))

    # If the expression is reduced to a single term, it is solved.
    if is_solved(expression) is True:
        return expression

    # Get terms from expression
    if advanced is True:
        # Advanced: solve addition before multiplication
        left, operation, right = get_advanced_terms(expression=expression)
    else:
        # Basic: solve left to right
        left, operation, right = get_basic_terms(expression=expression)

    # If our left or right hand terms are actually expressions, reduce them before continuing
    while is_solved(expression=left) is False:
        left = evaluate_expression(left, advanced=advanced)
    while is_solved(expression=right) is False:
        right = evaluate_expression(right, advanced=advanced)

    result = solve_operation(left=left, right=right, operation=operation)
    return result


def is_solved(expression: str) -> bool:
    """ If an expression has no spaces, it has been reduced to a single term and is considered solved. """
    if len(expression.split(" ")) == 1:
        return True
    else:
        return False


def get_sub_expression(expression: str) -> str:
    """ Return a sub-expression within an expression. """
    index_start = expression.find("(")
    index_end = None

    if index_start < 0:
        raise RuntimeError(f"No parentheses in expression: {expression}")

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


def get_basic_terms(expression: str) -> List[str]:
    """ Split by the first operand on the right-hand side. """
    return expression.rsplit(" ", maxsplit=2)


def get_advanced_terms(expression: str) -> List[str]:
    """ Split by multiplication first, then addition. """
    for operation in [PRODUCT, SUM]:
        if operation in expression:
            left, right = [s.strip() for s in expression.rsplit(operation, maxsplit=1)]
            return [left, operation, right]


def solve_operation(left: str, right: str, operation: str) -> str:
    """ Operate on two terms. """
    terms = [int(left), int(right)]
    if operation == SUM:
        return str(sum(terms))
    elif operation == PRODUCT:
        return str(math.prod(terms))
    else:
        raise RuntimeError(f"Invalid operation: {operation}")


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
