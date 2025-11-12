import random, time

def mergesort(a):
    if len(a) <= 1: return a
    m = len(a)//2
    left = mergesort(a[:m]); right = mergesort(a[m:])
    return merge(left, right)

def merge(a,b):
    i=j=0; out=[]
    while i<len(a) and j<len(b):
        if a[i] <= b[j]: out.append(a[i]); i+=1
        else: out.append(b[j]); j+=1
    out.extend(a[i:]); out.extend(b[j:]); return out

def quicksort(a):
    if len(a) <= 1: return a
    p = a[len(a)//2]
    return quicksort([x for x in a if x < p]) + [x for x in a if x==p] + quicksort([x for x in a if x > p])

def time_sort(f, n=5000, trials=1):
    best = 1e9
    for _ in range(trials):
        data = [random.randint(0, n) for _ in range(n)]
        t0 = time.perf_counter(); f(data); best = min(best, time.perf_counter()-t0)
    return best
