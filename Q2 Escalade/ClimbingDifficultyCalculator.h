// Maltais, 20244617
// Zhang, 20207461

#include <vector>
#include <string>

// ce fichier contient les declarations des methodes de la classe ClimbingDifficultyCalculator
// peut être modifié si vous voulez ajouter d'autres méthodes à la classe
// this file contains the declarations of the methods of the ClimbingDifficultyCalculator class
// can be modified if you wish to add other methods to the class

class ClimbingDifficultyCalculator
{
public:
    ClimbingDifficultyCalculator();
    int CalculateClimbingDifficulty(std::string);

private:
    std::vector<std::vector<int>> wall;
    std::vector<std::vector<int>> dp; 
};