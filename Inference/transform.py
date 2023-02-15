from collections import defaultdict
import random
import numpy as np
import time
import csv
from tqdm import tqdm
import argparse
allslices = []
class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)  
    def add_prod(self, lhs, rhs):
        prods = rhs.split(' \\ ')
        allslices.append(lhs)
        for prod in prods:
            for sp in prod.split():
                if sp not in allslices:
                    allslices.append(sp)
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def xss_add_prod(self, lhs, rhs):
        """ Add production to the grammar.
        """
        prods = rhs.split(' | ')
        allslices.append(lhs)
        for prod in prods:
            for sp in prod.split():
                if sp not in allslices:
                    allslices.append(sp)
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def get_sli_number(self, choice, slistr):
        for i in range(len(choice)):
            if choice[i]==slistr:
                return i
        return len(choice) 

    def get_ch_sli(self, slinum, choice):
        if slinum>=len(choice):
            return 0
        else:
            return choice[slinum]


def main(grammar_path, data_path):
    cfg = CFG()
    with open(grammar_path, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            bnflist = line.split(':=')
            if "xss" in grammar_path:
                cfg.xss_add_prod(bnflist[0],bnflist[1])
            else:
                cfg.add_prod(bnflist[0],bnflist[1])
    newallsli = []
    for slic in allslices:
        if slic not in newallsli:
            newallsli.append(slic)
    with open(data_path, 'r') as f:
        choicelist = [i[0].strip().split(' ') for i in csv.reader(f)]    
        choicelist=choicelist[1:]   
    for i in range(len(choicelist)):
        for j in range(len(choicelist[i])):
            choicelist[i][j]=int(choicelist[i][j]) 
    listss = []
    for j,schoice in enumerate(tqdm(choicelist)):
        global datafram
        datafram = schoice
        tmpstr = ''
        for dnum in datafram:
            sli = cfg.get_ch_sli(int(dnum),choice = newallsli)
            if sli not in cfg.prod:
                tmpstr = tmpstr + sli
        listss.append(tmpstr)
        
 

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--grammar_path')
    parser.add_argument('--data_path')
    args = parser.parse_args()
    main(args.grammar_path, args.data_path)


