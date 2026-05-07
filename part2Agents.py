from model import (
    Location,
    Wizard,
    IceStone,
    FireStone,
    WizardMoves,
    GameAction,
    GameState,
    WizardSpells, NeutralStone,
)
from agents import WizardAgent


import z3
from z3 import (Solver, Bool, Bools, Int, Ints, Or, Not, And, Implies, Distinct, If)



class PuzzleWizard(WizardAgent):


    def react(self, state: GameState) -> WizardMoves:
        fire_stones = state.get_all_tile_locations(FireStone)
        ice_stones = state.get_all_tile_locations(IceStone)
        grid_size = state.grid_size
        wizard_location = state.active_entity_location

        START = 1 
        Turn = 2
        Straight = 3
        Passed = 4
        
        s = Solver()
        fire_positions = {(f.row, f.col) for f in fire_stones}
        ice_positions = {(ice.row, ice.col) for ice in ice_stones}
        
        X = [[Int(f"{i}_{j}") for j in range(grid_size[0])] for i in range(grid_size[1])]

        for i in range(grid_size[1]):
            for j in range(grid_size[0]):
                if i == wizard_location.col and j == wizard_location.row:
                    s.add(X[i][j] == START) 
                
                elif (i,j) in fire_positions:
                    s.add(X[i][j] == Turn)
                
                elif (i,j) in ice_positions:
                    s.add(X[i][j] == Straight)
                    
        

                    
        match s.check():
            case z3.sat:
                    m = s.model()

                    grid = [
                    [
                    m.evaluate(X[i][j], model_completion=True).as_long()
                    for j in range(len(X[0]))
                    ]
                        for i in range(len(X))
                            ]
                    path = []
                    for i in range(len(grid)):
                        for j in range(len(grid[0])):
                            if grid[i][j] != 0:
                                if grid[i][j] == 1:
                                    SP = len(path)
                                    path.append([[i,j], START])
                                elif grid[i][j] == 2:
                                    path.append([[i,j], Turn])
                                elif grid[i][j] == 3:
                                    path.append([[i,j], Straight])

                    Wiz_Actions = []
                    while (1):
                        if (SP + 1) == len(path):
                            second = 0
                        else:
                            second = SP + 1

                        
                        current = path[SP]
                        next_stone = path[second]
            
                        if next_stone[1] == START:
                            break
                        
                        if current[1] == Turn and Wiz_Actions != [] and (Wiz_Actions[-1] == WizardMoves.LEFT or Wiz_Actions[-1] == WizardMoves.RIGHT):
                            vertical = next_stone[0][0] - current[0][0]
                            if vertical > 0:
                                for k in range(vertical):
                                    Wiz_Actions.append(WizardMoves.UP)
                            elif vertical < 0:
                                for l in range (vertical):
                                    Wiz_Actions.append(WizardMoves.DOWN)
                            
                            horizontal = next_stone[0][1] - current[0][1]

                            if horizontal > 0:
                                for k in range(horizontal):
                                    Wiz_Actions.append(WizardMoves.RIGHT)
                            elif horizontal < 0:
                                for l in range (horizontal):
                                    Wiz_Actions.append(WizardMoves.LEFT)
                        else:

                            horizontal = next_stone[0][1] - current[0][1]

                            if horizontal > 0:
                                for k in range(horizontal):
                                    Wiz_Actions.append(WizardMoves.RIGHT)
                            elif horizontal < 0:
                                for l in range (horizontal):
                                    Wiz_Actions.append(WizardMoves.LEFT)
                        
                            vertical = next_stone[00][0] - current[0][0]
                            if vertical > 0:
                                for k in range(vertical):
                                    Wiz_Actions.append(WizardMoves.UP)
                            elif vertical < 0:
                                for l in range (vertical):
                                    Wiz_Actions.append(WizardMoves.DOWN)
                        
                        SP += 1
                        if SP == len(path):
                            SP = 0
                        
                    print("VAILD SOLUTION:",Wiz_Actions, "\n")
                        

                    

            case z3.unsat:
                print("Wizard can't complete this puzzle")            
        
    
        return MASYU_1_SOLUTION.pop(0)




