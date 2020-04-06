# Updating value without intervention.
from multiprocessing import Process
import multiprocessing

import time

# Can be anything.
from sklearn.neighbors import KNeighborsClassifier

manager = multiprocessing.Manager()
g = manager.list()

def f1():
    while True:
        time.sleep(1)
        knc = KNeighborsClassifier()
        g.append(knc)

def f2():
    while True:
        time.sleep(0.1)
        if len(g) > 0:
            print g.pop()

def main():
    p1 = Process(target=f1)
    p2 = Process(target=f2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    main()
