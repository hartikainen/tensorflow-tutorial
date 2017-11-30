import matplotlib
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["figure.figsize"] = (20,5)

def plot_with_legend(data, figure_idx=1, show=True):
  """Plot multiple data series"""
  num_plots = len(data)
  rows, cols = np.floor(num_plots), 2

  plt.figure(figure_idx)
  for position, figure_data in enumerate(data, 1):
    plt.subplot(rows, cols, position)
    for name, series in figure_data.items():
      x, y = zip(*series)
      assert(len(x) == len(y))
      plt.plot(x, y, label=name)
    plt.legend()

  if show: plt.show()
