# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Sudoku can be seen as a Constraint Statisfaction Problem (CSP), that has a set of variables (the values of the boxes in the grid), the domain of the variables (the values the boxes can take, 1 to 9), and a set of constraints (the constraint that the same number can't be repeated in a unit, for example). In CSPs one can choose: to do a search by assigning a value to a variable, from within the possible values, and try to solve the CSP with that particular assignment; or to apply constraint propagation, by using constraints to reduce the number of possible values a variable can have, that will in turn increase the number of constraints and reduce in turn the number of possible values of another variable.

The naked twins strategy looks boxes that share the same tuple of possible values (have the same possible values), knowing that each one of those boxes must contain one of the values of the tuple (as given in the description of the problem, using a tuple of possible values of size 2). With this, we can induce that every other box in the same unit can't have any of the values of the tuple. This is one more constraint to be included in the Sudoku game, that will reduce the number of possible values to each box.

To implement the naked twins strategy I iterate every possible tuple of values with size  2 (although the strategy can be used with tuples with any size), and check which boxes have this tuple as possible values. If the number of boxes that have the tuple as possible value is the same as the size of the tuple, I found naked twins, and can remove the values of the tuple from the rest of the boxes in the same unit.

As a bonus I've also implemented the hidden twins strategy (although I don't use it, because the overhead that introduces isn't worth it). This strategy is the same as the naked twins strategy, but the "twin" boxes can have more values than the tuple being iterated, and these are the values being eliminated. It could also eliminate the tuple values from the rest of the boxes in the same unit (as the naked twins did), but I prefered to let that work be done by the naked twins strategy instead, since I'm using the naked twins strategy after the hidden twins one in the reduce puzzle step. This way the hidden twins strategy creates "naked twins" that are used by the naked twins strategy.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We use constraint propagation to solve the diagonal sudoku problem by simply adding the constraint that the two big diagonals of the grid form a unit as well. Since the constraints for units are already defined, by doing this the constraints applied before to the other units will also apply for the diagonals, transforming the normal sudoku into a diagonal sudoku problem.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

