__author__ = 'alipour'
import util
import pandas as pd
import re
import itertools
import pprocess

import matplotlib.pyplot as plt


def func(l, k):
    res = []
    for i in l:
        res.append(k.loc[i]['testId'])
        print k.loc[i]
    return frozenset(res)

class mdata:
    def __init__(self, db_file, project_id):
        if db_file.endswith('.json'):
            raise NotImplementedError
        elif db_file.endswith('.db') or db_file.endswith('sqlite'):
            db = util.load(db_file)
        else:
            raise Exception
	   
        _tests = db['testcases']['testId']
        _mutants = db['mutants']
        _mut_coverage = db['mut_coverage']

        _mut_coverage.columns = [u'testId', u'mutantId', u'Detected']
        data = pd.merge(_mutants, _mut_coverage)
        data['operator'] = map(lambda s: s.replace('org.pitest.mutationtest.engine.gregor.mutators.', ''), data['mutator'])
        data['operator'] = map(lambda s: re.sub(r'experimental.RemoveSwitchMutator.+', 'experimental.RemoveSwitchMutator', s), data['operator'])
	data['operator'] = map(lambda s: re.sub(r'RemoveConditionalMutator_.*', 'RemoveConditionalMutator', s), data['operator'])
                
	self._data = data
        self.num_mutants = len(_mutants)
        self.num_test = len(_tests)
        self.project_id = project_id
	df = data
	print (df.values.nbytes + df.index.nbytes + df.columns.nbytes)/1024, self.num_mutants, self.num_test, db_file	

    def equivalent_mutants(self):
        """ Not Finished """
        data = self._data
        detected = data[data['Detected'] == 1]
        #detected['testId'].apply(lambda n: 't'+ str(n))
        #detected['mutantId'].apply(lambda n: 'm'+ str(n))

        g = detected.groupby("mutantId")
        k = g['testId'].agg({'detectingTests':util.union_df})
        k['index'] = range(len(k))
        k.set_index(k['index'])
        k['dt'] = k['detectingTests'].apply(lambda s: str(s))
        k['test-size'] = k['detectingTests'].apply(lambda s: len(s))
        g = k.groupby('dt')
        print g.size()        
#        print k
        return k


    def op_subsumption(self):
        data = self._data
        detected = data[data['Detected'] == 1]
        g = detected.groupby(['operator'])
        k = g['testId'].agg({'detectingTests':util.union_df})
        not_sub_rel = set()
        sub_rel = set()
        for op1 in k.index:
            for op2 in k.index:
                if op1 != op2:
                    if k.loc[op1]['detectingTests'].issubset(k.loc[op2]['detectingTests']):
                        sub_rel.add('{0} > {1}'.format(op2, op1))
                    else:
                        not_sub_rel.add('{0} > {1}'.format(op2, op1))
        # print sub_rel
        return {'sub':sub_rel,
                'not_sub': not_sub_rel}




sub = set()
not_sub = set()
import glob
c = 0



def task_sub(file_name):
	print '###file', file_name
	d = mdata(file_name, '')
	return  d.op_subsumption()	#d.equivalent_mutants() #d.op_subsumption()	


def task_eq_mut(file_name):
	print '###file', file_name
	d = mdata(file_name, '')
	return  d.equivalent_mutants()



#results = map(task, glob.glob(sys.argv[1]))


def report_sub(results):
    for sub_res in results:
        sub = sub.union(sub_res['sub'])
        not_sub = not_sub.union(sub_res['not_sub'])
        print 'sub'#print sub
        print 'non_sub'
        print not_sub
        print 'diff'
        print len(sub.difference(not_sub))
        for l in  sub.difference(not_sub):
            print l

def report_eq(results):
    df = pd.concat(results)
    print df

import sys

if sys.argv[1] == 'sub':
    func = task_sub
    report = report_sub 
elif sys.argv[1] == 'eq':
    func = task_eq_mut
    report = report_eq

if len(sys.argv) > 3:
    results = pprocess.pmap(func, glob.glob(sys.argv[2]), limit=8)
else:
    results = map(func, glob.glob(sys.argv[2]))

report(results)
