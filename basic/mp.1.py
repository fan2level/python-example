from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x*x

def g(x,y):
    return x*x,y*y

if __name__ == '__main__':
    with Pool(processes=4) as pool:

        r = pool.apply(f, (10,))
        print(type(r), r)
        
        r = pool.map(f, range(10))
        print(type(r), r)

        r = pool.imap(f, [1,2,3])
        print(type(r), [x for x in r])

        r = pool.imap_unordered(f, range(10))
        print(type(r), [x for x in r])

        r = pool.starmap(g, zip(range(4), range(5,9)))
        print(type(r), [x for x in r])

        r = pool.starmap_async(g, zip(range(4), range(5,9)))
        print(type(r), r.get())

        r = pool.apply_async(f, (20,))
        print(type(r), r.get())

        r = pool.apply_async(os.getpid, ())
        print(type(r), r.get())

        r = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print(type(r), [x.get() for x in r])

        r = pool.apply_async(time.sleep, (3,))
        print(type(r))
        try:
            print(r.get(timeout=1))
        except TimeoutError as e:
            print(e)

        pool.close()
        pool.join()
    print('done')
        
            
        
