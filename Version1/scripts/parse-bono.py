import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

first_request_arr = []
second_request_arr = []
unauthorized_status_arr = []
ok_status_arr = []
service_unavailable_status_arr = []
server_timeout_status_arr = []
forbidden_status_arr = []

def parse_client_bono(i):
  fp = open("client-bono-" + str(i) + ".pcap")
  first_request = 0
  second_request = 0
  unauthorized_status = 0
  ok_status = 0
  service_unavailable_status = 0
  server_timeout_status = 0
  forbidden_status = 0
  total = 0;


  for line in fp:
    total += 1
    line = line.strip()
    words = line.split(' ')
    if words[6] == 'Request:':
      if int(words[5]) < 670 and int(words[5]) > 610:
        first_request = first_request + 1
      elif int(words[5]) < 590 and int(words[5]) > 500:
        second_request = second_request + 1
      else:
        print line
    elif words[6] == 'Status:':
      if words[7] == '401':
        unauthorized_status = unauthorized_status + 1
      elif words[7] == '200':
        ok_status = ok_status + 1
      elif words[7] == '503':
        service_unavailable_status = service_unavailable_status + 1
      elif words[7] == '504':
        server_timeout_status += 1
      elif words[7] == '403':
        forbidden_status += 1
    else:
      print line
  first_request_arr.append(first_request/first_request)
  unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
  second_request_arr.append(float(second_request)/float(first_request))
  ok_status_arr.append(float(ok_status)/float(first_request))
  print "Total number of lines in file is " + str(total)
  print "Number of requests sent initially " + str(first_request)
  print "Unauthorized response to the first request " + str(unauthorized_status)
  print "Number of re-requests " + str(second_request)
  print "Successful requests " + str(ok_status)
  print "Service unavailable status " + str(service_unavailable_status)
  print "Number of server timeout requests is " + str(server_timeout_status)
  print "Number of forbidden requests is " + str(forbidden_status)
  print "\n"

def make_plot():
  fig = plt.figure()
  ax = fig.add_subplot(111)

  N = 5
  ind = np.arange(N)                # the x locations for the groups
  width = 0.2                      # the width of the bars

  ## the bars
  rects1 = ax.bar(ind, first_request_arr, width,
                  color='black',
                  error_kw=dict(elinewidth=2,ecolor='black'))

  rects2 = ax.bar(ind+width, unauthorized_status_arr, width,
                      color='red',
                      error_kw=dict(elinewidth=2,ecolor='red'))

  rects3 = ax.bar(ind+2*width, second_request_arr, width,
                  color='yellow',
                  error_kw=dict(elinewidth=2,ecolor='yellow'))

  rects4 = ax.bar(ind+3*width, ok_status_arr, width,
                      color='green',
                      error_kw=dict(elinewidth=2,ecolor='green'))

  # axes and labels
  ax.set_xlim(-width,len(ind)+width)
  ax.set_ylim(0,2)
  ax.set_ylabel('Rate')
  ax.set_title('Communication between Client and Bono')
  xTickMarks = [str(i*10)+' req/secs' for i in range(1,6)]
  ax.set_xticks(ind+width)
  xtickNames = ax.set_xticklabels(xTickMarks)
  plt.setp(xtickNames, rotation=45, fontsize=10)

  ## add a legend
  ax.legend( (rects1[0], rects2[0],rects3[0], rects4[0]), ('Initial Request', 'Unauthorized response', 'Re-request', 'Ok Status') )

  # plt.show()
  pylab.savefig('Client-Bono.png')

def main():
  # parse_client_bono(10)
  # parse_client_bono(15)
  # parse_client_bono(18)
  for i in xrange(1,2):
    parse_client_bono(10*i)
  make_plot()


main()