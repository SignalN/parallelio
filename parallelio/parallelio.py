
def pread(*paths):
    print("Reading", ' '.join(paths))
    #print("Opening in parallel: ", *paths)
    files = [open(path, 'r') for path in paths]
    for t in zip(*files):
        clean = lambda line: line.strip()
        yield tuple(map(clean, t))

def pwrite(p_iter, path):
    print("Writing to", path)
    with open(path, 'w+') as f:
        f.write('\n'.join(map(str, p_iter)))
    return path

def pinsert(fn, p_iter, **kwargs):
    for t in p_iter:
        for i in fn(*t, **kwargs):
            yield i

def papply(fn, p_iter, **kwargs):
    for t in p_iter:
        yield fn(*t, **kwargs)

def pfilter(fn, p_iter, **kwargs):
    for t in p_iter:
        if fn(*t, **kwargs):
            yield t

from os.path import exists, commonprefix

def pio(fn, *ipaths, path=None, insert_fn=None, filter_fn=None, **kwargs):
    if path.startswith('.'):
        path = commonprefix(ipaths) + path
    p = pread(*ipaths)
    p = pinsert(insert_fn, p, **kwargs)
    p = papply(fn, p, **kwargs)
    p = pfilter(filter_fn, p, **kwargs)
    return write(p, path)
