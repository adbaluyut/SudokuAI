import json



def drawBoard():
    #this depends on the json file?
    pass

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


def main():
    # The json needs to be in the same directory as the sudoku file
    with open('games.json') as f:
        game = json.load(f)
    print(game)


if __name__ == "__main__":
    main()


#An OG empty spot will contain all numbers in it's value list and is initialized with a '.'
#An OG given number will only contain the number that it is in it's value list, and is intialized as itself

def cp(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

nums  = '123456789'
rows     = 'ABCDEFGHI'
cols     = nums
squares  = cp(rows, cols)
unitlist = ([cp(rows, c) for c in cols] +
            [cp(r, cols) for r in rows] +
            [cp(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((square, [u for u in unitlist if square in u]) 
            for square in squares)
peers = dict((square, set(sum(units[square],[]))-set([square]))
            for square in squares)

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any num; then assign values from the grid.
    values = dict((square, nums) for square in squares)
    for square,num in grid_values(grid).items():
        if num in nums and not assign(values, square, num):
            return False ## (Fail if we can't assign num to square.)
    return values

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in nums or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))