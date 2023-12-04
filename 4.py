"""
Day 4
"""
filepath = "data/4.txt"
#filepath = 'test.txt'
from day2 import load_file
import re



def get_game_card(card):
    return int(re.findall(r"Card\W*(\d*)", card)[0])


def process_card(data, nums, card_count):
    """
    Process a specific card(data) and return a dict of new card won from this
    along including any duplicates
    """
    card_num = get_game_card(data)

    # Find number of winning numbers (same as part 1)
    wins = find_winning_num_count(data)

    # iterate over each instance of the same card I have
    for card in range(nums):
        # iterate over a range of the wins running from
        # current_card + 1 and the number of wins
        for win in range(card_num+1, card_num+wins+1):
            # Add one new card each time
            card_count[win] += 1


def find_winning_num_count(card):
    """
    Find the amount of winning number on the card from the raw data line
    """
    data = card.split(':')[1]
    ref = data.split('|')[0].strip('\n').split(' ')
    game = data.split('|')[1].strip('\n').split(' ')
    ref = set([val for val in ref if val != ''])
    game = set([val for val in game if val != ''])

    res = ref.intersection(game)
    val = len(res)

    return val


def run():

    # Build a dict of all counds and how many I have of each
    card_count = dict(zip(range(1,205), [1]*204))

    # Loop over each card data
    for card in load_file(filepath):
        card_no = get_game_card(card)

        # Process the current card according to how have instances of it I have
        process_card(card, card_count[card_no], card_count)

    total = sum(card_count.values())
    return total


def run_4_1():
    score = 0
    for card in load_file(filepath):
        val = find_winning_num_count(card)

        if val-1 < 0:
            continue
        this_scope = 2**(val-1)
        #print(f"{ref=}, {this_scope=}")
        score += this_scope

    return score

if __name__ == '__main__':
    print(run())
