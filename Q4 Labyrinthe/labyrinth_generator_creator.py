# Maltais, 20244617
# Zhang, 20207461

import sys
import random

cell_size = 10 #mm
wall_height = 10 #mm
wall_thickness = 1 #mm

strategy_choice = 2
tiles_amt = 13


class Strategy :
    def __init__(self):
        pass

    def Apply(self, maze):
        print("Applying Abstract Strategy")

    def DoSomething(self):
        pass

class Algorithm1(Strategy) :
    def initialiser(self, ligne, d):
        i = 1
        while(i < len(ligne)):
            if ligne[i] == ' ':
                chiffre = 1
                while(chiffre in d):
                    chiffre += 1
                ligne[i] = chiffre
                d[chiffre] = 1
            i += 2

    def placer_mur_cote(self, ligne, d):

        i = 1 
        prev = ' '
        while(i < len(ligne)-3):
            choice = random.choice([True, False])
            if ligne[i] == ligne[i + 2]:
                ligne[i + 1] = '|'
            else:
                if choice:
                    d[ligne[i]] += 1
                    d[ligne[i + 2]] -= 1
                    if(d[ligne[i+ 2]] == 0):
                        del d[ligne[i+ 2]]
                    ligne[i + 2] = ligne[i]
                    ligne[i + 1] = ' '
                else:
                    ligne[i + 1] = '|'
            i += 2

    def placer_mur_dessous(self, ligne, d, maze):
        dessous = []
        i = 1

        while(i < len(ligne)):
            if(d[ligne[i]] == 1):
                dessous.append(" ")
            else:
                choice = random.choice([True, False])
                if choice:
                    dessous.append("_")
                    d[ligne[i]] -= 1
                    ligne[i] = " "
                else:
                    dessous.append(" ")
            i += 2
        
        maze.append(dessous)
        maze.append(maze[-2].copy())

    def Apply(self, maze):
        #super().Apply()
        # maze.append("|")
        row = []
        for _ in range(tiles_amt):
            row.append("_")
        maze.append(row)
        
        row = []
        row.append('|')
        for i in range(tiles_amt*2 - 1):
            row.append(" ")
        row.append('|')
        maze.append(row)

        d = {}
        # Pour que ce soit carrés
        for _ in range(tiles_amt):
            
            self.initialiser(maze[-1], d)
            self.placer_mur_cote(maze[-1], d)
            self.placer_mur_dessous(maze[-1], d, maze)

        maze.pop()
        maze.pop()
        row = []
        for _ in range(tiles_amt):
            row.append("_")
        maze.append(row)

        for i in range(1, len(maze), 2):
            newRow = []
            for elem in range(0, len(maze[i]), 2):
                newRow.append(maze[i][elem])

            maze[i] = newRow

        new_final = []
        for elem in maze[-2]:
            new_final.append(" ")
        new_final.pop()
        new_final.append("|")
        maze[-2] = new_final
        maze[1].pop()
        maze[1].append(" ")

        # for row in maze:
        #     line = ''
        #     for elem in row:
        #         # if(type(elem) == type(1)):
        #         #     line += ' '
        #         if(elem == ' '):
        #             line += 's'
        #         else:
        #             line += str(elem)
        #     print(line)