class SpellCastingPuzzleWizard(WizardAgent):

    def react(self, state: GameState) -> GameAction:
        fire_stones = state.get_all_tile_locations(FireStone)
        ice_stones = state.get_all_tile_locations(IceStone)
        neutral_stones = state.get_all_tile_locations(NeutralStone)

        grid_size = state.grid_size
        wizard_location = state.active_entity_location


        START = 1 
        Turn = 2
        Straight = 3
        Passed = 4
        Turn_Fire = 5
        Turn_Ice = 6
        
        s = Solver()
        fire_positions = {(f.row, f.col) for f in fire_stones}
        ice_positions = {(ice.row, ice.col) for ice in ice_stones}
        neutral_positions = {(n.row, n.col) for n in neutral_stones}
        
        X = [[Int(f"{i}_{j}") for j in range(grid_size[0])] for i in range(grid_size[1])]

        for i in range(grid_size[1]):
            for j in range(grid_size[0]):
                if i == wizard_location.col and j == wizard_location.row:
                    s.add(X[i][j] == START) 
                
                elif (i,j) in fire_positions:
                    s.add(X[i][j] == Turn)
                
                elif (i,j) in ice_positions:
                    s.add(X[i][j] == Straight)
                
                elif (i,j) in neutral_positions:
                    s.add(Or(X[i][j] == Turn_Fire, X[i][j] == Turn_Ice))
                    
        

                    
        match s.check():
            case z3.sat:
                    m = s.model()

                    grid = [
                    [
                    m.evaluate(X[i][j], model_completion=True).as_long()
                    for j in range(len(X[0]))
                    ]
                        for i in range(len(X))
                            ]
                    path = []
                    for i in range(len(grid)):
                        for j in range(len(grid[0])):
                            if grid[i][j] != 0:
                                if grid[i][j] == 1:
                                    SP = len(path)
                                    path.append([[i,j], START])
                                elif grid[i][j] == 2:
                                    path.append([[i,j], Turn])
                                elif grid[i][j] == 3:
                                    path.append([[i,j], Straight])
                                elif grid[i][j] == 5:
                                    path.append([[i,j], Turn_Fire])
                                elif grid[i][j] == 6:
                                    path.append([[i,j], ice_Fire])

                    Wiz_Actions = []
                    while (1):
                        if (SP + 1) == len(path):
                            second = 0
                        else:
                            second = SP + 1

                        
                        current = path[SP]
                        next_stone = path[second]
                        if next_stone[1] == START:
                            break
                        
                        if current[1] == Turn_Fire:
                            Wiz_Actions.append(WizardSpells.FIREBALL)

                        elif current[1] == Turn_Ice:
                            Wiz_Actions.append(WizardSpells.FREEZE)

                        if current[1] == Turn or current[1]== Turn_Fire and Wiz_Actions != [] and (Wiz_Actions[-1] == WizardMoves.LEFT or Wiz_Actions[-1] == WizardMoves.RIGHT):
                            vertical = next_stone[0][0] - current[0][0]
                            if vertical > 0:
                                for k in range(vertical):
                                    Wiz_Actions.append(WizardMoves.UP)
                            elif vertical < 0:
                                for l in range (vertical):
                                    Wiz_Actions.append(WizardMoves.DOWN)
                                                
                            horizontal = next_stone[0][1] - current[0][1]

                            if horizontal > 0:
                                for k in range(horizontal):
                                    Wiz_Actions.append(WizardMoves.RIGHT)
                            elif horizontal < 0:
                                for l in range (horizontal):
                                    Wiz_Actions.append(WizardMoves.LEFT)
                        else:
                            horizontal = next_stone[0][1] - current[0][1]
                            if horizontal > 0:
                                for k in range(horizontal):
                                    Wiz_Actions.append(WizardMoves.RIGHT)
                            elif horizontal < 0:
                                for l in range (horizontal):
                                    Wiz_Actions.append(WizardMoves.LEFT)
                                            
                            vertical = next_stone[0][0] - current[0][0]
                            if vertical > 0:
                                for k in range(vertical):
                                    Wiz_Actions.append(WizardMoves.UP)
                            elif vertical < 0:
                                for l in range (vertical):
                                    Wiz_Actions.append(WizardMoves.DOWN)
                        
                        SP += 1
                        if SP == len(path):
                            SP = 0

                    print("VAILD SOLUTION:",Wiz_Actions, "\n")
                        

                    

            case z3.unsat:
                print("Wizard can't complete this puzzle")  

"""
Here are some reference solutions for some of the included puzzle maps you can use to help you test things
"""

MASYU_1_SOLUTION =[WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.UP,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.RIGHT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.UP,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.UP,WizardMoves.UP,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.UP]


MASYU_2_SOLUTION =[WizardMoves.RIGHT,WizardSpells.FIREBALL,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.UP,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.RIGHT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.UP,WizardMoves.UP,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.DOWN,WizardSpells.FREEZE,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.LEFT,WizardMoves.DOWN,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.UP,WizardMoves.RIGHT,WizardMoves.UP,WizardMoves.UP,WizardMoves.UP,WizardMoves.LEFT,WizardMoves.UP,WizardMoves.UP,WizardSpells.FIREBALL,WizardMoves.RIGHT]
