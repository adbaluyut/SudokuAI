import json

def cp(X, Y):
    return [x+y for x in X for y in Y]

nums   = '123456789'
cols     = nums
rows     = 'ABCDEFGHI'
sqs  = cp(rows, cols)

#possible units
unit_pos = ([cp(rows, c) for c in cols] +
            [cp(r, cols) for r in rows] +
            [cp(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
#indiv. units separated
los_units = dict((sq, [u for u in unit_pos if sq in u]) for sq in sqs)
los_peers = dict((sq, set(sum(los_units[sq],[]))-set([sq])) for sq in sqs)

def main():
    # The json needs to be in the same directory as the sudoku file
    with open('games.json') as f:
        game_list = json.load(f)

    #error checking
    while True:
        difficulty = input("Select the difficulty: (e)asy, (m)edium, (h)ard\n").lower()

        if difficulty == 'e':
            difficulty = "easy"
            break
        elif difficulty == 'm':
            difficulty = "medium"
            break
        elif difficulty == 'h':
            difficulty = "hard"
            break
        else:
            print("Something went .")

    print("\nSelect the game you want to play: ")    
    
    # error checking
    while True:
        # display a menu of all the games
        print("+--------------+")
        for g in game_list[difficulty].keys():
            print(f"game id: {g}")    
        print("+--------------+")

        puzzle = input("\nType the game id:\n").lower()

        if puzzle not in game_list[difficulty].keys():
            print("Invalid game id. Try again!\n")
        else:
            break
        
    # show the initial grid
    display(board_values(game_list[difficulty][puzzle]))

    print()

    display(search(board2dict(board_1)))

def board2dict(board):
    """Convert board to a dict of possible values, {square: nums}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any num; then assign values from the board.
    values = dict((sq, nums) for sq in sqs)

    for sq,n in board_values(board).items():
        if n in nums and not assign(values, sq, n):
            return False ## (Fail if we can't assign n to square sq.)
    return values

def board_values(board):
    "Convert board into a dict of {square: char} with '*' for empties."
    chars = [char for char in board if char in nums or char in '*']
    assert len(chars) == 81
    return dict(zip(sqs, chars))

def assign(values, sq, n):
    """Eliminate all the other values (except n) from values[sq] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[sq].replace(n, '')
    if all(eliminate(values, sq, n2) for n2 in other_values):
        return values
    else:
        return False

def eliminate(values, sq, n):
    """Eliminate n from values[sq]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if n not in values[sq]:
        return values ## Already eliminated
    values[sq] = values[sq].replace(n,'')
    ## (1) If a square sq is reduced to one value n2, then eliminate n2 from the los_peers.
    if len(values[sq]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[sq]) == 1:
        n2 = values[sq]
        if not all(eliminate(values, s2, n2) for s2 in los_peers[sq]):
            return False
    ## (2) If a unit u is reduced to only one place for a value n, then put it there.
    for u in los_units[sq]:
        nplaces = [sq for sq in u if n in values[sq]]
        if len(nplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(nplaces) == 1:
            # n can only be in one place in unit; assign it there
            if not assign(values, nplaces[0], n):
                return False
    return values

def display(values):
    "Display these values as a 2-D board."
    width = 1+max(len(values[sq]) for sq in sqs)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print (''.join(values[r+char].center(width)+('|' if char in '36' else '')
                      for char in cols))
        if r in 'CF': print (line)
    print

def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[sq]) == 1 for sq in sqs):
        # display
        return values ## Solved!
    ## Chose the unfilled square sq with the fewest possibilities
    n,sq = min((len(values[sq]), sq) for sq in sqs if len(values[sq]) > 1)

    "Return some element of seq that is true."

    seq = (search(assign(values.copy(), sq, n)) for n in values[sq])

    for e in seq:
        if e: return e
    return False

def solved(values):
    "A puzzle is solved if each unit is a permutation of the nums 1 to 9."
    def unitsolved(unit): 
        return set(values[sq] for sq in unit) == set(nums)
    return values is not False and all(unitsolved(unit) for unit in unit_pos)

board_1  = '**3*2*6**9**3*5**1**18*64****81*29**7*******8**67*82****26*95**8**2*3**9**5*1*3**'

    
if __name__ == '__main__':
    main()
