import sqlite3
import pandas as pd
import sys
import matplotlib.pyplot as plt




def get_min_tests_to_cover(mut_coverage, mutants, tests):
    selected_tests = []
    selected_mutants = []
    mut_cov = mut_coverage[mut_coverage['testId'].isin(tests)]
    mut_cov = mut_cov[mut_cov['mutantid'].isin(mutants)]
    mut_cov = mut_cov[mut_cov['isCovered'] == 1]
    prev = len(mut_cov) + 1
    while set(mutants).difference(set(selected_mutants)) != set() and set(tests).difference(set(selected_tests)) != set():
        detecting_test_counts = (mut_cov['testId']).value_counts()
        max_detecting = detecting_test_counts.idxmax(axis=1)
        # print len(mut_cov[mut_cov['testId'] == max_detecting])
        cur = len(mut_cov[mut_cov['testId'] == max_detecting])
        # print max_detecting, (detecting_test_counts)
        selected_tests.append(max_detecting)
        selected_mutants += list(mut_cov[mut_cov['testId'] == max_detecting]['mutantid'])
        mut_cov = mut_cov[mut_cov['testId'] != max_detecting]
        # print "mutants len = {0}, testlen = {1}, #selected_test = {2}, selected_mutants = {3} ".format(len(mutants),
        #                                                                                                len(tests),
        #                                                                                                len(selected_tests),
        #                                                                                                len(selected_mutants))
    return selected_tests


def test_names(test_cases, testIds):
    return list(test_cases[test_cases['testId'].isin(testIds)]['tc_name'])
   
 




def load(db_file):
    conn = sqlite3.connect(db_file)
    mutants = pd.read_sql("select * from mutants", conn, index_col='mutantId')
    testcases = pd.read_sql("select * from testcases", conn, index_col='testId')
    mutcoverage = pd.read_sql("select * from mutcoverage", conn)
    conn.close()
    return {'mutants': mutants,
            'testcases': testcases,
            'mut_coverage': mutcoverage}


def main():
    db_file = sys.argv[1]
    data = load(db_file)
    tests = data['testcases']['testId']
    mut_coverage = data['mut_coverage']
    mutants = mut_coverage[mut_coverage['isCovered'] == 1]['mutantid']
    min_tests = get_min_tests_to_cover(mut_coverage, mutants, tests)
    for t in test_names(data['testcases'], min_tests):
        print t


main()
