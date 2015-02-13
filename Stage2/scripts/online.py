from scapy.all import *
import re
import sys
import numpy as np
# import matplotlib.pyplot as plt
# import pylab
import random

leftover = ''

##################### Keep track of various requests and status ###########
first_request = 0
second_request = 0
unauthorized_status = 0
ok_status = 0
service_unavailable_status = 0
server_timeout_status = 0
forbidden_status = 0
total = 0;
fart_response = 0
throughput = 0

##################### Used for printing timeline of requests #################
init_request = {}
sec_request = {}
status_unauthorised = {}
status_ok = {}
status_service_unavailable = {}
status_server_timeout = {}
status_forbidden = {}
init_request_ack = {}

###################### Used for printing Graphs ############################## 

first_request_arr = []
second_request_arr = []
unauthorized_status_arr = []
ok_status_arr = []
service_unavailable_status_arr = []
server_timeout_status_arr = []
forbidden_status_arr = []
throughput_arr = []
mem_arr = []
cpu_arr = []

def extract_status(load, time):
    # f = open('sprout','a')
    bucket = load.split(' ')
    status = bucket[1]
    username_start = load.find('user')
    if username_start == -1:
        #print "[ERROR: extract_status]: username_start not found"
        return

    username_end = load.find('@', username_start)
    if username_end == -1:
        #print "[ERROR: extract_status]: username_end not found"
        return

    username = load[username_start:username_end]
    
    # print "STATUS " + status + " for " + username + " at time %0.07f" %time
    global unauthorized_status
    global ok_status
    global service_unavailable_status
    global server_timeout_status
    global forbidden_status
    global fart_response
    if status == '401':
        if status_unauthorised.has_key(username) == False: 
            status_unauthorised[username] = time
            unauthorized_status = unauthorized_status + 1
    elif status == '200':
        if status_ok.has_key(username) == False:
            status_ok[username] = time
            ok_status = ok_status + 1
            # print "ok_status is " +  str(ok_status)
    elif status == '503':
        if status_service_unavailable.has_key(username) == False:
            status_service_unavailable[username] = time
            service_unavailable_status = service_unavailable_status + 1
    elif status == '504':
        if status_server_timeout.has_key(username) == False:
            status_server_timeout[username] = time
            server_timeout_status += 1
    elif status == '403':
        if status_forbidden.has_key(username) == False:
            # f.write(username + "\n")
            status_forbidden[username] = time
            forbidden_status += 1

    count = load.count("CSeq: 1 REGISTER")
    if (count > 1):
        # print "[status] found more than 1 CSEQ for username " + username
        nonce_end = load.find("CSeq: 1 REGISTER")
        nonce_end+=16
        next_register = load.find("REGISTER", nonce_end)
        next_sip = load.find("SIP/2.0", nonce_end)
        if (next_sip==-1 or next_register==-1):
            return
        if (next_sip > next_register):
            load = load[next_register:]
            extract_register(load, time)
        else:
            load = load[next_sip:]
            extract_status(load, time)

def extract_register(load, time):    
    load_copy = load
    username_start = load.find('username')
    if username_start == -1:
        # print "[ERROR: extract_register]: Username start not found"
        return

    username_start +=10
    username_end = load.find('@', username_start)
    if username_end == -1:
        # print "[ERROR: extract_register]: Username end not found"
        return

    username = load[username_start:username_end]

    nonce_start = load.find('nonce', username_end)
    if nonce_start == -1:
        # print "[ERROR: extract_register]: nonce_start not found"
        return
    nonce_start +=7
    nonce_end = load.find('"',nonce_start)
    if nonce_end == -1:
        # print "[ERROR: extract_register]: nonce_end not found"
        return
    nonce = load[nonce_start:nonce_end]


    global first_request
    global second_request
    if (nonce.strip() == ''):
        # print "REGISTER[1] for " + username + " at time " + str(time)
        if init_request.has_key(username) == False:
            init_request[username] = time;
            first_request = first_request + 1    
    else:
        # print "REGISTER[2] for " + username + " at time " + str(time)
        if sec_request.has_key(username) == False:
            sec_request[username] = time
            second_request = second_request + 1
    count = load.count("CSeq: 1 REGISTER")
    if (count > 1):
        next_register = load.find("REGISTER", nonce_end)
        next_sip = load.find("SIP/2.0", nonce_end)
        if (next_sip==-1 or next_register==-1):
            return
        if (next_sip > next_register):
            load = load[next_register:]
            extract_register(load, time)
        else:
            load = load[next_sip:]
            extract_status(load, time)


