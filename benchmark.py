#!/usr/bin/env python

from change import *
import sys, os, getopt, random, time

def printHelp():
  print
  print os.path.basename(sys.argv[0]) + " [--help|-h]",
  print "[(--algorithm|-a)=(greedy|dp|slow)]"
  print
  print "Enter the name of the script, optional argument to specify the algorithm, "
  print "and the number of random data points to be generated."
  print 
  print "--coins,-a\tspecify coin denominations"
  print "--algorithm,-a\tspecify and algorithm"
  print "--avg\t\tthe number of times to run the test and average, defaults to 10"
  print "--steps\t\tdefaults to 1"
  print "--stepsize\t\tdefaults to 1000"
  print "--help,-h\tprint this help message"

  print
  print "Sample usage..."
  print "\t" + os.path.basename(sys.argv[0]) + " -a=dp -c=1,5,10,25"
  print

def main(argv):

  try:
    opts, args = getopt.getopt(argv, "ha:c:", ["help", "algorithm=", "steps=", "stepsize=", "coins=", "start="])
  except getopt.GetoptError:
    printHelp()
    exit(2)

  selectedAlgorithm = "dp"
  avg = 10
  steps = 1
  stepsize = 1000
  start = 1000
  coinList = []

  for opt in opts:
    if opt[0] == "--algorithm" or opt[0] == "-a":

      if opt[1] in ["dp", "greedy", "slow"]:
        selectedAlgorithm = opt[1]

    elif opt[0] == "--steps":
      steps = int(opt[1])

    elif opt[0] == "--stepsize":
      stepsize = int(opt[1])

    elif opt[0] == "--start":
      start = int(opt[1])

    elif opt[0] == "--coins" or opt[0] == "-c":
      coins = opt[1].split(",")
      for coin in coins:
        coinList.append(int(coin))

    elif opt[0] == "--help" or opt[0] == "-h":
      printHelp()
      exit(1)

  if len(coinList) == 0:
    printHelp()
    exit(1)


  for step in range(1, steps + 1):

    totalTime = 0

    amount = start + (step - 1) * stepsize; 

    for j in range(0, avg):

      startTime = time.clock()

      if selectedAlgorithm == "dp":
        changedp(coinList, amount)

      elif selectedAlgorithm == "slow":
        changeslow(coinList, amount)

      elif selectedAlgorithm == "greedy":
        changegreedy(coinList, amount)

      else:
        print "Unsupported algorithm: ", selectedAlgorithm
        exit(1)

      endTime = time.clock()
      totalTime = totalTime + (endTime - startTime)

    avgTime = totalTime / avg
    print str(amount) + "," + str(avgTime)

if __name__ == "__main__":
  main(sys.argv[1:])
