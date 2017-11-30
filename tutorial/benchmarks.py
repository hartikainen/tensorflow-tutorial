import timeit
from functools import partial

import numpy as np

DEFAULT_REPEAT = 5
DEFAULT_NUMBER = 5
DEFAULT_TEST_SIZES = tuple(10 * 2**x for x in range(1, 8))
WARMUP_REPEAT = 5
WARMUP_NUMBER = 5

class TableTestTimer(object):
  def __init__(self, timeit_fn):
    self.timeit_fn = timeit_fn

  def body(self):
    raise NotImplementedError()

  def repeat(self,
             table_sizes=DEFAULT_TEST_SIZES,
             repeat=DEFAULT_REPEAT,
             number=DEFAULT_NUMBER,
             verbose=False):
    if verbose:
      args_str = "\n".join([
        "{}={}".format(name, val) for name, val in zip(
            ("table_sizes", "repeat", "number", "verbose"),
            (table_sizes, repeat, number, verbose))
      ])
      print(self.__class__.__name__)
      print("{}\n".format(args_str))
      print("Results:")

    results = []
    for table_size in table_sizes:
      if verbose:
          print("{}".format(table_size), end=": ")

      times = self.body(table_size,
                        repeat=repeat,
                        number=number,
                        verbose=verbose)

      # Why min? See, for example, the note in:
      # https://docs.python.org/2/library/timeit.html#timeit.Timer.repeat
      average_min_time = min(times) / number
      results.append((table_size, average_min_time))

      if verbose:
        print("{:.5f}".format(average_min_time), end="; ")

    if verbose: print()

    return results

class TableTestPy(TableTestTimer):
  def body(self,
           table_size,
           repeat=DEFAULT_REPEAT,
           number=DEFAULT_NUMBER,
           verbose=False,
           warmup=False):
    timer = timeit.Timer(
      setup=('from numpy.random import rand;'
             'table = rand(table_size, table_size).tolist();'),
      stmt='timeit_fn(table)',
      globals={"table_size": table_size, "timeit_fn": self.timeit_fn})
    if warmup:
      warmup_times = timer.repeat(repeat=WARMUP_REPEAT, number=WARMUP_NUMBER)
    times = timer.repeat(repeat=repeat, number=number)

    return times

class TableTestNp(TableTestTimer):
  def body(self,
           table_size,
           repeat=DEFAULT_REPEAT,
           number=DEFAULT_NUMBER,
           verbose=False,
           warmup=False):
    timer = timeit.Timer(
      setup=('from numpy.random import rand;'
             'table = rand(table_size, table_size);'),
      stmt='timeit_fn(table)',
      globals={"table_size": table_size, "timeit_fn": self.timeit_fn})
    if warmup:
      warmup_times = timer.repeat(repeat=WARMUP_REPEAT, number=WARMUP_NUMBER)
    times = timer.repeat(repeat=repeat, number=number)

    return times

class TableTestTf(TableTestTimer):
  def body(self,
           table_size,
           repeat=DEFAULT_REPEAT,
           number=DEFAULT_NUMBER,
           verbose=False,
           warmup=False):

    timer = timeit.Timer(
      setup=('from numpy.random import rand;'
             'import tensorflow as tf;'
             'table = rand(table_size, table_size);'
             'ops = timeit_fn(table);'
             'session = tf.Session();'
             'session.run(tf.global_variables_initializer());'),
      stmt='session.run(ops)',
      globals={"table_size": table_size, "timeit_fn": self.timeit_fn})
    if warmup:
      warmup_times = timer.repeat(repeat=WARMUP_REPEAT, number=WARMUP_NUMBER)
    times = timer.repeat(repeat=repeat, number=number)

    return times

DEFAULT_MAT_POW_SIZES = tuple(2**x for x in range(6, 14))
def mat_pow_data_generator(shape=(2**6, 2**6), dtype=np.float32):
  """Generate uniformly random data between -1...1

  Arguments:
  ----------
  shape (int): number of data points to generate.
  dtype (int): type of the data to generate.
  """
  data = np.random.uniform(-1, 1, size=shape) - 0.5
  return data.astype(dtype)

class MatPowTestTimer(object):
  def __init__(self, timeit_fn, data_generator=mat_pow_data_generator):
    self.timeit_fn = timeit_fn
    self.data_generator = data_generator

  def body(self):
    raise NotImplementedError()

  def repeat(self,
             data_sizes=DEFAULT_MAT_POW_SIZES,
             repeat=DEFAULT_REPEAT,
             number=DEFAULT_NUMBER,
             verbose=False):
    if verbose:
      args_str = "\n".join([
        "{}={}".format(name, val) for name, val in zip(
            ("data_sizes", "repeat", "number", "verbose"),
            (data_sizes, repeat, number, verbose))
      ])
      print(self.__class__.__name__)
      print("{}\n".format(args_str))
      print("Results:")

    results = []
    for data_size in data_sizes:
      if verbose:
          print("{}".format(data_size), end=": ")

      times = self.body(data_size,
                        repeat=repeat,
                        number=number,
                        verbose=verbose)

      # Why min? See, for example, the note in:
      # https://docs.python.org/2/library/timeit.html#timeit.Timer.repeat
      average_min_time = min(times) / number
      results.append((data_size, average_min_time))

      if verbose:
        print("{:.5f}".format(average_min_time), end="; ")

    if verbose: print()

    return results

class MatPowTestNp(MatPowTestTimer):
  def body(self,
           data_size,
           repeat=DEFAULT_REPEAT,
           number=DEFAULT_NUMBER,
           verbose=False,
           warmup=False):

    data_shape = (data_size, data_size)
    timer = timeit.Timer(
      setup='data = data_generator(data_shape);',
      stmt='timeit_fn(data);',
      globals={"data_generator": self.data_generator,
               "timeit_fn": self.timeit_fn,
               "data_shape": data_shape})
    if warmup:
      warmup_times = timer.repeat(repeat=WARMUP_REPEAT, number=WARMUP_NUMBER)
    times = timer.repeat(repeat=repeat, number=number)

    return times



    return times
