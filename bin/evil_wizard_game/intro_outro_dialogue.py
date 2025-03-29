from blessings import Terminal

t = Terminal()
def intro(t):
    print('You have traveled for ' + t.underline + 'days' + ' into a thick forest.\nYou stop out of sheer exhaustion and take stock\nWhat will you do next?\n')
    print('You can turn '+ t.underline + t.bold + t.green + 'left, turn right, inspect surroundings, ahead, walk ahead, or open your bag.\n')
