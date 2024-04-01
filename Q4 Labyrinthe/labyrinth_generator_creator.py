# Maltais, 20244617
# Zhang, 20207461

import sys
import random

cell_size = 10 #mm
wall_height = 10 #mm
wall_thickness = 1 #mm

strategy_choice = 1
tiles_amt = 5


class Strategy :
    def __init__(self):
        pass

    def Apply(self, maze):
        print("Applying Abstract Strategy")

    def DoSomething(self):
        print("Do Something")

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

        for row in maze:
            line = ''
            for elem in row:
                # if(type(elem) == type(1)):
                #     line += ' '
                if(elem == ' '):
                    line += 's'
                else:
                    line += str(elem)
            print(line)

class Algorithm2(Strategy) :

    def Apply(self, maze):
        #super().Apply()
        print("Applying Algorithm2")

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

# Cube de cote
# translate([115.0,50.0,5.0]){
# cube([11,1,10], center=true);
# }

class Creator() :
    def __init__(self):
        pass

    def PrintLabyrinth(self):
        pass


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
    my_generator.Generate()

    #Creator
    my_creator = Creator()
    my_creator.PrintLabyrinth()


if __name__ == "__main__":
    main()