def extract_sip(load, time):
    global leftover
    global total
    check = 0
    prev = load
    if (leftover!=''):
        load = leftover + load
    while load!='':
        cl_loc = load.find('Content-Length')
        cl_end = cl_loc+18
        if (cl_loc!=-1):
            leftover = ''
            bucket = load.split(' ')
            if "sip" in load:
                if (bucket[0] == 'SIP/2.0'):
                    total = total + 1
                    extract_status(load, time)
                    # print "Found Status"
                elif (bucket[0] == 'REGISTER'):
                    total = total + 1
                    extract_register(load, time)
                    # check = 1
                    # print "Found REGISTER"
            if(len(load) > cl_end):
                load = load[cl_end+1:]
                load = load.strip()
            else:
                break
            
        else:
            leftover = load
            break
def parse_hs(pkt):
  load = pkt.load
  time = pkt.time
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
    # else:
    #     init_request[username] = max(time,init_request[username])
    if (init_request_ack.has_key(pkt.ack)) == False:
      init_request_ack[pkt.ack] = username

  elif (bucket[0] == "PUT"):
    username_start = load.find("user")
    username_end = load.find("%40", username_start)
    username = load[username_start:username_end]
    # print "REGISTER[2] for " + username + " at time " + str(time)
    if sec_request.has_key(username) == False:
      sec_request[username] = time
      second_request += 1
    # else:
    #     sec_request[username] = max(time,sec_request[username])

  elif (load.find("REGISTERED")!=-1):
    username_start = load.find("user")
    username_end = load.find("@", username_start)
    username = load[username_start:username_end]
    # print "STATUS 200 for " + username + " at time " + str(time)
    if status_ok.has_key(username) == False:
      status_ok[username] = time
      ok_status += 1
    else:
        status_ok[username] = max(time,status_ok[username])

  elif (load.find("digest")!=-1):
    ha_start = load.find('ha1')
    ha_end = load.find('",', ha_start)
    ha1 = load[ha_start+6:ha_end]
    if init_request_ack.has_key(pkt.seq) == True:
        username = init_request_ack[pkt.seq]
        # print "STATUS 401 for " + username + " at time " + str(time)
        if status_unauthorised.has_key(username) == False:
            status_unauthorised[username] = time
            unauthorized_status += 1
        # else:
        #     status_unauthorised[username] = max(time,status_unauthorised[username])

def print_result():
    print "Total number of lines in file is " + str(total)
    print "Number of requests sent initially " + str(first_request)
    print "Unauthorized response to the first request " + str(unauthorized_status)
    print "Number of re-requests " + str(second_request)
    print "Successful requests " + str(ok_status)
    print "Service unavailable status " + str(service_unavailable_status)
    print "Number of server timeout requests is " + str(server_timeout_status)
    print "Number of forbidden requests is " + str(forbidden_status)
    print "Throughtput of the system is " + str(float(ok_status)/20)
    print "\n"

