import json

def cp(X, Y):
    return [x+y for x in X for y in Y]

nums = '123456789'
cols = nums
rows = 'ABCDEFGHI'
sqs = cp(rows, cols)

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
        # show a menu of all the games
        print("+--------------+")
        for g in game_list[difficulty].keys():
            print(f"game id: {g}")    
        print("+--------------+")

        puzzle = input("\nType the game id:\n").lower()

        if puzzle not in game_list[difficulty].keys():
            print("Invalid game id. Try again!\n")
        else:
            break
    
    selected_game = game_list[difficulty][puzzle]
        
    # show the initial grid
    board = board_values(selected_game)
    show(board)

    show(search(board2dict(selected_game)))

def board_values(board):
    chars = [char for char in board if char in nums or char in '*']
    assert len(chars) == 81
    return dict(zip(sqs, chars))

def board2dict(board):
    values = dict((sq, nums) for sq in sqs)

    for sq,n in board_values(board).items():
        if n in nums and not keep(values, sq, n):
            return False
    return values

def remove(values, sq, n):
    if n not in values[sq]:
        return values 
    values[sq] = values[sq].replace(n,'')

    if len(values[sq]) == 0:
        return False 
    elif len(values[sq]) == 1:
        n2 = values[sq]
        if not all(remove(values, s2, n2) for s2 in los_peers[sq]):
            return False
   
    for unit in los_units[sq]:
        loc_n = [sq for sq in unit if n in values[sq]]
        if len(loc_n) == 0:
            return False 
        elif len(loc_n) == 1:
            if not keep(values, loc_n[0], n):
                return False

    return values

def keep(values, sq, n):
    non_values = values[sq].replace(n, '')
    if all(remove(values, sq, n2) for n2 in non_values):
        return values
    else:
        return False

def show(values):
    width = 1 + max(len(values[sq]) for sq in sqs)
    horizontal_line = "------+-------+------"
    for letter in rows:
        print (''.join(values[letter + digit] + (' | ' if digit in '36' else ' ') for digit in cols))
        # after column C and F print the horizontal grid line
        if letter in 'CF': 
            print (horizontal_line)
    print()

def search(values):
    if values is False:
        return False

    if all(len(values[sq]) == 1 for sq in sqs):
        return values

    n,sq = min((len(values[sq]), sq) for sq in sqs if len(values[sq]) > 1)
    seq = (search(keep(values.copy(), sq, n)) for n in values[sq])

    for e in seq:
        if e: return e
    return False

def solved(values):
    return values is not False and all(unitsolved(unit, values) for unit in unit_pos)


def unitsolved(unit, values): 
        return set(values[sq] for sq in unit) == set(nums)

    
if __name__ == '__main__':
    main()
