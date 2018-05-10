import os,json
import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch, helpers

def build_bulk_index(event_list, idx, idxtype):
    for ev in event_list:
        id = ev["id"]
        yield {'_op_type': 'create',
               '_index': idx,
               '_type': idxtype,
               '_id': id,
               '_source': ev}
def main():
    es_idx = "potus"
    es_type = "_doc"

    es = Elasticsearch()
    # ignore 400 cause by IndexAlreadyExistsException when creating an index
    es.indices.create(index='potus', ignore=400)

    with open("../data/twitter/100056842809511937.txt", 'r') as f:
        jlist = []
        for line in f.readlines():
            try:
                j = json.loads(line)
                jlist.append(j)
            except Exception as e:
                print(e)
                continue
        try:

            bad = 0
            for ok, result in helpers.parallel_bulk(es, build_bulk_index(jlist, es_idx, es_type)):
                if not ok:
                    bad += 1
                    print(result)
            print('bad', bad, "good", len(jlist) - bad)
        except Exception as e:
            print(e)
main()