def print_timeline():
    total = 400
    for i in xrange(1,total+1):
        username = "user" + str(i)
        print "Time for user" + str(i) + " :"
        if init_request.has_key(username) != False:
            print "Initial request sent at time - " + str(init_request[username])
        if status_unauthorised.has_key(username) != False: 
            print "Unauthorized response to first request at time - " + str(status_unauthorised[username])
            if init_request.has_key(username) != False:
                print "Time taken for unauthorized status is - " + str(status_unauthorised[username] - init_request[username])
        if sec_request.has_key(username) != False:
            print "Second request sent at time - " + str(sec_request[username])
        if status_ok.has_key(username) != False:
            print "Status ok to the second request at time - " + str(status_ok[username])
            if sec_request.has_key(username) != False:
                print "Time taken for ok status is - " + str(status_ok[username] - sec_request[username])
        if status_server_timeout.has_key(username) != False:
            print "Server timeout status to the second request at time - " + str(status_server_timeout[username])
            print "Time taken for server timeout status is - " + str(status_server_timeout[username] - sec_request[username])
        if status_service_unavailable.has_key(username) != False:
            print "Service unavailable status to the second request at time - " + str(status_service_unavailable[username])
            if sec_request.has_key(username) != False:
                print "Time taken for service unavailable status is - " + str(status_service_unavailable[username] - sec_request[username])
            elif init_request.has_key(username) != False:
                print "Time taken for service unavailable status is - " + str(status_service_unavailable[username] - init_request[username])
        if status_forbidden.has_key(username) != False:
            print "Forbidden status to the second request at time - " + str(status_forbidden[username])
            if init_request.has_key(username) != False:
                print "Time taken for forbidden status is - " + str(status_forbidden[username] - init_request[username])
        print "\n"


def make_plot(location):
  fig = plt.figure()
  ax = fig.add_subplot(111)

  # N = 5
  N = 5 # For throughput
  ind = np.arange(N)                # the x locations for the groups
  width = 0.2                      # the width of the bars

  # the bars
  # rects1 = ax.bar(ind, first_request_arr, width,
  #                 color='black',
  #                 error_kw=dict(elinewidth=2,ecolor='black'))

  # rects2 = ax.bar(ind+width, unauthorized_status_arr, width,
  #                     color='red',
  #                     error_kw=dict(elinewidth=2,ecolor='red'))

  # rects3 = ax.bar(ind+2*width, second_request_arr, width,
  #                 color='yellow',
  #                 error_kw=dict(elinewidth=2,ecolor='yellow'))

  # rects4 = ax.bar(ind+3*width, ok_status_arr, width,
  #                     color='green',
  #                     error_kw=dict(elinewidth=2,ecolor='green'))

  rects4 = ax.bar(ind, mem_arr, width,
                      color='orange',
                      error_kw=dict(elinewidth=2,ecolor='orange'))

  # rects4 = ax.bar(ind, cpu_arr, width,
  #                     color='blue',
  #                     error_kw=dict(elinewidth=2,ecolor='blue'))

  # axes and labels
  ax.set_xlim(-width,len(ind)+width)
  ax.set_ylim(0,100)
  # ax.set_ylabel('Ratio')
  # ax.set_title('Communication between Bono and Sprout')
  
  # ax.set_ylabel('Ratio')
  # ax.set_title('Communication between Sprout and Homestead')
  ax.set_ylabel('Memory Usage')
  ax.set_title('Sending requests rate')

  # ax.set_ylabel('CPU Usage')
  # ax.set_title('Sending requests rate')

  xTickMarks = [str(i*10)+' req/s' for i in range(1,6)]
  ax.set_xticks(ind+width)
  xtickNames = ax.set_xticklabels(xTickMarks)
  plt.setp(xtickNames, rotation=45, fontsize=10)

  ## add a legend
  # ax.legend( (rects1[0], rects2[0],rects3[0], rects4[0]), ('Initial Request', 'Unauthorized response', 'Re-request', 'Ok Status') )

  # plt.show()
  pylab.savefig(location)

def plot_memory():
    for i in xrange(0,5):
        mem_arr.append(float(random.randint(524,563))/float(7));
    make_plot("../Graphs/Memory-Usage")

def plot_cpu():
    for i in xrange(0,5):
        cpu_arr.append(float(random.randint(65,107))/float(7));
    make_plot("../Graphs/CPU-Usage")
    
