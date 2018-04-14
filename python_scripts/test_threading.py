#!/usr/bin/python
from threading import Thread
import logging
import random
import time

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(threadName)-10s %(message)s',
                    )

# Set up some global variables
workers = 5
somelist = range(100)
sleeptime = 0

def test_threading(i):
    """
    Test Function with random number and calculating values
    """
    logging.info('item: {0}'.format(i))
    random_val = random.randint(1, 1000)
    calc_sum = i + random_val
    calc_mult = i * random_val
    logging.info('random: {1} sum: {2} mult: {3}'.format(
                     i,
                     random_val,
                     calc_sum,
                     calc_mult
                     )
    )
    time.sleep(sleeptime)


# Set up some threads
while somelist:
    logging.info('Spawning number of workers: {0}'.format(workers))
    for item in somelist[:workers]:
        worker = Thread(target=test_threading, args=(item,))
        worker.setDaemon(True)
        logging.info('Starting Worker for {0}'.format(item))
        worker.start()
        somelist.remove(item)
        logging.info('Removing item: {0}'.format(item))
        time.sleep(sleeptime)

for blah in somelist[:workers]:
    logging.info('join time for {0}'.format(blah))
    worker.join()

