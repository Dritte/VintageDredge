import random

attempts = 1000000
failures = 0
count = 0
x=[]

def shuffle(deck):
  for i in range(len(deck)):
    num = random.randint(i,len(deck)-1)
    temp = deck[i]
    deck[i] = deck[num]
    deck[num] = temp

def makeDecisions(deck):
    shuffle(deck)
    hand = deck[0:7-i]
    for j in range(4):
      if j in hand:
        x.append(i)
        raise
    for j in range(4):
      if (j+4) in hand:
        deck = deck[len(hand):]
        makeDecisions(deck)

for k in range(attempts):
  #print k
  deck = range(60)
  try:
    for i in range(7):
      makeDecisions(deck)
    failures+=1
    x.append(7)
  except:
    pass

print "attempts"
print attempts
print "successes"
print attempts - failures
print "failures"
print failures
print "success_rate"
print ((attempts - failures)*1.0)/attempts
print "Average hand size kept"
print (sum([7-i for i in x])*1.0)/attempts
