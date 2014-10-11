from scapy.all import *
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

##################### Keep track of various requests and status ###########
first_request = 0
second_request = 0
unauthorized_status = 0
ok_status = 0
total = 0

##################### Used for printing timeline of requests #################
init_request = {}
sec_request = {}
status_unauthorised = {}
status_ok = {}

first_request_arr = []
second_request_arr = []
unauthorized_status_arr = []
ok_status_arr = []



def parse_hs(load, time):
	global first_request
	global second_request
	global unauthorized_status
	global ok_status
	bucket = load.split(' ')
	if (bucket[0] == "GET"):
		username_start = load.find("user")
		username_end = load.find("%40", username_start)
		username = load[username_start:username_end]
		# print "REGISTER[1] for " + username + " at time " + str(time)
		if (init_request.has_key(username)) == False:
			init_request[username] = time
			first_request += 1

	elif (bucket[0] == "PUT"):
		username_start = load.find("user")
		username_end = load.find("%40", username_start)
		username = load[username_start:username_end]
		# print "REGISTER[2] for " + username + " at time " + str(time)
		if sec_request.has_key(username) == False:
			sec_request[username] = time
			second_request += 1

	elif (load.find("REGISTERED")!=-1):
		username_start = load.find("user")
		username_end = load.find("@", username_start)
		username = load[username_start:username_end]
		# print "STATUS 200 for " + username + " at time " + str(time)
		if status_ok.has_key(username) == False:
			status_ok[username] = time
			ok_status += 1

	elif (load.find("digest")!=-1):
		ha_start = load.find('ha1')
		ha_end = load.find('",', ha_start)
		ha1 = load[ha_start+6:ha_end]
		# print "STATUS 401 Authorized for ha1 " + ha1 + " at time " + str(time)
		if status_unauthorised.has_key(ha1) == False:
			status_unauthorised[ha1] = time
			unauthorized_status += 1

def print_result():
    print "\n"
    print "Total number of lines in file is " + str(total)
    print "Number of requests sent initially " + str(first_request)
    print "Unauthorized response to the first request " + str(unauthorized_status)
    print "Number of re-requests " + str(second_request)
    print "Successful requests " + str(ok_status)
    print "\n"

def make_plot(location):
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
  ax.set_ylabel('Ratio')
  ax.set_title('Communication between Sprout and Homestead')
  xTickMarks = [str(i*10)+' req/s' for i in range(1,6)]
  ax.set_xticks(ind+width)
  xtickNames = ax.set_xticklabels(xTickMarks)
  plt.setp(xtickNames, rotation=45, fontsize=10)

  ## add a legend
  ax.legend( (rects1[0], rects2[0],rects3[0], rects4[0]), ('Initial Request', 'Unauthorized response', 'Re-request', 'Ok Status') )

  # plt.show()
  pylab.savefig(location)

def main(filename):
  global total
  total = 0
  global first_request
  first_request = 0
  global unauthorized_status
  unauthorized_status = 0
  global second_request
  second_request = 0
  global ok_status
  ok_status = 0
  init_request.clear()
  sec_request.clear()
  status_unauthorised.clear()
  status_ok.clear()  
  pkts = rdpcap(filename)
  for pkt in pkts:
	 if "HTTP" in str(pkt):
		  total += 1
		  parse_hs(pkt.load, pkt.time)


def plot_graphs():
    for i in xrange(1,6):
        filename = "../logs/sprout-hs-" + str(10*i) + ".pcap"
        main(filename)
        print_result()
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        # print ok_status
        # print first_request
        # print float(ok_status)/float(first_request)
    make_plot("../Graphs/Sprout-Hs")

def print_maps():
  file_data = open("data.py","a")
  for i in xrange(1,2):
    filename = "../logs/logs/sprout-" + str(10*i) + "-2.pcap"
    main(filename)
    print_result()
    first_request_arr.append(first_request/first_request)
    unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
    second_request_arr.append(float(second_request)/float(first_request))
    ok_status_arr.append(float(ok_status)/float(first_request))
    file_data.write("left_sprout_first_request = " + str(init_request) + "\n")
    file_data.write("left_sprout_second_request = " + str(sec_request) + "\n")
    file_data.write("came_sprout_first_response = " + str(status_unauthorised) + "\n")
    file_data.write("came_sprout_second_response = " + str(status_ok) + "\n")
  for i in xrange(1,2):
    filename = "../logs/logs/hs-" + str(10*i) + ".pcap"
    main(filename)
    print_result()
    first_request_arr.append(first_request/first_request)
    unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
    second_request_arr.append(float(second_request)/float(first_request))
    ok_status_arr.append(float(ok_status)/float(first_request))
    file_data.write("came_hs_first_request = " + str(init_request) + "\n")
    file_data.write("came_hs_second_request = " + str(init_request) + "\n")
    file_data.write("left_hs_first_response = " + str(init_request) + "\n")
    file_data.write("left_hs_second_response = " + str(init_request) + "\n")

# main(str(sys.argv[1]))
# plot_graphs()
# print_result()
print_maps()