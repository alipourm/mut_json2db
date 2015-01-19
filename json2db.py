import json
import sqlite3
import sys
from progressbar import ProgressBar, Percentage, RotatingMarker, Bar
import psutil
import pprocess
# json_file = sys.argv[1]
# db_name = sys.argv[2]





def create_db(db_name):
    return sqlite3.connect('{0}.db'.format(db_name))


def create_tables(cursor):
    cursor.execute(''' create table mutants
                        (mutantId integer, mdesc text, class text, method text,
                        indexes text, mutator text, line integer,
                        block integer, fileName text)''')
    cursor.execute('''create table testcases
                        (testId integer, tc_name text)''')
    cursor.execute('''create table mutcoverage
                        (testId integer,
                         mutantId integer,
                         isCovered integer)
                    ''')


def load_data(json_file, cursor):
    lines = open(json_file).readlines()
    testcases= {}
    tc_n0 = 0
    widgets = ['Creating database: ', Percentage(), ' ', Bar(marker=RotatingMarker())]
    pbar = ProgressBar(widgets=widgets, maxval=len(lines)).start()

    for i in range(len(lines)):
        l = lines[i]
        line_data = json.loads(l)
        loc = line_data['mutant']['id']['location']
        mdesc = loc['mdesc']
        clazz = loc['class']
        method = loc['method']
        indexes = line_data['mutant']['id']['indexes']
        mutator = line_data['mutant']['id']['mutator']
        line = line_data['mutant']['line']
        block = line_data['mutant']['block']
        file_name = line_data['mutant']['filename']
        killing = line_data['killing']
        covered_by = line_data['coveredBy']
        for tc in covered_by:
            if tc not in testcases.keys():
                testcases[tc] = tc_n0
                cursor.execute('''insert into testcases values (?,?)''', (testcases[tc], tc,))
                tc_n0 += 1

            cursor.execute('insert into mutcoverage values (?,?,?)',
                    (testcases[tc], i, 1 if tc in killing else 0,))

        cursor.execute('insert into mutants values (?,?,?,?,?,?,?,?,?)',
            (i, mdesc, clazz, method,  indexes, mutator, line, block, file_name,))
        pbar.update(i)
    pbar.finish()


def do(db_name, json_file):
    conn = create_db(db_name)
    cursor = conn.cursor()
    create_tables(cursor)
    load_data(json_file, cursor)
    conn.commit()
    conn.close()


def do_stuff(f):
    print 'doing', j
    parts = j.split('.')
    db_name = ''.join(parts[:-1]) + '.sqlite'
    if db_name + '.db' not in glob.glob(dir_name + "*.db"):
    	try:
		do(db_name, j)	
    	except TypeError:
		print "Couldn't  finish {0}".format(db_name)



def dir_stuff(dir_name):
    import glob
    ncpu = psutil.cpu_count()/2
    print 'number of cpus we are using: {}'.format(ncpu)
    pprocess.pmap(do_stuff, glob.glob(dir_name + "*.json"), limit=ncpu)
        

dir_stuff(sys.argv[1])
