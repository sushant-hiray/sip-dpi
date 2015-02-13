from scapy.all import *
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

############################ Arrays for plotting graphs ##############################
first_request_bono = []
first_request_sprout = []
first_request_hs = []
first_response_sprout = []
first_response_bono = []
second_request_bono = []
second_request_sprout = []
second_request_hs = []
second_response_sprout = []
second_response_bono = []


def make_plot(location):
  fig = plt.figure()
  ax = fig.add_subplot(111)

  N = 5
  ind = np.arange(N)                # the x locations for the groups
  width = 0.2                      # the width of the bars

  data = np.array([first_request_bono,first_request_sprout,first_request_hs,first_response_sprout,first_response_bono,second_request_bono,second_request_sprout,second_request_hs,second_response_sprout,second_response_bono])
  bottom = np.vstack((np.zeros((data.shape[1],), dtype=data.dtype),
                    np.cumsum(data, axis=0)[:-1]))
  colors = ('black', 'red', 'green', 'blue', 'cyan','black', 'red', 'green', 'blue', 'cyan')
  
  for dat, col, bot in zip(data, colors, bottom):
    plt.bar(ind, dat, color=col, bottom=bot)
  
  ax.set_xlim(-width,len(ind)+width)
  ax.set_ylim(0,10)
  
  ax.set_ylabel('Per Hop Delay')
  ax.set_title('Per hop delay at various nodes')
  
  xTickMarks = [str(i*10)+' req/s' for i in range(1,6)]
  ax.set_xticks(ind+width)
  xtickNames = ax.set_xticklabels(xTickMarks)
  plt.setp(xtickNames, rotation=45, fontsize=10)

  
  # plt.show()
  pylab.savefig(location)


def parse_file():
  with open("graph_arrays","r") as f:
    for line in f:
      values = line.split(' ')
      first_request_bono.append(float(values[0]))
      first_request_sprout.append(float(values[1]))
      first_request_hs.append(float(values[2]))
      first_response_sprout.append(float(values[3]))
      first_response_bono.append(float(values[4]))
      second_request_bono.append(float(values[5]))
      second_request_sprout.append(float(values[6]))
      second_request_hs.append(float(values[7]))
      second_response_sprout.append(float(values[8]))
      second_response_bono.append(float(values[9]))
      total = 0
      for i in xrange(0,10):
        total += float(values[i])
      print "Total time = " + str(total)

parse_file()
make_plot("../Graphs/Per-Hop-Delay")
