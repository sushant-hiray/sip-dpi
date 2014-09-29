from scapy.all import *

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
    if (nonce.strip() == ''):
        print "REGISTER[1] for " + username + " at time " + str(time)
    else:
        print "REGISTER[2] for " + username + " at time " + str(time)

def extract_status(load, time):
    bucket = load.split(' ')
    status = bucket[1]
    username_start = load.find('user')
    username_end = load.find('@', username_start)
    username = load[username_start:username_end]
    print "STATUS " + status + " for " + username + " at time " + str(time)

def parse(pkt):
    load = pkt[1].load
    bucket = pkt.load.split(' ')
    if (bucket[0] == 'SIP/2.0'):
        extract_status(pkt.load, pkt.time)
    elif (bucket[0] == 'REGISTER'):
        extract_register(pkt.load, pkt.time)

def main(file_name):
    pkts = rdpcap(file_name)
    for i in xrange(0, len(pkts)):
        parse(pkts[i])

main('../logs/client-bono-1.pcap')

