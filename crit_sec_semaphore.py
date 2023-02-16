#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:27:37 2023

@author: prpa
"""
import random
import time
from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import BoundedSemaphore

N = 8


def task(common, tid, semaforo):
    a = 0
    for i in range(10):
        print(f'{tid}−{i}: Non−critical Section')
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')
        
        #Para simular que hay más operaciones
        time.sleep(random.random())
        
        #preprotocolo
        semaforo.acquire()
        
        print(f'{tid}−{i}: Critical section', flush=True)
        v = common.value + 1
        print(f'{tid}−{i}: Inside critical section', flush=True)
        
        time.sleep(random.random())
        
        common.value = v
        print(f'{tid}−{i}: End of critical section', flush=True)
        
        #post_protocolo
        semaforo.release()
        
def main():
    lp = []
    common = Value('i', 0)
    
    semaforo = BoundedSemaphore(1) #Solo permitimos a un proceso el acceso a la saección crítica de foprma simultánea
    
    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, semaforo)))
    print (f"Valor inicial del contador {common.value}", flush=True)
    for p in lp:
        p.start()
    for p in lp:
        p.join()
        
    print (f"Valor final del contador {common.value}", flush=True)
    print ("fin", flush=True)
 
if __name__ == "__main__":
    main()