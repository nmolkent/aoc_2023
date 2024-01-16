from collections import namedtuple

Hand = namedtuple("Hand", "hand, bid")
mkHand = lambda hand, bid: Hand(hand, int(bid))

card_order = "AKQT98765432" # remove joker from card order and count jokers sepperately
joker_order = card_order + "J"
type_order = [[5], [1, 4], [2, 3], [1, 1, 3], [1, 2, 2], [1, 1, 1, 2], [1, 1, 1, 1, 1]]

def solve(filename):
    cards_seen = []

    with open(filename) as file:
        for line in file:
            h = mkHand(*line.split(" "))
            idx = 0
            while idx < len(cards_seen):
                score = scorer(cards_seen[idx],h)
                if score > 0:
                    break
                idx += 1
            cards_seen.insert(idx, h)

    sum = 0
    for i, card in enumerate(cards_seen[::-1], start=1):
        sum += i * card.bid
    return sum


def get_type_order(h):
    # the type order is influenced by jokers but broadly matches the previous implementation
    jokers = h.hand.count("J")
    s = sorted([h.hand.count(x) for x in card_order if h.hand.count(x) > 0])
    
    if len(s) == 0: 
        # if all cards are jokers we will have an empty list, manually set it to be 5 of a kind
        s = [5]
    else:
        # if we have values the sorting order means the largest will be at the end of the list, add jokers to the largest
        s[-1] += jokers
    return s

def scorer(first, second):
    s1 = get_type_order(first)
    s2 = get_type_order(second)        
    if type_order.index(s1) == type_order.index(s2):
        for card1, card2 in zip(first.hand, second.hand):
            if card1 == card2:
                pass
            else:
                return joker_order.index(card1) - joker_order.index(card2)
        return 0
    else:
        return type_order.index(s1) - type_order.index(s2)

if __name__ == "__main__":
    solve("test1.txt")
