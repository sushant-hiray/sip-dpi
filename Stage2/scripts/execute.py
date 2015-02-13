import os

for i in xrange(1,2):
  os.system("python test.py " + str(i) + " > check")
  os.system("python per_hop_delay.py > out")
