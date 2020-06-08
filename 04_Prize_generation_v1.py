import random

NUM_TRAILS = 100
winnings = 0

cost = NUM_TRAILS * 5

for item in range(0, NUM_TRAILS):
    round_winnings = 0
    for thing in range(0, 3):
        prize_num = random.randint(1,100)
        if 0 < prize_num <= 5:
            round_winnings += 5
        elif 5 < prize_num <=25:
            round_winnings += 2
        elif 25 < prize_num <= 65:
            round_winnings += 1
        '''else:
            prize += "lead"'''

    winnings += round_winnings

print("Paid In: ${}".format(cost))
print("Pay Out: ${}".format(winnings))

if winnings > cost:
    print("You came out ${} ahead".fomat(winnings - cost))
else:
    print("Sorry, you lost ${}".format(cost-winnings))