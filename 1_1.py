import re

def convert(value) -> int:
    mapping = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    try:
        return mapping[value]
    except KeyError:
        return value


def run() -> int:
    """
    Iterates over a file of strings and finds the first and last digit in each line. Combines them to a double digit int
    and cummulative adds them together

    Return
    ------
    int
        Total combined value
    """
    # filepath = "/home/warrot/projects/advent_of_coding/data/1_1.txt"
    total = 0
    
    filepath = "/home/warrot/projects/advent_of_coding/data/test.txt"


    # search = r'(\d|one|two|three|four|five|six|seven|eight|nine)'
    patterns = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
    ]
    # search = r'(\d)'

    with open(filepath, "r") as file:
        for line in file:
            first = (999, None)
            last = (-1, None)
            for pat in patterns:
                # pat = 'six'
                res = re.finditer(pat, line)
                for m in res:
                    if m.start() <= first[0]:
                        first = (m.start(), m[0])
                    if m.start() >= last[0]:
                        last = (m.start(), m[0])
            first = str(first[1])
            last = str(last[1])
            comb = int(convert(first) + convert(last))
            print(f"{first=}, {last=}, {comb=}")
            total += comb

    return total

if __name__ == "__main__":
    print(run())