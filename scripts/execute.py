import os

for i in xrange(1,6):
  os.system("python test.py " + str(i))
  os.system("python per_hop_delay.py")