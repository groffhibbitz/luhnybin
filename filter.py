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


def luhn_test(ints_tuple):
    #logger.debug('going to test with %s' %ints_tuple)

    # double every other digit starting at the end..so if number is odd, we do not double first number
    double = False
    if len(ints_tuple)%2 == 0:
        double = True
    else: 
        double = False

    total = 0
    
    for idx, tup in enumerate(ints_tuple):
        x = tup[1]
        if double:
            temp = x * 2
            if temp > 9:
                temp = temp/10 + (temp - 10)

            total += temp

            double = False
        else:
            total += x
            double = True


        if idx == 13:
            if total % 10 == 0:
                pass

    if total % 10 == 0:
        #logger.debug('returning true')
        return True
    else: 
        #logger.debug('total is %s returning false' %total)
        return False


#logger.debug('going to do stuff')

def do_filter(line):
    out = list(line)

    to_test = get_lists_to_test(line)
    
    for test_list in to_test:
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
            if len(dbuff) > 13:
                for i in range(13,16):
                    num_sublists = len(dbuff) - i 

                    sublists = [dbuff[j:j+i+1] for j in range (0, num_sublists)]
                          
                    #logger.debug('got sublists: %s' %sublists)

                    to_test.extend(sublists)

            dbuff = []
    
    #logger.debug('to_test is %s' %to_test)

    return to_test

for line in sys.stdin:
    output = do_filter(line)

    print output,
