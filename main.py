from itertools import combinations, permutations
import math


class Number:
    def __init__(self, number, rep):
        self.number = number
        self.rep = rep

    def __call__(self):
        return self.number

    def to_string(self):
        return self.rep


class Operation:

    def __init__(self, num_operands, func, rep, commutative=True):
        self.num_operands = num_operands
        self.func = func
        self.rep = rep
        self.commutative = commutative

    def count_operands(self):
        return self.num_operands

    def is_commutative(self):
        return self.commutative

    def __call__(self, numbers):
        value = self.func(*[n() for n in numbers])
        if abs(value - int(value)) > 1e-4:
            raise ValueError("Not an integer")
        return Number(int(value), "(" + self.rep(*numbers) + ")")


def bigroup(items, size, commutative):
    indices = set(range(len(items)))
    generator = combinations(indices, size) if commutative else permutations(indices, size)
    for selected in generator:
        not_selected = indices - set(selected)
        selected_result = [items[i] for i in selected]
        yield selected_result, [items[i] for i in not_selected]


class Searcher:

    def __init__(self, operations, target):
        self.target = target
        self.operations = operations
        self.group_sizes = {}
        for operator in self.operations:
            if operator.count_operands() not in self.group_sizes:
                self.group_sizes[operator.count_operands()] = []
            self.group_sizes[operator.count_operands()].append(operator)

        self.dup_check_table = []

    def __call__(self, numbers):
        for size, sub_operators in self.group_sizes.items():
            for operator in sub_operators:
                for selected, not_selected in bigroup(numbers, size, operator.is_commutative()):
                    try:
                        new_number = operator(selected)
                    except Exception as e:
                        continue

                    if len(not_selected) == 0:
                        if new_number() == self.target:
                            print(new_number.to_string())
                    else:
                        new_numbers = [new_number]
                        new_numbers.extend(not_selected)

                        # sorted([n() for n in new_numbers])
                        # hash_number = "".join([str(n()) for n in new_numbers])
                        # if hash_number not in self.dup_check_table:
                        # self.dup_check_table.append(hash_number)
                        self(new_numbers)


def v_sqrt(a):
    if a > 1:
        return math.sqrt(a)
    raise ValueError("Sqrt less than 1")


def v_div(a, b):
    if b == 0:
        raise ValueError("Div by zero")
    return a / b


if __name__ == '__main__':

    operators = [
        Operation(1, v_sqrt, lambda a: "r(" + a.to_string() + ")", False),
        Operation(2, lambda a, b: a + b, lambda a, b: a.to_string() + " + " + b.to_string(), True),
        Operation(2, lambda a, b: a - b, lambda a, b: a.to_string() + " - " + b.to_string(), False),
        Operation(2, lambda a, b: a * b, lambda a, b: a.to_string() + " x " + b.to_string(), True),
        Operation(2, v_div, lambda a, b: a.to_string() + " / " + b.to_string(), False),
        Operation(2, lambda a, b: math.pow(a, b), lambda a, b: a.to_string() + " ^ " + b.to_string(), False)
    ]

    numbers = [8, 4, 2, 6, 5]

    searcher = Searcher(operators, 497)
    searcher([Number(n, str(n)) for n in numbers])
