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
    

def allcombinations(featurset):
    raise NotImplemented



def learn_dtree(data, image_prefix):
    clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=4)
    
  #  print len(data), len(data['operator'])
    data['mf'] = data['class'] + ' ' + data['method']
    k = data.groupby(['mf'])

#    k = data.groupby(['operator'])
    f = k['isCovered'].agg({'mean': np.mean, 'len': len, 'sum':np.sum})
    ff = lambda x: x.line
    gg = lambda y: y-np.min(y)
    f
    g = k['line'].agg({'max': np.max, 'min':np.min})
    print 'g:', g
    fig = plt.figure()

    # ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')

    plt.scatter(standardize (f['mean']),f['len'])
    plt.ylabel('mutant_size')
    plt.xlabel('expected_kill (standatdize)')
#    print f[f['len'] > 25000] 
    # ax.set_xlabel('mean')
    # ax.set_ylabel('len')
    # ax.set_zlabel('sum')
    
    plt.show()

    # plt.show()
    # for m in k.groups:
    #   print m,len(k.groups[m]),
    data['op'] = pd.factorize(data['operator'])[0]
    data['m'] = pd.factorize(data['method'])[0]
    data['c'] = pd.factorize(data['class'])[0]

    # plt.show()
    # plt.close()
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


#db1 = 'data/com_lang.db'
#k = main(sys.argv[1])
#dot = learn_dtree(k, sys.argv[2])
# open(sys.argv[3], 'w').write(dot)







