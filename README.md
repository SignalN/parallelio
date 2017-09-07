# Parallel I/O

**Parallel I/O** is a library for easily reading from and writing to parallel data files in Python.

***What are parallel data files?***

Parallel data files are two or more files that have the same number of lines, like columns in a spreadsheet.  Their rows correspond to each other.

With Parallel I/O, data from the same row across multiple files can be read as input to functions, and the output of the functions can be written to new files.

It is especially intended for text data, for which formats like CSV and TSV are not ideal.

```
pip install parallelio
```

```
from parallelio.parallelio import pread, papply, pwrite

a_b = pread("a.txt", "b.txt")
c = papply(magic_fn, a_b)
pwrite(c, "c.txt")
```

`pread`, `pwrite` and `papply` do not change the number of lines, but `pinsert` and `pfilter` do.

### pread
`pread` reads in a variable number of files, which must have the same number of lines.
```
a_b = pread("a.txt", "b.txt")
```
It returns an iterator over tuples of corresponding lines.

## papply
`papply` applies a function to the items in the iterator.
```
c = papply(magic_fn, a_b)
```
`fn` should expect an argument for each item in the iterator's tuples, for example `lambda a, b: a + ' ' + b
`, where `a` is a line in a.txt and be is the corresponding line in b.txt.  It can also take arbitrary keyword arguments.  It should return a single value.

### pwrite
`pwrite` writes lines to a file.
```
pwrite(c, "c.txt")
```
It expects an iterator of values, and writes out one value per line.  It returns only the path to the newly written file.

## pinsert
`pinsert` turns one line into multiple lines.
```
c = pinsert(insert_fn, c)
```
`fn` should have an argument for each item in the iterator's tuples.  It can also take arbitrary keyword arguments.  It should return a tuple of values.  The tuple can be empty, and if it is empty or it does not contain the original value then it is equivalent to filtering out the line.

`pinsert` returns a new iterator.

## pfilter
`pfilter` is a way to remove certain lines.
```
c = pfilter(fn, c)
```
`fn` should have an argument for item in the iterator's tuples.  It can also take arbitrary keyword arguments.  Similar to built-in `filter`, only those items in the iterator for which `fn` returns something that evaluates to `True` are preserved.

`pfilter` returns a new iterator.

### pio
`pio` is simply all operations in one - `pread`, `pinsert`, `papply`, `pfilter` and `pwrite`.

```
c_txt = pio(fn, "a.txt", "b.txt", insert_fn=fx, filter_fn=fy, path="c.txt")
```

If `path` is an extension, it will add it to the common prefix.  For example, if the input files are `"data/fifa/matches.location.txt"` and `"data/fifa/matches.date.txt"`, and path is `".weather.txt"`, the output will written to
`"data/fifa/matches.weather.txt"`.

## Keyword arguments

`pinsert`, `papply`, `pfilter` and `pio` support keyword arguments that will be passed on to the functions `fn`.
