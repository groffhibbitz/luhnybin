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
    logger.debug('going to test with %s' %ints)

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

    if total % 10 == 0:
        return True
    else: 
        return False


logger.debug('going to do stuff')

for line in sys.stdin:
    output = ""

    buf = []
    current_pass = False

    for x in line:
        try:
            num = int(x)

            buf.append(num)

            test_result = test(buf)
                
            logger.debug("got test result of %s" %test_result)

            if len(buf) == 14 and current_pass == True:
                logger.debug('found a match')

        except ValueError:
            # clear buffer
            buf = []

        output += x

        
    print output,
