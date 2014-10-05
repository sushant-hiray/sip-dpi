from scapy.all import *

leftover = ''
first_request = 0
second_request = 0
unauthorized_status = 0
ok_status = 0
service_unavailable_status = 0
server_timeout_status = 0
forbidden_status = 0
total = 0;
fart_response = 0
init_request = {}
sec_request = {}
status_unauthorised = {}
status_ok = {}
status_service_unavailable = {}
status_server_timeout = {}
status_forbidden = {}

def extract_status(load, time):
    print "extract_status"
    print load
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
    print "STATUS " + status + " for " + username + " at time " + str(time)
    global unauthorized_status
    global ok_status
    global service_unavailable_status
    global server_timeout_status
    global forbidden_status
    global fart_response
    if status == '401':
        if status_unauthorised.has_key(username) == False: 
            status_unauthorised[username] = 1
            unauthorized_status = unauthorized_status + 1
    elif status == '200':
        if status_ok.has_key(username) == False:
            status_ok[username] = 1
            ok_status = ok_status + 1
    elif status == '503':
        if status_service_unavailable.has_key(username) == False:
            status_service_unavailable[username] = 1
            service_unavailable_status = service_unavailable_status + 1
    elif status == '504':
        if status_server_timeout.has_key(username) == False:
            status_server_timeout[username] = 1
            server_timeout_status += 1
    elif status == '403':
        if status_forbidden.has_key(username) == False:
            status_forbidden[username] = 1
            forbidden_status += 1

def extract_register(load, time):
    print "############################"
    print load
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        
    load_copy = load
    username_start = load.find('username')
    if username_start == -1:
        #print "[ERROR: extract_register]: Username start not found"
        return

    username_start +=10
    username_end = load.find('@', username_start)
    if username_end == -1:
        #print "[ERROR: extract_register]: Username end not found"
        return

    username = load[username_start:username_end]

    nonce_start = load.find('nonce', username_end)
    if nonce_start == -1:
        #print "[ERROR: extract_register]: nonce_start not found"
        return
    nonce_start +=7
    nonce_end = load.find('"',nonce_start)
    if nonce_end == -1:
        #print "[ERROR: extract_register]: nonce_end not found"
        return
    nonce = load[nonce_start:nonce_end]


    global first_request
    global second_request
    if (nonce.strip() == ''):
        print "REGISTER[1] for " + username + " at time " + str(time)
        if init_request.has_key(username) == False:
            init_request[username] = 1;
            first_request = first_request + 1    
    else:
        print "REGISTER[2] for " + username + " at time " + str(time)
        if sec_request.has_key(username) == False:
            sec_request[username] = 1
            second_request = second_request + 1
    count = load.count("CSeq: 1 REGISTER")
    if (count > 1):
        "found more than 1 CSEQ for username " + username
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
                elif (bucket[0] == 'REGISTER'):
                    extract_register(load, time)
                    total = total + 1
            if(len(load) > cl_end):
                load = load[cl_end+1:]
                load = load.strip()
            else:
                break        
        else:
            leftover = load
            break


def print_result():
    print "Total number of lines in file is " + str(total)
    print "Number of requests sent initially " + str(first_request)
    print "Unauthorized response to the first request " + str(unauthorized_status)
    print "Number of re-requests " + str(second_request)
    print "Successful requests " + str(ok_status)
    print "Service unavailable status " + str(service_unavailable_status)
    print "Number of server timeout requests is " + str(server_timeout_status)
    print "Number of forbidden requests is " + str(forbidden_status)
    print "\n"


def main(filename):
    pkts = rdpcap(filename)
    for i in xrange(0, len(pkts)):
        if "sip" in str(pkts[i]):
            extract_sip(pkts[i].load, pkts[i].time)
        else:
            extract_sip(str(pkts[i]), pkts[i].time)



main(str(sys.argv[1]))
print_result()
# print mystr
# print "###############"
# cl_loc = mystr.find('Content-Length')
# cl_end = cl_loc+19
# print mystr[cl_end:]
# print "$$$$$$$$$$$$$$$$"
# print mystr2
# fp = open('multiple-register.pcap', 'r')
# strs = fp.read()
# extract_register(strs,1)