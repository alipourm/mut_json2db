
from sklearn import tree, cluster
import pandas as pd
import matplotlib.pyplot as plt
import StringIO
import pydot
# from IPython.display import Image

import sqlite3
import util
import sys
import re
import numpy as np
from mpl_toolkits.mplot3d import Axes3D, axes3d
import itertools
from scipy import sparse


def standardize(A):
    return (A - np.mean(A)) / np.std(A)
    

def allcombinations(featurset):
    raise NotImplemented


def groups2csv(data, prefix):
    tags = ['function', 'operator', 'class']

    combinations = []
    for i in range(1, len(tags)+1):
        items = itertools.combinations(tags, i)
        for it in items:
            combinations.append(list(it))
    print combinations

    comb_names = map(lambda l: ''.join(map(lambda s: s[0],l)), combinations)
    tasks = zip(combinations, comb_names)
    for c in tasks:
        print c
        k = data.groupby(c[0])
        f = k['isCovered'].agg({'mean_kill': np.mean, 'number of mutants': len, 'number of killed':np.sum})
        f.to_csv(prefix + c[1] + '.csv')


def unionDF(df):
    # d = sparse.dok_matrix((1, 100000))
    # print df
    # for e in df:
    #     print e
    #     d[0, e] = 1
    # return d.tocsc()
    k = []
    for e in df:
        k.append(e)
    return str(sorted(k))

def mut_dist(m1, m2):
    print 'type:', type(m1)
    # return
    return max(m1.difference(m2), m2.difference(m1))


def meanDFs(df1, df2):
    np.union1d(df1,df2)


def precompute(mat):
    k = pd.Series()
   # nd = np.ndarray(, 3)


def identity(x):
    return x

def clustering(mut_coverage):
    killed = mut_coverage[mut_coverage['isCovered'] == 1]
    groupby = killed.groupby(['mutantId'])
    f = groupby['testId'].agg({'set': unionDF})

    # clf = cluster.AgglomerativeClustering(n_clusters=2,
    #                                               affinity=mut_dist,
    #                                               # memory=Memory(cachedir=None),
    #                                               connectivity=None,
    #                                               n_components=None,
    #                                               compute_full_tree='auto',
    #                                               linkage='average',
    #                                               pooling_func=unionDF)
    # clf.fit(f)

    # print f

    # groupby = killed.groupby(['class'])
    # f = groupby['mutantId'].apply

    g = f.groupby(['set'])
    print groupby.size()

def learn_dtree(data, csvfile):
    clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=4)
    k = data.groupby(['operator'])
   # k = data.groupby(['operator'])
    f = k['isCovered'].agg({'mean_kill': np.mean, 'number of mutants': len, 'number of killed':np.sum})
    f.to_csv(csvfile)
    fig = plt.figure()
    # ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')
    plt.scatter(standardize (f['mean']),f['sum'])
    plt.ylabel('mutant_size')
    plt.xlabel('expected_kill (standatdize)')
    # print f[f['len'] > 25000] 
    # ax.set_xlabel('mean')
    # ax.set_ylabel('len')
    # ax.set_zlabel('sum')
    
    plt.show()

    # plt.show()
    # for m in k.groups:
    #   print m,len(k.groups[m]),
    data['op'] = pd.factorize(data['operator'])[0]
    data['m'] = pd.factorize(data['method'])[0]
    HLdata['c'] = pd.factorize(data['class'])[0]

    # plt.show()
    plt.close()
    x = data[['op', 'c', 'testId']].values
    y = data['isCovered'].values
    clf.fit(x,y)
    dot_data = StringIO.StringIO()
    tree.export_graphviz(clf, out_file=dot_data)
    return dot_data.getvalue()
    # plt.Image(graph.create_png())

#raw_data['norm_pos'] = raw_data.groupby(['cm','operator']).transform(lambda x: np.sum(x[x['line'] > 0]))

def main(file_name):
    db_file = file_name
    db = util.load(db_file)
    tests = db['testcases']['testId']
    mutants = db['mutants']
    mut_coverage = db['mut_coverage']

    # mutants = mut_coverage[mut_coverage['isCovered'] == 1]['mutantid']
    # mut_coverage['operator'] = mutants.
    print mut_coverage.columns
    mut_coverage.columns = [u'testId', u'mutantId', u'isCovered']
    print mut_coverage.columns
    data = pd.merge(mutants, mut_coverage)
    data['ope'] = map(lambda s: s.replace('org.pitest.mutationtest.engine.gregor.mutators.', ''), data['mutator'])
    data['operator'] = map(lambda s: re.sub(r'experimental.RemoveSwitchMutator.*', 'experimental.RemoveSwitchMutator', s), data['ope'])
    return data

sys.argv = ['', 'data/com_lang.db', 'lang_']
db1 = 'data/com_lang.db'
db_file = sys.argv[1]
prefix = sys.argv[2]
data = main(db_file)
data['function'] = data['class'] + ' ' + data['method']
# groups2csv(data, prefix)
# dot = learn_dtree(data, prefix)
# open(prefix + '.dot', 'w').write(dot)

clustering(data)






