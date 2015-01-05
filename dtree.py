from sklearn import tree
import pandas as pd
import matplotlib.pyplot as plt
import StringIO
import pydot
from IPython.display import Image

import sqlite3
import util
import sys



def main():
    db_file = sys.argv[1]
    db = util.load(db_file)
    tests = db['testcases']['testId']
    mutants = db['mutants']
    mut_coverage = db['mut_coverage']
    # mutants = mut_coverage[mut_coverage['isCovered'] == 1]['mutantid']
    mut_coverage['operator'] = mutants.
    mut_coverage['mutantid']




def read_test_mut_vec(db):



