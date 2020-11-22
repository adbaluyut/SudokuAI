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

    # change False to True if you want to output the results to a file results.txt
    show(board, False, difficulty, puzzle)
    show(search(board2dict(selected_game)), False, difficulty, puzzle)

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

# print the board to the terminal with an option to output to a file
def show(values, output, difficulty, puzzle):
    if output is True:
        f = open('results.txt', 'a')
        f.write('\n' + difficulty + ' ' + puzzle + '\n')
    horizontal_line = "------+-------+------"
    for letter in rows:
        #for every row iterate through the columns and append to a new string the value in that index
        # after every num a space space is added and after the third and sixth col a '|' is added
        print (''.join(values[letter + digit] + (' | ' if digit in '36' else ' ') for digit in cols))
        if output is True:
            f.write(''.join(values[letter + digit] + (' | ' if digit in '36' else ' ') for digit in cols))
            f.write('\n')
        # after column C and F print the horizontal grid line
        if letter in 'CF': 
            print (horizontal_line)
            if output is True:
                f.write(horizontal_line + '\n')
    if output is True:
        f.close()
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

    
if __name__ == '__main__':
    main()
