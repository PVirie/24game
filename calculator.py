from enum import Enum
import copy
import math


class Token:
    def __init__(self):
        self.leading = None
        self.trailing = None

    def set_leading(self, token, bidirectional=True):
        self.leading = token
        if bidirectional and token is not None:
            token.set_trailing(self, False)

    def set_trailing(self, token, bidirectional=True):
        self.trailing = token
        if bidirectional and token is not None:
            token.set_leading(self, False)


class Expression(Token):
    def __init__(self, expr_str, operators):
        super().__init__()
        self.operators = operators

        f_group = []
        m_group = []
        a_group = []

        opening = 0
        prev_token = None
        i = 0
        while i < len(expr_str):
            s = 1
            c = expr_str[i]
            if c == " ":
                pass
            elif c == "(":
                token = Expression(expr_str[(i + 1):], self.operators)
                self.node = token
                token.set_leading(prev_token)
                prev_token = token
                s = token.terminal
                opening += 1
            elif c == ")":
                opening -= 1
                if opening == -1:
                    break
            elif c.isdigit():
                if prev_token is not None and isinstance(prev_token, Number):
                    prev_token.concat(float(c))
                else:
                    token = Number(float(c))
                    self.node = token
                    token.set_leading(prev_token)
                    prev_token = token
            else:
                token = self.match(expr_str[i:])
                if token is not None:
                    if token.group == Operator_group.FUNCTION:
                        f_group.append(token)
                    elif token.group == Operator_group.MULTIPLICATIVE:
                        m_group.append(token)
                    elif token.group == Operator_group.ADDICTIVE:
                        a_group.append(token)
                    token.set_leading(prev_token)
                    prev_token = token
                    s = len(token.symbol)
            i += s

        for t in f_group:
            self.node = t.operate()
        for t in m_group:
            self.node = t.operate()
        for t in a_group:
            self.node = t.operate()

        self.terminal = i + 1

    def match(self, expr_str):
        for o in self.operators:
            if o.symbol == expr_str[:len(o.symbol)]:
                return copy.deepcopy(o)

    def evaluate(self):
        return self.node.evaluate()


class Number(Token):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def concat(self, c):
        self.number = self.number * 10 + c

    def evaluate(self):
        return self.number


class Operator_type(Enum):
    PREFIX = 1
    BINARY = 2


class Operator_group(Enum):
    FUNCTION = 1
    MULTIPLICATIVE = 2
    ADDICTIVE = 3


class Operator(Token):
    def __init__(self, symbol: str, type: Operator_type, group: Operator_group, implementation):
        super().__init__()
        self.symbol = symbol
        self.type = type
        self.group = group
        self.implementation = implementation

    def operate(self):
        if self.type == Operator_type.PREFIX:
            print(self.symbol, self.trailing.evaluate(), "=", self.implementation(self.trailing.evaluate()))
            product = Number(self.implementation(self.trailing.evaluate()))
            product.set_leading(self.leading)
            if self.trailing is not None:
                product.set_trailing(self.trailing.trailing)
        elif self.type == Operator_type.BINARY:
            print(self.leading.evaluate(), self.symbol, self.trailing.evaluate(), "=", self.implementation(self.leading.evaluate(), self.trailing.evaluate()))
            product = Number(self.implementation(self.leading.evaluate(), self.trailing.evaluate()))
            if self.leading is not None:
                product.set_leading(self.leading.leading)
            if self.trailing is not None:
                product.set_trailing(self.trailing.trailing)
        return product


if __name__ == '__main__':
    operators = [
        Operator("+", Operator_type.BINARY, Operator_group.ADDICTIVE, lambda a, b: a + b),
        Operator("-", Operator_type.BINARY, Operator_group.ADDICTIVE, lambda a, b: a - b),
        Operator("x", Operator_type.BINARY, Operator_group.MULTIPLICATIVE, lambda a, b: a * b),
        Operator("/", Operator_type.BINARY, Operator_group.MULTIPLICATIVE, lambda a, b: a / b),
        Operator("sqrt", Operator_type.PREFIX, Operator_group.FUNCTION, lambda a: math.sqrt(a))
    ]

    r = Expression("1 + sqrt(3x3x( sqrt(1) - 0)) + 3x(2 + 5x(1 + 1) )", operators).evaluate()
    print(r, "#")
