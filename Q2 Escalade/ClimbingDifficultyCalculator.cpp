/// Maltais, 20244617
// Zhang, 20207461

#include "ClimbingDifficultyCalculator.h"
#include <fstream>
#include <vector>
#include <unordered_set>
#include <math.h>
#include <algorithm>
#include <iostream>
#include <sstream>

// ce fichier contient les definitions des methodes de la classe ClimbingDifficultyCalculator
// this file contains the definitions of the methods of the ClimbingDifficultyCalculator class

ClimbingDifficultyCalculator::ClimbingDifficultyCalculator()
{
}

int ClimbingDifficultyCalculator::CalculateClimbingDifficulty(string filename)
{
    std::ifstream file(filename);
    std::string line;
    std::vector<std::vector<int>> wall;                          // Dynamic 2D array

    // Read file and construct wall matrix
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::vector<int> row;
        std::string difficultyStr;
        while (std::getline(iss, difficultyStr, ',')) { 
            int difficulty = std::stoi(difficultyStr);          // Convert string to integer
            row.push_back(difficulty);
        }
        wall.push_back(row);
    }
    file.close();
    
    int m = wall.size();
    if (m == 0) return 0;
    int n = wall[0].size();

    std::vector<std::vector<int>> dp(m, std::vector<int>(n));

    // Initialize base case (mth row)
    for (int j = 0; j < n; ++j) {
        dp[m-1][j] = wall[m-1][j];
    }

    // DP calculation from bottom to top
    for (int i = m - 2; i >= 0; --i) {
        for (int j = 0; j < n; ++j) {
            int up = dp[i + 1][j];
            int leftUp = (j > 0) ? dp[i + 1][j - 1] : std::numeric_limits<int>::max();
            int rightUp = (j < n - 1) ? dp[i + 1][j + 1] : std::numeric_limits<int>::max();
            dp[i][j] = wall[i][j] + std::min({up, leftUp, rightUp});
        }
    }

    // Find the minimum difficulty path to the top
    int minPathDifficulty = std::numeric_limits<int>::max();
    for (int j = 0; j < n; ++j) {
        if (dp[0][j] < minPathDifficulty) {
            minPathDifficulty = dp[0][j];
        }
    }

    return minPathDifficulty;
}
