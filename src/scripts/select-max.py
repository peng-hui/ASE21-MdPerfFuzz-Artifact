#!/usr/bin/env python3
import os, sys
import numpy
import subprocess
output_dir = 'out-cmark/showmax'
app_path = './apps/cmark/cmark'

def runshowmax():
    with open('unique-max.log', 'r') as input_f:
        files = input_f.readlines()
        path_lengths = {}
        for f in files:
            result = subprocess.run(['./afl-showmax', '-a', app_path, f.rstrip()], stdout=subprocess.PIPE)
            path_lengths[f.rstrip()] = int(result.stdout.decode('utf-8').rstrip())
        values = list(path_lengths.values())
        values = sorted(values)
        with open('values', 'w') as output_f:
            output_f.write('\n'.join([str(i) for i in values]))
        mean = numpy.mean(values)
        std = numpy.std(values)
        print(mean, std)
        '''
        with open(os.path.join(output_dir, 'length'), 'w') as output_f:
            output_f.write(''.join(path_lengths))

            with open(os.path.join(output_dir, f.split('/')[-1].rstrip()), 'w') as output_f:
                output_f.write(result.stdout.decode('utf-8'))
        '''
output_sorted_dir = 'out-cmark/showmax-sorted'
def pick_hot_edges():
    results = {}
    hotblocks = {}
    for f in os.listdir(output_dir):
        with open(os.path.join(output_dir, f), 'r') as input_f:
            edges = {}
            lines = input_f.readlines()
            for l in lines:
                key, hit = l.split(' ')
                edges[key] = int(hit.rstrip())
            hits = list(edges.values())
            mean = round(numpy.mean(hits), 2)
            std = round(numpy.std(hits), 2)
            result_s = "%s all:%d:%d:%d mean:%d:%d std:%d +1std:%d:%d 2std:%d:%d 3std:%d:%d 4std:%d:%d 5std:%d:%d"\
                    %(f, sum(hits), len(hits), max(hits),  mean, len([i for i in hits if i > mean]), \
                    std, \
                    mean+std, len([i for i in hits if i > mean+std]), \
                    mean+2*std, len([i for i in hits if i > mean+2*std]), \
                    mean+3*std, len([i for i in hits if i > mean + 3*std]), \
                    mean+4*std, len([i for i in hits if i > mean + 4*std]), \
                    mean+5*std, len([i for i in hits if i > mean + 5*std]), \
                    )
            #print(result_s)
            results[result_s] = sum(hits)
            sorted_edges = sorted(edges.items(), key=lambda item: item[1])
            threshold = len([i for i in hits if i > mean + 2* std])
            hotblocks[result_s] = sorted([edge[0] for edge in sorted_edges][-threshold: ])

    sum_mean = numpy.mean(list(results.values()))
    sum_std = numpy.std(list(results.values()))
    results = {i[0]: i[1] for i in results.items() if i[1] > sum_mean +  2*sum_std}

    srcs = []
    results1 = {}
    for re in results.items():
        key = re[0]
        src = key.split(',')[1]
        if src not in srcs:
            results1[key] = re[1]
            srcs.append(src)

    results = results1
    filelist = results.keys()
    results = sorted(results.items(), key=lambda item: item[1])


    with open('analysis.log', 'w') as output_f:
        output_f.write('\n'.join([r[0] for r in results]))

    with open('hot-edges.log', 'w') as output_f:
        output_f.write('\n'.join(['-'.join(hotblocks[r[0]]) for r in results]))
    hot_edge2f = {}

    for hot in hotblocks.items():
        if hot[0] not in filelist:
            continue
        key = '-'.join(hot[1])
        if key not in hot_edge2f:
            hot_edge2f[key] = [hot[0].split(' ')[0]]
        else:
            hot_edge2f[key].append(hot[0].split(' ')[0])

    with open('hotedge2file.log', 'w') as output_f:
        for h in hot_edge2f.items():
            output_f.write("%s\t%s\n" % (h[0], ' '.join(h[1])))

pick_hot_edges()
