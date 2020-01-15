def push(obj, l, depth):
    while depth:
        l = l[-1]
        depth -= 1

    l.append(obj)


def parse_parentheses(s):
    groups = []
    depth = 0

    try:
        for char in s:
            if char == '(':
                push([], groups, depth)
                depth += 1
            elif char == ')':
                depth -= 1
            else:
                push(char, groups, depth)
    except IndexError:
        raise ValueError('Parentheses mismatch')

    if depth > 0:
        raise ValueError('Parentheses mismatch')
    else:
        return groups

print(parse_parentheses('ai feow f(b(cd)f)')) # ['a', ['b', ['c', 'd'], 'f']]
