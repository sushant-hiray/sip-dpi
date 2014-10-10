from scapy.all import *

def parse_hs(load, time):
	bucket = load.split(' ')
	if (bucket[0] == "GET"):
		username_start = load.find("user")
		username_end = load.find("%40", username_start)
		username = load[username_start:username_end]
		print "REGISTER[1] for " + username + " at time " + str(time)
	
	elif (bucket[0] == "PUT"):
		username_start = load.find("user")
		username_end = load.find("%40", username_start)
		username = load[username_start:username_end]
		print "REGISTER[2] for " + username + " at time " + str(time)

	elif (load.find("REGISTERED")!=-1):
		username_start = load.find("user")
		username_end = load.find("@", username_start)
		username = load[username_start:username_end]
		print "STATUS 200 for " + username + " at time " + str(time)

	elif (load.find("digest")!=-1):
		ha_start = load.find('ha1')
		ha_end = load.find('",', ha_start)
		ha1 = load[ha_start+6:ha_end]
		print "STATUS 401 Authorized for ha1 " + ha1 + " at time " + str(time)

def main(filename):
	pkts = rdpcap(filename)
	for pkt in pkts:
		if "HTTP" in str(pkt):
			parse_hs(pkt.load, pkt.time)

main(str(sys.argv[1]))