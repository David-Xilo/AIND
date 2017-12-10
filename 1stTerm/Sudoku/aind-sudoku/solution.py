import itertools
import time
assignments = []


"""
Decorator from:
https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
"""
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000) )
        return result
    return timed

"""
Functions that generate the default values: unused, but present just for fun! 
"""
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

def do_rows():
    return 'ABCDEFGHI'

def do_cols():
    return '123456789'

def do_boxes():
    return cross(do_rows(), do_cols())

def do_row_units():
    return [cross(row, do_cols()) for row in do_rows()]

def do_col_units():
    return [cross(do_rows(), col) for col in do_cols()]

def do_square_units():
    return [cross(row, col) for row in ['ABC', 'DEF', 'GHI'] for col in ['123', '456', '789']]
#print(row_units())

def do_diagonal_units():
    return [ [r1 + c1 for r1, c1 in zip(do_rows(), do_cols())], [r2 + c2 for r2, c2 in zip(do_rows(), do_cols()[::-1])] ]

def do_units_list():
    return do_row_units() + do_col_units() + do_square_units() + do_diagonal_units()

def do_units():
    return {box:[unit for unit in do_units_list() if box in unit] for box in do_boxes()}

"""
The defaults with the additional unit: diagonal_unit
"""
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [ [r1 + c1 for r1, c1 in zip(rows, cols)], [r2 + c2 for r2, c2 in zip(rows, cols[::-1])] ]
unitslist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitslist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

"""
Function that generates the tuples to check for twins.
I use a global variable to avoid the overhead of running the function every time

I wanted to generalize the heuristics, and be able to use the twins technique 
with any size (or at least with triplets). However, this seems to bring a big overhead..
At least the way I implemented.. I leave here the code anyway, but I only use tuples
with size 2 (so they are truly twins)
"""

def twins_tuples():
    result = []
    for i in range(2, 10):
        for tup in itertools.combinations('123456789', i):
            r = ''.join(t for t in tup)
            result.append(r)
    return result

twinstuples = [tup for tup in twins_tuples() if len(tup) < 3] 

#returns either a dict with every possible box and every peer of that box (if no
#input is given), or it returns a set containing all the peers of the 
#box specified in the input
#peers are boxes that are in the same unit
"""
def peers(box = None):
    if box:
        return (set( sum(units()[box], []) ) - set([box]) )
    return { b: (set( sum(units()[b], []) ) - set([b])) for b in boxes()}
"""

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    lstgrid = []
    for g in grid:
        if g == '.':
            lstgrid.append('123456789')
        else:
            lstgrid.append(g)
    return {key:value for key, value in zip(boxes, lstgrid)}

"""
The hidden twins technique is not used due to the overhead it introduces in the
tests that are made, however I'll leave the code here

I use parts of code from: 
http://code.activestate.com/recipes/65441-checking-whether-a-string-contains-a-set-of-chars/
"""
#@timeit
def hidden_twins(values):
    """Eliminate values using the hidden twins strategy.
    Does the same as the naked_twins strategy, but this time boxes that form the
    twins may have more values than the twin values. It enforces that these boxes
    can only have values belonging to the twin tuples, and that peers can't have
    the values of the twin tuples.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the hidden twins eliminated from peers.
    """
    for unit in unitslist:
        for tup in twinstuples:
            #to get better performance, it checks first if it is possible that
            #it exists a hidden twin in the unit
            numb = [b for b in unit if len(values[b]) >= len(tup)]
            if len(numb) < len(tup):
                continue
            # checks within the possibilities
            hidden = [ b for b in numb if 0 not in [c in values[b] for c in tup] ]
            if len(hidden) != len(tup):
                continue
            #checks if it is really a twin
            one_timer = [ b for b in unit if 1 in [c in values[b] for c in tup] ]
            if len(hidden) == len(one_timer):
                for twin in hidden:
                    values[twin] = tup
    return values

#@timeit
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    The naked_twins strategy takes a tuple of values that can only be in a certain
    group of boxes, and enforces that no box outside this group can possibly have
    these values
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitslist:
        for tup in twinstuples:
            twins = set(b for b in unit if values[b] == tup)
            if len(twins) == len(tup):
                others = set(peers[twins.pop()])
                for twin in twins:
                    others = others.intersection(peers[twin])
                for other in others:
                    for t in tup:
                        values[other] = values[other].replace(t, '')
                        if len(values[other]) == 1:
                            values = assign_value(values, other, values[other])
    return values
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if not values:
        print (values)
        return
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

def eliminate(values):
    '''
    Eliminate impossible values from the board. After this function,
    the board should have only the possible values for each box.
    What the function does is to inspect definitive values (boxes with only
    one value), and eliminate those values from boxes of the same unit.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): The sudoku in dictionary form
    '''
    for box, val in values.items():
        if len(val) == 1:
            for peer in peers[box]:
                if val in values[peer]:
                    values[peer] = values[peer].replace(val, '')
                    if values[peer] == 1:
                        values = assign_value(values, peer, val)
    return values

def only_choice(values):
    '''
    Pics the only choice of a value to a certain box, having into account the 
    values of the boxe's unit. It checks every box in a certain unit, and
    if there is a value X that can only fit in one box of that unit (that box
    is the only one whose possible values contain value X), it means that only
    that box can have value X, and since every unit must have every value,
    value X must be in that box.
    It runs every possible value, for every box in every unit, and if there is
    a value that fits only in one box (that is not already completed), it gives
    that value to the box.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): The sudoku in dictionary form
    '''
    for unit in unitslist:
        for val in '123456789':
            fits = [box for box in unit if val in values[box]]
            if len(fits) == 1:
                values = assign_value(values, fits[0], val)
    return values                      

def reduce_puzzle(values):
    '''
    It uses both elimination and only_choice in order to reduce the number
    of possible values in every box.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): The sudoku in dictionary form
    '''
    stalled = False
    while not stalled:
        solved_values_before = [box for box, val in values.items() if len(val) == 1]
        values = eliminate(values)
        values = only_choice(values)
        #values = hidden_twins(values)
        values = naked_twins(values)
        solved_values_after = [box for box, val in values.items() if len(val) == 1]
        stalled = len(solved_values_after) == len(solved_values_before)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


#@timeit
def search(values):
    '''
    It reduces the puzzle, using reduce_puzzle. If the puzzle isn't solved by
    reducing, it chooses a possible value for one of the boxes (the one with less possibilities) 
    and repeats the process recursively, returning false when it reaches an 
    impossible solution or returning the solved puzzle if it reaches a possible one.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): The sudoku in dictionary form
    '''
    values = reduce_puzzle(values)
    if not values:
        return False
    if all(len(values[box]) == 1 for box in boxes):
        return values
    box, possibilities = min( (bx, values[bx]) for bx in boxes if len(values[bx]) > 1 )
    for value in values[box]:
        result = values.copy()
        result[box] = value
        result = search(result)
        if result:
            return result
    return False

#@timeit
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
