import sys
import mdata
import glob
import pprocess
import pp
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



def task_sample_muscore(file_name):
	d = mdata.mdata(file_name)
	if d.num_mutants >= 1000 and d.num_test >= 1:
		total = 0.0
		for i in range(30):
			data = d.get_data()
			sample = d.sample(100)
			total += d.mutation_score(sample)
			
		return d.mutation_score(), total/30.
	
	else:
		return -1





def report_sub(results):
    for sub_res in results:
        sub = sub.union(sub_res['sub'])
        not_sub = not_sub.union(sub_res['not_sub'])
    print len(sub.difference(not_sub))
    for l in  sub.difference(not_sub):
            print l

def report_eq(results):
    df = pd.concat(results)
    print df


def printIt(s):
    print "original, sampled"
    for n in s:
        if n != -1:
	     print '{0}, {1}'.format(n[0], n[1])





if sys.argv[1] == 'sub':
    func = task_sub
    report = report_sub 
elif sys.argv[1] == 'eq':
    func = task_eq_mut
    report = report_eq
elif sys.argv[1] == 'muscore':
    func = task_sample_muscore
    report = printIt

if len(sys.argv) > 3:
    results = pprocess.pmap(func, glob.glob(sys.argv[2]), limit=8)
else:
    results = map(func, glob.glob(sys.argv[2]))

report(results)
