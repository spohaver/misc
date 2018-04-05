#!/bin/python
from Queue import Queue
from threading import Thread
import logging
import random
import time

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s %(message)s)',
                    )

# Set up some global variables
thread_max = 5
test_queue = Queue()

def test_threading(i, q):
    """
    Test function with random number and calculations
    while True seems to be the only way this works with a queue.
    tried using while not q.empty but it doesn't work
    """
    while True:
        item = q.get()
        print item
        logging.info('item: {0}'.format(item))
        logging.info('queue size: {0}'.format(q.qsize()))
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
        time.sleep(2)
        q.task_done()


# Set up some threads
for i in range(thread_max):
    worker = Thread(target=test_threading, args=(i, test_queue,))
    worker.setDaemon(True)
    logging.info('Starting Worker')
    worker.start()

for randval in range(1,35):
    logging.info('Putting {0} into queue'.format(randval))
    test_queue.put(randval)

# Now wait for the queue to be empty
print '*** Main thread waiting'
test_queue.join()
print '*** Done'
