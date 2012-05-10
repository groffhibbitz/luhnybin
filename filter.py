import sys
from sets import Set
import copy
import os
import os.path
import logging
import logging.config
import logging.handlers


#file handler
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler('log.out', maxBytes=5242880, backupCount=10)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

vals = {0:0, 1:2, 2:4, 3:6, 4:8, 5:1, 6:3, 7:5, 8:7, 9:9}

def luhn_test(ints_tuple):
    #logger.debug('going to test with %s' %ints_tuple)

    # double every other digit starting at the end..so if number is odd, we do not double first number
    double = False
    if len(ints_tuple)%2 == 0:
        double = True

    total = 0
    
    for tup in ints_tuple:
        x = tup[1]
        if double:
            total += vals[x]
            double = False
        else:
            total += x
            double = True

    if total % 10 == 0:
        #logger.debug('returning true')
        return True
    else: 
        #logger.debug('total is %s returning false' %total)
        return False

#logger.debug('going to do stuff')

def do_filter(line):
    out = list(line)

    for test_list in get_lists_to_test(line):
        if luhn_test(test_list):
            for x in test_list:
                out[x[0]] = 'X'

    return ''.join(out)

def get_lists_to_test(line):
    to_test = []

    dbuff = []

    for i, x in enumerate(line):
        if x.isdigit():
            dbuff.append((i, int(x)))
        elif x in [' ', '-']:
            continue
        else:
            length = len(dbuff)
            if length > 13:
                for i in range(13,16):
                    if i >= length:
                        continue
                    sublists = [dbuff[j:j+i+1] for j in range (0, length - i)]
                    to_test.extend(sublists)

            dbuff = []
    
    return to_test

for line in sys.stdin:
    print do_filter(line),

