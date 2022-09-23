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
        return Number(self.func(*[n() for n in numbers]), "(" + self.rep(*numbers) + ")")


def bigroup(items, size, commutative):
    indices = set(range(len(items)))
    dup_check_table = []
    generator = combinations(indices, size) if commutative else permutations(indices, size)
    for selected in generator:
        not_selected = indices - set(selected)
        selected_result = [items[i] for i in selected]
        hash_number = "".join([str(n()) for n in selected_result])
        if hash_number not in dup_check_table:
            yield selected_result, [items[i] for i in not_selected]
            dup_check_table.append(hash_number)


class Searcher:

    def __init__(self, operations, target):
        self.target = target
        self.operations = operations
        self.group_sizes = {}
        for operator in self.operations:
            if operator.count_operands() not in self.group_sizes:
                self.group_sizes[operator.count_operands()] = []
            self.group_sizes[operator.count_operands()].append(operator)

    def __call__(self, numbers):
        for size, sub_operators in self.group_sizes.items():
            for operator in sub_operators:
                for selected, not_selected in bigroup(numbers, size, operator.is_commutative()):
                    try:
                        new_number = operator(selected)
                    except Exception as e:
                        pass

                    if len(not_selected) == 0:
                        if new_number() == self.target:
                            print(new_number.to_string())
                    else:
                        new_numbers = [new_number]
                        new_numbers.extend(not_selected)
                        self(new_numbers)


if __name__ == '__main__':

    operators = [
        Operation(2, lambda a, b: a + b, lambda a, b: a.to_string() + " + " + b.to_string(), True),
        Operation(2, lambda a, b: a - b, lambda a, b: a.to_string() + " - " + b.to_string(), False),
        Operation(2, lambda a, b: a * b, lambda a, b: a.to_string() + " x " + b.to_string(), True),
        Operation(2, lambda a, b: 0 if b == 0 else a // b, lambda a, b: a.to_string() + " / " + b.to_string(), False),
        Operation(2, lambda a, b: int(math.pow(a, b)), lambda a, b: a.to_string() + " ^ " + b.to_string(), False),
    ]

    numbers = [9, 9, 8, 6]

    searcher = Searcher(operators, 24)
    searcher([Number(n, str(n)) for n in numbers])
