#!/usr/bin/env python

import sys, os, getopt
sys.setrecursionlimit(100000)

def changeslow(coins, amount, change = None):

  if change == None:
    change = []
    for i in range(0, len(coins)):
      change.append(0)

  try:

    idx = coins.index(amount)
    change[idx] = change[idx] + 1

  except ValueError:

    tmpCoins = None

    for i in range(1, amount):

        iChange = changeslow(coins, i)
        kMinusIChange = changeslow(coins, amount - i)

        tmpCoins2 = 0
        tmpChange = []

        for i in range(0, len(iChange)):
          tmpCoins2 = tmpCoins2 + iChange[i]
          tmpCoins2 = tmpCoins2 + kMinusIChange[i]
          tmpChange.append(iChange[i] + kMinusIChange[i])

        if tmpCoins == None or tmpCoins2 < tmpCoins:
          tmpCoins = tmpCoins2
          change = tmpChange

  return change

def changegreedy(coins, amount):

  change = []
  for i in range(0, len(coins)):
    change.append(0)

  coinIdx = len(coins) - 1;

  while amount > 0:

    while coins[coinIdx] > amount:
      coinIdx = coinIdx - 1

    amount = amount - coins[coinIdx]
    change[coinIdx] = change[coinIdx] + 1

  return change

def changedp(coins, amount, change = None, table = None):

  if change == None:
    change = []
    for i in range(0, len(coins)):
      change.append(0)

  if table == None:
    table = {}
    table[0] = []
    for i in range(0, len(coins)):
      table[0].append(0)

  if table.has_key(amount):
    return table[amount]

  try:

    idx = coins.index(amount)
    change[idx] = change[idx] + 1

  except ValueError:

    tmpCoins = None

    for i in range(1, amount):

        iChange = changedp(coins, i, None, table)
        kMinusIChange = changedp(coins, amount - i, None, table)

        tmpCoins2 = 0
        tmpChange = []

        for i in range(0, len(iChange)):
          tmpCoins2 = tmpCoins2 + iChange[i]
          tmpCoins2 = tmpCoins2 + kMinusIChange[i]
          tmpChange.append(iChange[i] + kMinusIChange[i])

        if tmpCoins == None or tmpCoins2 < tmpCoins:
          tmpCoins = tmpCoins2
          change = tmpChange

  table[amount] = change
  return change

def changedp_bottomup(coins, n):

  C = {}
  C[0] = {}
  C[0][0] = 1;  

  for a in range(0, n + 1):

    for b in range(0, len(coins)):

      if a + coins[b] <= n:

        C[a+coins[b]][b] += C[a][b];

      C[a][b+1] += C[a][b];

  return C[n]

def printHelp():
  print
  print os.path.basename(sys.argv[0]) + " [--algorithm|-a dp,greedy,slow] [--help|-h] file1 [file2 ...]",
  print
  print "Options"
  print "\t--help,-h\tprint this help message"
  print
  print "Enter the name of the script, algorithm type, and the input"
  print "filename. Algorithm can be one of dp, greedy, or slow. The"
  print "default algorithm is dp."
  print
  print "The input file must be in the format of one line [X,Y,Z]"
  print "where the letters are integer coin values and every line"
  print "after the first is an amount to make change for ie..."
  print
  print "[1,2,5]"
  print "10"
  print "[1,3,7,26]"
  print "22"
  print

def parseCoins(line):
  line = line.rstrip()
  line = line[1:len(line) - 1]
  coins = line.split(",")
  for i in range(0, len(coins)):
    coins[i] = int(coins[i])

  return coins

def main(argv):

  try:
    opts, args = getopt.getopt(argv, "ha:", ["help", "algorithm="])
  except getopt.GetoptError:
    printHelp()
    exit(2)

  if len(args) < 1:
    printHelp()
    exit(1)

  algo = "dp"

  for opt in opts:

    if opt[0] == "--help" or opt[0] == "-h":
      printHelp()
      exit(1)
    elif opt[0] == "--algorithm" or opt[0] == "-a":

      if opt[1] in ["dp", "greedy", "slow"]:
        algo = opt[1]
      else:
        print "INVALID ALGORITHM: ", opt[1]
        printHelp()
        exit(1)

  for fileName in args:

    inputFile = open(fileName)
    outputFile = open(fileName[:len(fileName) - 4] + "change.txt", "w")

    while 1:

      coinline = inputFile.readline()
      if not coinline:
        break

      coins = parseCoins(coinline)

      amount = int(inputFile.readline().rstrip())

      if algo == "greedy":
        change = changegreedy(coins, amount)
      elif algo == "slow":
        change = changeslow(coins, amount)
      else:
        change = changedp(coins, amount)

      outputFile.write(str(change) + "\n")
      outputFile.write(str(sum(change)) + "\n")

    inputFile.close()
    outputFile.close()

if __name__ == "__main__":
  main(sys.argv[1:])