#Random dfs
class Algorithm2(Strategy) :


    def not_visited_neighbors(self, visited, current):
        not_visited = []
        x = current[0]
        y = current[1]
        #Gauche
        if(x - 1 >= 0):
            if(not visited[x-1][y]):
                not_visited.append("Gauche")
        #Droite
        if(x + 1 < len(visited)):
            if(not visited[x+1][y]):
                not_visited.append("Droite")
        #Haut
        if(y + 1 < len(visited)):
            if(not visited[x][y + 1]):
                not_visited.append("Haut")
        #Bas
        if(y - 1 >= 0):
            if(not visited[x][y - 1]):
                not_visited.append("Bas")

        return not_visited

    def Apply(self, maze):
        visited = []
        bottom_walls = []
        right_walls = []
        visited_stack = []
        to_visit = -1
        for _ in range(tiles_amt):
            top_row = []
            bottom_row = []
            visited_row = []
            for _ in range(tiles_amt):
                visited_row.append(False)
                to_visit += 1
                bottom_row.append("_")
                top_row.append("|")
                
            top_row.append("|")
            visited.append(visited_row)
            bottom_walls.append(top_row)
            right_walls.append(bottom_row)

        
        visited[0][0] = True
        visited_stack.append([0,0])

        while(to_visit > 0):
            curr = visited_stack.pop()
            choices = self.not_visited_neighbors(visited, curr)
            if(len(choices) == 0):
                pass
                    
            else:
                direction = random.choice(choices)
                nextCell = [curr[0], curr[1]]
                if direction == "Bas":
                    bottom_walls[curr[0]][curr[1]] = " "
                    nextCell[1] -= 1
                elif direction == "Haut":
                    bottom_walls[curr[0]][curr[1] + 1] = " "
                    nextCell[1] += 1
                elif direction == "Droite":
                    right_walls[curr[0]][curr[1]] = " "
                    nextCell[0] += 1
                elif direction == "Gauche":
                    right_walls[curr[0] - 1][curr[1]] = " "
                    nextCell[0] -= 1
                
                to_visit -= 1
                visited_stack.append(curr)
                visited_stack.append(nextCell)
                visited[nextCell[0]][nextCell[1]] = True

        row = []
        for _ in range(tiles_amt):
            row.append("_")
        maze.append(row)
        

        for i in range(len(bottom_walls)):
            maze.append(right_walls[i])
            maze.append(bottom_walls[i])
        
        maze[2].pop(0)
        maze[2].insert(0," ")
        maze[-1].pop()
        maze[-1].append(" ")

class Generator() :
    strategy = None
    labyrinthe = []

    def __init__(self):
        pass

    def SetStrategy(self, new_strategy):
        self.strategy = new_strategy

    def Generate(self):
        self.strategy.Apply(self.labyrinthe)
        self.strategy.DoSomething()
        return self.labyrinthe



class Creator() :
    file = "tgl.scad"
    initialString = f"""
    // Labyrinth generated for openscad
    // IFT2125 - H24
    // Authors : Samuel Maltais et Celina Zhang
    difference(){{
    union(){{
    // base plate
    translate([-0.5,-0.5,-1]){{
    cube([{cell_size * tiles_amt + 1},{cell_size * tiles_amt + 1}, 1.0], center=false);
    }}"""

    endOfString = """
    // logo
    translate([1,-0.2,1]){
    rotate([90,0,0]){
    linear_extrude(1) text( "CELINA ET SAM GOATS", size= 7.0);
    }
    }
    }
    }
    """

    def __init__(self):
        pass

    def horizontal_wall(self, horizontal_offset, vertical_offset):
        return f"""
                    translate([{horizontal_offset  + cell_size/2},{vertical_offset},{cell_size / 2}]){{
                    cube([{cell_size + 1},{wall_thickness},{cell_size}], center=true);
                    }}\n
            """
    def vertical_wall(self, horizontal_offset, vertical_offset):
        return f"""
                    translate([{horizontal_offset},{vertical_offset - cell_size/2},{cell_size / 2}]){{
                    rotate([0,0,90]){{
                    cube([{cell_size + 1},{wall_thickness},{cell_size}], center=true);
                    }}
                    }}
                    \n
            """


    def make_row(self,vertical_offset, row):
        offset = 0
        ourStr = ""
        i = 0
        while(i < len(row)):

            row[i] = str(row[i])

            if(row[i] == '|'):
                ourStr += self.vertical_wall(offset,vertical_offset)
            elif(row[i] == '_'):
                ourStr += self.horizontal_wall(offset, vertical_offset)

            offset += cell_size
            i += 1

        return ourStr

    def PrintLabyrinth(self, maze):
        offset = 0
        finalCode = self.initialString

        i = 0
        for row in maze:
            finalCode += self.make_row(offset,row)
            if(i % 2 == 0):
                offset += cell_size
            i += 1
        finalCode += self.endOfString
        
        f = open(self.file, 'w')
        f.write(finalCode)
        f.close

# main call
def main():
    global strategy_choice
    args = sys.argv[:]
    if len(args) >= 2 :
        strategy_choice = int(args[1])

    # Generator
    my_generator = Generator()
    if strategy_choice == 1:
        my_generator.SetStrategy(Algorithm1())
    elif strategy_choice == 2:
        my_generator.SetStrategy(Algorithm2())
    else :
        print("error strategy choice")
    maze = my_generator.Generate()

    #Creator
    my_creator = Creator()
    my_creator.PrintLabyrinth(maze)


if __name__ == "__main__":
    main()
