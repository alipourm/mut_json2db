import sys
import mdata
import glob
import pprocess
sub = set()
not_sub = set()

def task_sub(file_name):
	print '###file', file_name
	d = mdata.mdata(file_name)
	return  d.op_subsumption()	#d.equivalent_mutants() #d.op_subsumption()	


def task_eq_mut(file_name):
	print '###file', file_name
	d = mdata.mdata(file_name)
	return  d.equivalent_mutants()



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
