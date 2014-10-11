from data import *
from test import *


def make_plot(location):
  fig = plt.figure()
  ax = fig.add_subplot(111)

  N = 5 # For throughput
  ind = np.arange(N)                # the x locations for the groups
  width = 0.2                      # the width of the bars

  # the bars
  rects1 = ax.bar(ind, first_request_arr, width,
                  color='black',
                  error_kw=dict(elinewidth=2,ecolor='black'))

  rects2 = ax.bar(ind, unauthorized_status_arr, width,
                      color='red',
                      error_kw=dict(elinewidth=2,ecolor='red'))

  # rects3 = ax.bar(ind+2*width, second_request_arr, width,
  #                 color='yellow',
  #                 error_kw=dict(elinewidth=2,ecolor='yellow'))

  # rects4 = ax.bar(ind+3*width, ok_status_arr, width,
                      # color='green',
                      # error_kw=dict(elinewidth=2,ecolor='green'))

  # axes and labels
  ax.set_xlim(-width,len(ind)+width)
  ax.set_ylim(0,0.001)
  
  ax.set_ylabel('Per Hop Delay')
  ax.set_title('Per hop delay at various nodes')
  
  xTickMarks = [str(i*10)+' req/s' for i in range(1,6)]
  ax.set_xticks(ind+width)
  xtickNames = ax.set_xticklabels(xTickMarks)
  plt.setp(xtickNames, rotation=45, fontsize=10)

  ## add a legend
  # ax.legend( (rects1[0], rects2[0],rects3[0], rects4[0]), ('Initial Request', 'Unauthorized response', 'Re-request', 'Ok Status') )

  # plt.show()
  pylab.savefig(location)


def calculate_time_diff():
    for key in left_bono_second_response:


calculate_time_diff()