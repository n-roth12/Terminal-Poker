from poker import *

def testHand(hand):
	sorted_hand = sort(hand)
	full_result = checkHand(sorted_hand)
	if len(full_result) > 1:
		print(full_result[0], displayHand(full_result[1]), full_result[2])

# should return two pair of A and 10
test1 = [Card(14, 'C'), Card(10, 'H'), Card(10, 'D'), Card(8, 'D'), Card(14, 'H'), Card(3, 'H'), Card(2, 'H')]

# should return royal flush of clubs
test2 = [Card(14, 'C'), Card(10, 'C'), Card(11, 'C'), Card(13, 'C'), Card(14, 'H'), Card(12, 'C'), Card(2, 'H')]

# should return straight flush from 9-5
test3 = [Card(6, 'C'), Card(9, 'C'), Card(7, 'C'), Card(13, 'C'), Card(8, 'C'), Card(2, 'C'), Card(5, 'C')]

# should return straight from 9-5
test4 = [Card(6, 'S'), Card(9, 'S'), Card(7, 'H'), Card(13, 'D'), Card(8, 'D'), Card(2, 'C'), Card(5, 'H')]

# should return a flush
test5 = [Card(6, 'C'), Card(2, 'H'), Card(7, 'C'), Card(13, 'C'), Card(8, 'H'), Card(2, 'C'), Card(14, 'C')]

# should return full house of 6 and 2
test6 = [Card(6, 'C'), Card(2, 'H'), Card(7, 'D'), Card(6, 'D'), Card(8, 'H'), Card(2, 'C'), Card(6, 'S')]

# should return three-of-a-kind of 6
test7 = [Card(6, 'C'), Card(2, 'H'), Card(7, 'C'), Card(6, 'D'), Card(8, 'H'), Card(6, 'D'), Card(14, 'S')]

# should return pair of 9
test8 = [Card(4,  'D'), Card(9, 'S'), Card(14, 'C'), Card(10, 'D'), Card(8, 'H'), Card(6, 'D'), Card(9, 'C')]

# should return two pair of 2 and J
test9 = [Card(11, 'S'), Card(2, 'S'), Card(4, 'C'), Card(2, 'D'), Card(8, 'D'), Card(11, 'H'), Card(14, 'S')]

# should return straight from 5-A
test10 = [Card(3, 'D'), Card(2, 'D'), Card(8, 'C'), Card(4, 'D'), Card(10, 'H'), Card(5, 'S'), Card(14, 'H')]

# should return four-of-a-kind of 5
test11 = [Card(5, 'S'), Card(2, 'D'), Card(5, 'C'), Card(5, 'D'), Card(10, 'H'), Card(12, 'H'), Card(5, 'H')]

# should return straight from 5-A
test12 = [Card(3, 'H'), Card(14, 'D'), Card(5, 'S'), Card(4, 'D'), Card(8, 'S'), Card(2, 'C'), Card(11, 'C')]

playGame()