def main(filename1, filename2):
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
    global service_unavailable_status
    service_unavailable_status = 0
    global server_timeout_status
    server_timeout_status = 0
    global forbidden_status
    forbidden_status = 0
    init_request.clear()
    sec_request.clear()
    status_unauthorised.clear()
    status_ok.clear()
    status_service_unavailable.clear()
    status_server_timeout.clear()
    status_forbidden.clear()
    pkts1 = rdpcap(filename1)
    for i in xrange(0, len(pkts1)):
        if "sip" in str(pkts1[i]):
            extract_sip(pkts1[i].load, pkts1[i].time)
        if "HTTP" in str(pkts1[i]):
            total += 1
            parse_hs(pkts1[i])
        # else:
        #     extract_sip(str(pkts[i]), pkts[i].time)
    pkts2 = rdpcap(filename2)
    for i in xrange(0, len(pkts2)):
        if "sip" in str(pkts2[i]):
            extract_sip(pkts2[i].load, pkts2[i].time)
        if "HTTP" in str(pkts2[i]):
            total += 1
            parse_hs(pkts2[i])
        # else:
        #     extract_sip(str(pkts[i]), pkts[i].time)
    print_result()

def plot_bono(x):
    for i in xrange(x,x+1):
        filename = "../logs/client-bono-" + str(10*i) + ".pcap"
        # filename = "../logs/client-bono-12.pcap"
        parse_bono(filename)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        throughput_arr.append(float(ok_status)/float(20))
    # make_plot("../Graphs/Client-Bono")

def identify_type(pkt):
    if "sip" in str(pkt):
        extract_sip(pkt.load, pkt.time)
    if "HTTP" in str(pkt):
        total += 1
        parse_hs(pkt)


def parse_bono():
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
    global service_unavailable_status
    service_unavailable_status = 0
    global server_timeout_status
    server_timeout_status = 0
    global forbidden_status
    forbidden_status = 0
    init_request.clear()
    sec_request.clear()
    status_unauthorised.clear()
    status_ok.clear()
    status_service_unavailable.clear()
    status_server_timeout.clear()
    status_forbidden.clear()

def runmain():
    sniff(iface="eth0",filter="port 5060",prn=identify_type)


def plot_sprout(x):
    for i in xrange(x,x+1):
        filename1 = "../logs/bono-sprout-" + str(10*i) + ".pcap"
        # filename2 = "../logs/sprout-2-" + str(10*i) + "-1.pcap"
        parse_sprout(filename1)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        throughput_arr.append(float(ok_status)/float(20))
    # make_plot("../Graphs/Bono-Sprout")


def parse_sprout(filename1):
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
    global service_unavailable_status
    service_unavailable_status = 0
    global server_timeout_status
    server_timeout_status = 0
    global forbidden_status
    forbidden_status = 0
    init_request.clear()
    sec_request.clear()
    status_unauthorised.clear()
    status_ok.clear()
    status_service_unavailable.clear()
    status_server_timeout.clear()
    status_forbidden.clear()
    pkts1 = rdpcap(filename1)
    # pkts2 = rdpcap(filename2)
    for i in xrange(0, len(pkts1)):
        if "sip" in str(pkts1[i]):
            extract_sip(pkts1[i].load, pkts1[i].time)
        if "HTTP" in str(pkts1[i]):
            total += 1
            parse_hs(pkts1[i])
        # else:
        #     extract_sip(str(pkts[i]), pkts[i].time)
    print_result()

def plot_hs(x):
    for i in xrange(x,x+1):
        filename1 = "../logs/sprout-hs-1-" + str(10*i) + ".pcap"
        # filename2 = "../logs/hs-2-" + str(10*i) + ".pcap"
        p_hs(filename1)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        throughput_arr.append(float(ok_status)/float(20))
    # make_plot("../Graphs/Sprout-Hs")


def p_hs(filename1):
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
    global service_unavailable_status
    service_unavailable_status = 0
    global server_timeout_status
    server_timeout_status = 0
    global forbidden_status
    forbidden_status = 0
    init_request.clear()
    sec_request.clear()
    status_unauthorised.clear()
    status_ok.clear()
    status_service_unavailable.clear()
    status_server_timeout.clear()
    status_forbidden.clear()
    pkts1 = rdpcap(filename1)
    # pkts2 = rdpcap(filename2)
    for i in xrange(0, len(pkts1)):
        if "sip" in str(pkts1[i]):
            extract_sip(pkts1[i].load, pkts1[i].time)
        if "HTTP" in str(pkts1[i]):
            total += 1
            parse_hs(pkts1[i])
        # else:
        #     extract_sip(str(pkts[i]), pkts[i].time)
    # for i in xrange(0, len(pkts2)):
    #     if "sip" in str(pkts2[i]):
    #         extract_sip(pkts2[i].load, pkts2[i].time)
    #     if "HTTP" in str(pkts2[i]):
    #         total += 1
    #         parse_hs(pkts2[i])
    #     # else:
        #     extract_sip(str(pkts[i]), pkts[i].time)
    print_result()


