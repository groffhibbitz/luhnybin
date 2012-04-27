import sys

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


def test(ints):
    #logger.debug('going to test with %s' %ints)

    double = True
    total = 0
    for x in ints:
        if double:
            temp = x * 2
            if temp > 9:
                temp = temp/10 + (temp - 10)

            total += temp

            double = False
        else:
            total += x
            double = True

        #logger.debug("s: %s total:%s" %(total, x))

    if total % 10 == 0:
        return True
    else: 
        return False


logger.debug('going to do stuff')

for line in sys.stdin:
    output = ""

    buf = []
    current_pass = False

    index = 0
    crossout = []
    for x in line:
        try:
            num = int(x)

            buf.append(num)

            current_pass = test(buf)
                
            #logger.debug("got test result of %s" %current_pass)

            if len(buf) == 14 and current_pass == True:
                # TODO use a dict not a list for crossout
                crossout.extend([index - i for i in range(0,14)])
                logger.debug('found a match: %s' %buf)
                #logger.debug('crossout is: %s' %crossout)
                

        except ValueError:
            # clear buffer only if not a space or dash
            if x == ' ' or x == '-':
                pass
            else:
                buf = []
        finally:
            if len(buf) > 16:
                buf = buf[1:]
            index += 1

        #output += x

    for idx, val in enumerate(line):
        if idx in crossout:
            output += 'X'
        else:
            output += val

    print output,
