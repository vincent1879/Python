
# 1. 
# 	1. 1 / 8
# 	2. 1 / 8
# 	3. {H,H,T} {H,T,H} {T,H,H}  So 3 / 8
# 	4. 3 + {H,H,H} So 1 / 2

# 2.  6 / 6**5 = 1 / 6**4 = 1 / 1296

import random
import pylab

class SimpleDice(object):
	def __init__(self, side):
		self.side = side

	def RollDice(self):
		return random.randrange(1, self.side + 1)

def SimulateYahtzee(DiceNum, DiceSide, totalTrails):

	DiceSet = []

	YahtzeeCount = 0


	for i in range(DiceNum):
		DiceSet.append(SimpleDice(DiceSide))

	for i in range(totalTrails):
		
		resultSet = []

		for dice in DiceSet:
			result = dice.RollDice()
			resultSet.append(result)

		if checkYahtzee(resultSet):
			YahtzeeCount += 1
			print resultSet

	print 'theorial anwser = ' + str(float(1.0)/1296)
	print 'simulation anwser = ' + str(float(YahtzeeCount) / totalTrails)


def checkYahtzee(rList):

	if len(rList) > 0:
		
		for i in rList:
			if i == rList[0]:
				continue
			else:
				return False
		
		return True
	else:
		return False


if __name__ == '__main__':
	SimulateYahtzee(5,6,100000)









