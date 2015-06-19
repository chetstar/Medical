import multiprocessing as mp

def chunk_eater(i):
    name = mp.current_process().name
    print('{0} Starting').format(name)
    print('{0} ate {1} Yummy Chunks!').format(name,i)
    print('{0} Finishing').format(name)
    return

if __name__ == '__main__':
    jobs = []
    for i in range(6):
        p = mp.Process(target=chunk_eater, args = (i,))
        jobs.append(p)
        p.start()
