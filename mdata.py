__author__ = 'alipour'
import util
import pandas as pd
import re






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
        data['operator'] = map(lambda s: re.sub(r'experimental.RemoveSwitchMutator.*', 'experimental.RemoveSwitchMutator', s), data['operator'])
        self._data = data
        self.num_mutants = len(_mutants)
        self.num_test = len(_tests)
        self.project_id = project_id

    def op_subsumption(self):
        data = self._data
        detected = data[data['Detected'] == 1]
        g = detected.groupby(['operator'])
        k = g['testId'].agg({'detectingTests':util.union_df})
        # print k.values
        # print k.loc['ConstructorCallMutator']['detectingTests']
        sub_rel = set()
        not_sub_rel = set()
        for op1 in k.index:
            # print op1
            for op2 in k.index:
                if op1 != op2:
                    if k.loc[op1]['detectingTests'].issubset(k.loc[op2]['detectingTests']):
                        sub_rel.add('{0} > {1}'.format(op2, op1))
                    else:
                        not_sub_rel.add('{0} > {1}'.format(op2, op1))
        return {'sub':sub_rel,
                'not_sub': not_sub_rel}




sub = set()
not_sub = set()
for f in glob.glob('/home/alipour/papers/data-mu-issta2015/json/*.db'):
    print f
    d = mdata(f, '')
    sub_res = d.op_subsumption()
    sub.union(sub_res['sub'])
    not_sub.union(sub_res['not_sub'])


print sub.difference(not_sub)

