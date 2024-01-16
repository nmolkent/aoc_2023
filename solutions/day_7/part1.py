from collections import namedtuple

# custom sorting. so ive used a linear sort which should be O(n**2) but could deffinitely try to optimise
# merge sort would be fun to try and implement, check if lower than as well as greater than and split the tree inside the while loop
# the custom ordering has 2 features 
# given a hand size must be len(5) the type_order represents the count fo any 1 card in card order
# the card order represents the value of cards

Hand = namedtuple("Hand", "hand, bid")

def mkHand(hand, bid): 
    return Hand(hand, int(bid))

card_order = "AKQJT98765432"
type_order = [[5], [1, 4], [2, 3], [1, 1, 3], [1, 2, 2], [1, 1, 1, 2], [1, 1, 1, 1, 1]]

def solve(filename):
    cards_seen = []

    with open(filename) as file:
        for line in file:
            h = mkHand(*line.split(" "))
            idx = 0
            while idx < len(cards_seen):
                # sort loop will increase the index in cards seen unless the score comparison is greater than or there is no list left
                score = scorer(cards_seen[idx],h)
                if score > 0:
                    break
                idx += 1
            cards_seen.insert(idx, h)
    
    sum = 0
    for i, card in enumerate(cards_seen[::-1], start=1):
        sum += i * card.bid
    return sum

def scorer(first, second):
    # score these hands against each other first > second = positive
    # create the type of hand for each
    s1 = sorted([first.hand.count(x) for x in card_order if first.hand.count(x) > 0])
    s2 = sorted([second.hand.count(x) for x in card_order if second.hand.count(x) > 0])
    # compare based on type
    if type_order.index(s1) == type_order.index(s2):
        # compare based on card value
        for card1, card2 in zip(first.hand, second.hand):
            if card_order.index(card1) == card_order.index(card2):
                pass
            else:
                # if this difference is positive or negative that represents gt or lt
                return card_order.index(card1) - card_order.index(card2)
        # otherwise the 2 hands are completely equal return zero
        return 0
    else:
        # if this difference is positive or negative that represents gt or lt
        return type_order.index(s1) - type_order.index(s2)

if __name__ == "__main__":
    solve("test1.txt")
