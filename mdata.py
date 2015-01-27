__author__ = 'alipour'
import util
import pandas as pd
import re
import pprocess




def func(l, k):
    res = []
    for i in l:
        res.append(k.loc[i]['testId'])
        print k.loc[i]
    return frozenset(res)

class mdata:
    def __init__(self, db_file):
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
                
	self.data = data
        self.num_mutants = len(_mutants)
        self.num_test = len(_tests)
	df = data
#        print 'data loaded from {0}, into ~ {1}KB memory. Numeber of mutants: {2}, number of tests:{3}'.format( db_file, (df.values.nbytes + df.index.nbytes + df.columns.nbytes)/1024, self.num_mutants, self.num_test)
    

    def get_data(self):
        return self.data


    def equivalent_mutants(self):
        data = self.data
        detected = data[data['Detected'] == 1]
        g = detected.groupby("mutantId")
        k = g['testId'].agg({'detectingTests':util.union_df})
        k['index'] = range(len(k))
        k.set_index(k['index'])
        k['dt'] = k['detectingTests'].apply(lambda s: str(s))
        k['test-size'] = k['detectingTests'].apply(lambda s: len(s))
        g = k.groupby('dt')
        print g.size()        

        return k


    def op_subsumption(self):
        data = self.data
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

        return {'sub':sub_rel,
                'not_sub': not_sub_rel}


    def sample(self, n):
        import random
        data = self.data
        if len(data.index) < n:
            return data
        else:
            sample_data = data.loc[random.sample(data.index, n)]
            return sample_data


    def mutation_score(self, data=None):
        if data is  None:
            data = self.data
        size_mutants = len(data.index)
        detected_mutatnts = len(data[data['Detected'] == 1].index)
        if size_mutants!= 0: 
            return  float(detected_mutatnts)/size_mutants
        else:
            return 0.
        

        


