from scapy.packet import *
from scapy.fields import *
from scapy.ansmachine import *
from scapy.layers.inet import *
import dissector


class IMAPField(StrField):
    """
    field class for handling imap packets
    @attention: it inherets StrField from Scapy library
    """
    holds_packets = 1
    name = "IMAPField"

    def getfield(self, pkt, s):
        """
        this method will get the packet, takes what does need to be
        taken and let the remaining go, so it returns two values.
        first value which belongs to this field and the second is
        the remaining which does need to be dissected with
        other "field classes".
        @param pkt: holds the whole packet
        @param s: holds only the remaining data which is not dissected yet.
        """
        cstream = -1
        if pkt.underlayer.name == "TCP":
            cstream = dissector.check_stream(\
                        pkt.underlayer.underlayer.fields["src"],\
                         pkt.underlayer.underlayer.fields["dst"],\
                          pkt.underlayer.fields["sport"],\
                           pkt.underlayer.fields["dport"],\
                            pkt.underlayer.fields["seq"], s)
        if not cstream == -1:
            s = cstream
        remain = ""
        value = ""
        ls = s.splitlines()
        myresult = ""
        lslen = len(ls)
        i = 0
        k = 0
        for line in ls:
            k = k + 1
            ls2 = line.split()
            length = len(ls2)
            if length > 1:
                value = ls2[0]
                c = 1
                remain = ""
                while c < length:
                    remain = remain + ls2[c] + " "
                    c = c + 1
                if self.name.startswith("request"):
                    myresult = myresult + "Request Tag: " +\
                            value + ", Request Argument: " + remain
                    if k < lslen:
                        myresult = myresult + " | "
                if self.name.startswith("response"):
                    myresult = myresult + "Response Tag: " +\
                    value + ", Response Argument: " + remain
                    if k < lslen:
                        myresult = myresult + " | "
            i = i + 1
            if i == lslen:
                return "", myresult

    def __init__(self, name, default, fmt, remain=0):
        """
        class constructor for initializing the instance variables
        @param name: name of the field
        @param default: Scapy has many formats to represent the data
        internal, human and machine. anyways you may sit this param to None.
        @param fmt: specifying the format, this has been set to "H"
        @param remain: this parameter specifies the size of the remaining
        data so make it 0 to handle all of the data.
        """
        self.name = name
        StrField.__init__(self, name, default, fmt, remain)


class IMAPRes(Packet):
    """
    class for handling imap responses
    @attention: it inherets Packet from Scapy library
    """
    name = "imap"
    fields_desc = [IMAPField("response", "", "H")]


class IMAPReq(Packet):
    """
    class for handling imap requests
    @attention: it inherets Packet from Scapy library
    """
    name = "imap"
    fields_desc = [IMAPField("request", "", "H")]


bind_layers(TCP, IMAPReq, dport=143)
bind_layers(TCP, IMAPRes, sport=143)
