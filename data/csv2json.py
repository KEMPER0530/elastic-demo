# coding: UTF-8
import csv
import json
import random
import sys
import argparse

INDEX = "restaurant"
TYPE = "_doc"

ARGS = sys.argv[0]

parser = argparse.ArgumentParser()
parser.add_argument('arg1')
args = parser.parse_args()


def random_string(length, seq='0123456789abcdefghijklmnopqrstuvwxyz'):
    sr = random.SystemRandom()
    return ''.join([sr.choice(seq) for i in range(length)])


with open(args.arg1, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    num = 1
    for row in reader:
        # bulk API だと Index を付けなきゃいけないけど...
        index = {'index': {'_id': random_string(16)}}
        print(json.dumps(index))
        print(json.dumps(dict(zip(header, row)), ensure_ascii=False))
        num += 1
        if 30000 <= num:
            break
