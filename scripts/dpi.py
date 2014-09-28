from scapy import *
from dissector import *

first_request = 0
second_request = 0
unauthorized_status = 0
ok_status = 0
service_unavailable_status = 0
server_timeout_status = 0
forbidden_status = 0
total = 0;


def extract_register(load, time):
    username_start = load.find('username')
    username_start +=10
    load = load[username_start:]
    username_end = load.find('@')
    username = load[:username_end]
    nonce_start = load.find('nonce')
    nonce_start +=7
    nonce_end = load.find('"',nonce_start)
    nonce = load[nonce_start:nonce_end]
    global first_request
    global second_request

    if (nonce.strip() == ''):
        print "REGISTER[1] for " + username + " at time " + str(time)
        first_request = first_request + 1
    else:
        print "REGISTER[2] for " + username + " at time " + str(time)
        second_request = second_request + 1

def extract_status(load, time):
    bucket = load.split(' ')
    status = bucket[1]
    username_start = load.find('user')
    username_end = load.find('@', username_start)
    username = load[username_start:username_end]
    print "STATUS " + status + " for " + username + " at time " + str(time)
    global unauthorized_status
    global ok_status
    global service_unavailable_status
    global server_timeout_status
    global forbidden_status
    if status == '401':
        unauthorized_status = unauthorized_status + 1
    elif status == '200':
        ok_status = ok_status + 1
    elif status == '503':
        service_unavailable_status = service_unavailable_status + 1
    elif status == '504':
        server_timeout_status += 1
    elif status == '403':
        forbidden_status += 1

def extract_sip(pkt):
    bucket = pkt.load.split(' ')
    global total
    if (bucket[0] == 'SIP/2.0'):
        extract_status(pkt.load, pkt.time)
        total = total + 1
    elif (bucket[0] == 'REGISTER'):
        extract_register(pkt.load, pkt.time)
        total = total + 1

def main(file_name):
    pkts = rdpcap(file_name)
    for i in xrange(0, 100):
        if "sip" in str(pkts[i]):
            extract_sip(pkts[i])

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


main(str(sys.argv[1]))
print_result()