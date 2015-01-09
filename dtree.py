from sklearn import tree
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


def standardize(A):
    return (A - np.mean(A)) / np.std(A)
    



def learn_dtree(data):
    clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=4)
    data['ope'] = map(lambda s: s.replace('org.pitest.mutationtest.engine.gregor.mutators.', ''), data['mutator'])
    data['operator'] = map(lambda s: re.sub(r'experimental.RemoveSwitchMutator.*', 'experimental.RemoveSwitchMutator', s), data['ope'])
    print len(data), len(data['operator'])
   # k = data.groupby(['operator', 'class', 'method'])
    k = data.groupby(['operator'])
    f= k['isCovered'].agg({'mean': np.mean, 'len': len, 'sum':np.sum})
    fig = plt.figure()

#    ax = Axes3D(fig)
   # ax = fig.add_subplot(111, projection='3d')

    plt.scatter( f['mean'], (f['len']))
#    ax.set_xlabel('mean')
#    ax.set_ylabel('len')
#    ax.set_zlabel('sum')
    plt.show()
#    plt.show()
    #for m in k.groups:
    #    print m,len(k.groups[m]),
    data['op'] = pd.factorize(data['operator'])[0]
    data['m'] = pd.factorize(data['method'])[0]
    data['c'] = pd.factorize(data['class'])[0]
    plt.hist(data['op'])
    plt.hist(data['op'])
#    plt.show()
#    plt.close()
    x = data[['op', 'c', 'testId']].values
    y = data['isCovered'].values
    clf.fit(x,y)
    dot_data = StringIO.StringIO()
    tree.export_graphviz(clf, out_file=dot_data)
    return dot_data.getvalue()
    # plt.Image(graph.create_png())



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
    k = pd.merge(mutants, mut_coverage)
    return k


db1 = 'data/com_lang.db'
k = main(sys.argv[1])
dot = learn_dtree(k)
open(sys.argv[2], 'w').write(dot)







