import os, sys

def parse_test_case(lines):
    outputs = []
    maxes = {}
    lines.reverse()
    for l in lines:
        l = l.strip()
        if l.startswith('adding out-cmark'):
            filename = l.split(' ')[1]
        elif l.startswith('New max'):
            edge = l[7:14]
            count = int(l.split(' ')[3])
            if edge not in maxes:
                maxes[edge] = count
                outputs.append(filename)
    with open('unique-max.log', 'w') as output_f:
        output_f.write('\n'.join(list(set(outputs))))
with open('out-cmark/max-ct-fuzzing.log', 'r') as input_f:
    lines = input_f.readlines()
    parse_test_case(lines)