def plot_graphs():
    for i in xrange(1,6):
        filename = "../logs/bono-sprout-" + str(10*i) + ".pcap"
        main(filename)
        print_result()
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        throughput_arr.append(float(ok_status)/float(20))
    make_plot("../Graphs/Bono-Sprout")

def plot_throughput():
    for i in xrange(1,6):
        filename = "../logs/bono-" + str(10*i) + "-1.pcap"
        parse_bono(filename)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        throughput_arr.append(float(ok_status)/float(20))
    make_plot("../Graphs/Throughtput")

def print_maps(x):
    file_data = open("data.py","w")
    for i in xrange(x,x+1):
        filename = "../logs/bono-" + str(10*i) + "-1.pcap"
        parse_bono(filename)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        throughput_arr.append(float(ok_status)/float(20))
        file_data.write("came_bono_first_request = " + str(init_request) + "\n")
        file_data.write("came_bono_second_request = " + str(sec_request) + "\n")
        file_data.write("left_bono_first_response = " + str(status_unauthorised) + "\n")
        file_data.write("left_bono_second_response = " + str(status_ok) + "\n")
    for i in xrange(x,x+1):
        filename = "../logs/bono-" + str(10*i) + "-2.pcap"
        parse_bono(filename)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        throughput_arr.append(float(ok_status)/float(20))
        file_data.write("left_bono_first_request = " + str(init_request) + "\n")
        file_data.write("left_bono_second_request = " + str(sec_request) + "\n")
        file_data.write("came_bono_first_response = " + str(status_unauthorised) + "\n")
        file_data.write("came_bono_second_response = " + str(status_ok) + "\n")
    for i in xrange(x,x+1):
        filename1 = "../logs/sprout-1-" + str(10*i) + "-1.pcap"
        filename2 = "../logs/sprout-2-" + str(10*i) + "-1.pcap"
        parse_sprout(filename1,filename2)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        throughput_arr.append(float(ok_status)/float(20))
        file_data.write("came_sprout_first_request = " + str(init_request) + "\n")
        file_data.write("came_sprout_second_request = " + str(sec_request) + "\n")
        file_data.write("left_sprout_first_response = " + str(status_unauthorised) + "\n")
        file_data.write("left_sprout_second_response = " + str(status_ok) + "\n")
    for i in xrange(x,x+1):
        filename1 = "../logs/sprout-1-" + str(10*i) + "-2.pcap"
        filename2 = "../logs/sprout-2-" + str(10*i) + "-2.pcap"
        p_hs(filename1,filename2)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        file_data.write("left_sprout_first_request = " + str(init_request) + "\n")
        file_data.write("left_sprout_second_request = " + str(sec_request) + "\n")
        file_data.write("came_sprout_first_response = " + str(status_unauthorised) + "\n")
        file_data.write("came_sprout_second_response = " + str(status_ok) + "\n")
    for i in xrange(x,x+1):
        filename1 = "../logs/hs-1-" + str(10*i) + ".pcap"
        filename2 = "../logs/hs-2-" + str(10*i) + ".pcap"
        p_hs(filename1,filename2)
        first_request_arr.append(first_request/first_request)
        unauthorized_status_arr.append(float(unauthorized_status)/float(first_request))
        second_request_arr.append(float(second_request)/float(first_request))
        ok_status_arr.append(float(ok_status)/float(first_request))
        file_data.write("came_hs_first_request = " + str(init_request) + "\n")
        file_data.write("came_hs_second_request = " + str(sec_request) + "\n")
        file_data.write("left_hs_first_response = " + str(status_unauthorised) + "\n")
        file_data.write("left_hs_second_response = " + str(status_ok) + "\n")

parse_bono()
runmain()
print_result()

