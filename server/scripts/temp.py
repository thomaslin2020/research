"""
Queries arxiv API and downloads papers (the query is a parameter).
The script is intended to enrich an existing database pickle (by default db.p),
so this file will be loaded first, and then new results will be added to it.
"""

import argparse
import pickle
import random
import time
import urllib.request

import feedparser

from utils import Config, safe_pickle_dump


def encode_feedparser_dict(d):
    """
    helper function to get rid of feedparser bs with a deep copy.
    I hate when libs wrap simple things in their own classes.
    """
    if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
        return {k: encode_feedparser_dict(d[k]) for k in d.keys()}
    elif isinstance(d, list):
        return [encode_feedparser_dict(k) for k in d]
    else:
        return d


def parse_arxiv_url(url):
    """
    examples is http://arxiv.org/abs/1512.08756v2
    we want to extract the raw id and the version
    """
    ix = url.rfind('/')
    idversion = url[ix + 1:]  # extract just the id (and the version)
    parts = idversion.split('v')
    assert len(parts) == 2, 'error parsing url ' + url
    return parts[0], int(parts[1])


if __name__ == "__main__":
    search_query = 'cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML'
    max_index = 10
    results_per_iteration = 1
    # misc hardcoded variables
    base_url = 'http://export.arxiv.org/api/query?'  # base api query url
    print('Searching arXiv for %s' % (search_query,))

    num_added_total = 0
    for i in range(0, max_index, results_per_iteration):

        print("Results %i - %i" % (i, i + results_per_iteration))
        query = 'search_query=%s&sortBy=lastUpdatedDate&start=%i' % (search_query,
                                                                     i)
        with urllib.request.urlopen(base_url + query) as url:
            response = url.read()
        parse = feedparser.parse(response)
        num_added = 0
        num_skipped = 0
        for e in parse.entries:
            j = dict(e)
            print(j == dict(e))
            # extract just the raw arxiv id and version for this paper
            rawid, version = parse_arxiv_url(j['id'])
            j['_rawid'] = rawid
            j['_version'] = version
            print(j)
