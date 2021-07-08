#!/usr/bin/env python3
import numpy as np
from numpy import dot, inner
from numpy.linalg import norm
import os, sys
import time

#cos_sim = dot(a, b)/(norm(a)*norm(b))
output_dir = 'out-cmark/showmax1'
output_dir = 'out-cmark/showmax'
def peer_cos():
    edges = {}
    for f in os.listdir(output_dir):
        with open(os.path.join(output_dir, f), 'r') as input_f:
            lines = input_f.readlines()
            for l in lines:
                key, hit = l.split(' ')
                key = int(key)
                if key not in edges:
                    edges[key] = len(edges.keys())

    vectors = {}
    copy_vectors = {}
    vector_length = len(edges.keys())
    for f in os.listdir(output_dir):
        with open(os.path.join(output_dir, f), 'r') as input_f:
            lines = input_f.readlines()
            new_vector = [0] * vector_length
            for l in lines:
                key, hit = l.split(' ')
                key = int(key)
                hit = int(hit.rstrip())
                new_vector[edges[key]] = hit
            if sum(new_vector) > 40000:
                copy_vectors[f] = new_vector
                vectors[f] = list(np.add.reduceat(new_vector, np.arange(0, len(new_vector), 15)))
            
    print(vector_length, len(vectors.keys()))
    start = time.time()
    case2buckets = {}
    buckets = []
    threshold = 0.5
    n_b = 0
    with open('cos-clean.log', 'w') as output_f:
        for i, (k1, v1) in enumerate(vectors.items()):
            for j, (k2, v2) in enumerate(vectors.items()):
                if i >= j:
                    continue
                cos_sim = inner(v1, v2)/(norm(v1) * norm(v2))
                output_f.write('%s %s %.4f\n' % (k1, k2, round(cos_sim, 4)))
                if cos_sim > threshold:
                    if k1 in case2buckets and k2 in case2buckets:
                        continue
                    elif k1 in case2buckets:
                        case2buckets[k2] = case2buckets[k1]
                        buckets[case2buckets[k2]].append(k2)
                    elif k2 in case2buckets:
                        case2buckets[k1] = case2buckets[k2]
                        buckets[case2buckets[k1]].append(k1)
                    else: 
                        case2buckets[k1] = case2buckets[k2] = len(buckets)
                        buckets.append([k1, k2])

    print("-1# buckets-one:%d cases:%d" %(len(buckets), len(case2buckets)))
    threshold1 = 0.95
    with open('cos-details.log', 'w') as output_f:
        for idx in range(len(buckets)):
            case2buckets1 = {}
            buckets1 = []
            n_b1 = 0
            for i, k1 in enumerate(buckets[idx]):
                v1 = copy_vectors[k1]
                for j, k2 in enumerate(buckets[idx]):
                    if i >= j:
                        continue
                    v2 = copy_vectors[k2]
                    cos_sim = inner(v1, v2)/(norm(v1) * norm(v2))
                    if cos_sim > threshold1:
                        if k1 in case2buckets1 and k2 in case2buckets1:
                            continue
                        elif k1 in case2buckets1:
                            case2buckets1[k2] = case2buckets1[k1]
                            buckets1[case2buckets1[k2]].append(k2)
                        elif k2 in case2buckets1:
                            case2buckets1[k1] = case2buckets1[k2]
                            buckets1[case2buckets1[k1]].append(k1)
                        else: 
                            case2buckets1[k1] = case2buckets1[k2] = len(buckets1)
                            buckets1.append([k1, k2])
            print("-2# buckets-one:%d cases:%d " %(len(buckets1), len(case2buckets1)))
            output_f.write("====%d\n" % idx)
            for b in buckets:
                output_f.write(' '.join(b) + '\n')


    print('finished ', time.time() - start)
peer_cos()
