__author__ = 'alipour'
import util
import pandas as pd
import re
import itertools
# import pp
import pprocess



def func(l, k):
    res = set()
    for i in l:
        res.union(k.loc[i]['detectingTests'])
    return res

class mdata:
    def __init__(self, db_file, project_id):
        if db_file.endswith('.json'):
            raise NotImplementedError
        elif db_file.endswith('.db') or db_file.endswith('sqlite'):
            db = util.load(db_file)
	   
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
	# print self

    def op_subsumption(self):
        data = self._data
        detected = data[data['Detected'] == 1]
        g = detected.groupby(['operator'])
	# self._data = pd.DataFrame()

        k = g['testId'].agg({'detectingTests':util.union_df})
        # print k.values
        # print k.loc['ConstructorCallMutator']['detectingTests']
        # indexes = k.index
        # for i in itertools.combinations(indexes, 2):
        #     print i
        #     k.at[str(sorted(i))]['detectingTests'] = set()
        #     kk = k.loc[str(sorted(i))]['detectingTests']
        #     for j in i:
        #         kk = kk.union(k.loc[j])
        l = []
        g = []
        f = []
        h = []
        for i in itertools.combinations(k.index, 2):
            l.append(i[0])
            g.append(i[1])
            f.append(str(sorted(i)))
            h.append(k.loc[i[0]]['detectingTests'].union(k.loc[i[1]]['detectingTests']))
        kk = pd.DataFrame({'detectingTests': h}, index=f)

        # k = pd.concat([k, kk])
        #
        # kk['detectingTests'] = (k.loc[kk['op1']]['detectingTests']).union(k.loc[kk['op2']]['detectingTests'])
        #
        # print kk
        # print k
        # exit(0)
        sub_rel = set()
        not_sub_rel = set()
        for op1 in k.index:
            for op2 in k.index:
                if op1 != op2:
                    # print op1, op2
                    # print k.loc[op1]['detectingTests']
                    # print k.loc[op2]['detectingTests']
                    if k.loc[op1]['detectingTests'].issubset(k.loc[op2]['detectingTests']):
                    # n = float(len(k.loc[op1]['detectingTests'].difference(k.loc[op2]['detectingTests'])))
                    # m = float(len(k.loc[op2]['detectingTests'].difference(k.loc[op1]['detectingTests'])))
                    # print n, m
                    # if n < 0.3:
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

ppservers = ()
ncpus = 2
# job_server = pp.Server(ncpus, ppservers=ppservers)
jobs =[]


def task(file_name):
	# print '###file', file_name
	d = mdata(file_name, '')
	return d.op_subsumption()	

import sys
# '/home/alipour/papers/data-mu-issta2015/json/*.db1'
#for f in glob.glob(sys.argv[1]):
#    print f
 
#   job = job_server.submit(task, (f,),depfuncs=(func,mdata.op_subsumption,),modules=('util','pandas as pd', 're', 'itertools', 'mdata',))
#    jobs.append((f, job))

# print glob.glob(sys.argv[1])
results = pprocess.pmap(task, glob.glob(sys.argv[1]), limit=2)


for sub_res in results:
    sub_res
    sub = sub.union(sub_res['sub'])
    not_sub = not_sub.union(sub_res['not_sub'])


print 'sub'
#print sub
print 'non_sub'
#print not_sub
print 'diff'
print len(sub.difference(not_sub))
for l in  sub.difference(not_sub):
	print l

