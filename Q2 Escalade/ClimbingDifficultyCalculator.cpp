/// Maltais, 20244617
// Zhang, 20207461

#include "ClimbingDifficultyCalculator.h"
#include <fstream>
#include <vector>
#include <unordered_set>
#include <cmath>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <limits>

using namespace std;

// ce fichier contient les definitions des methodes de la classe ClimbingDifficultyCalculator
// this file contains the definitions of the methods of the ClimbingDifficultyCalculator class

ClimbingDifficultyCalculator::ClimbingDifficultyCalculator()
{
}

int ClimbingDifficultyCalculator::CalculateClimbingDifficulty(string filename)
{
    ifstream file("../Q2 Escalade/" + filename);
    if (!file) {
        cerr << "Failed to open file: " << filename << endl;
        return -1;
    }

    string line;
    vector<vector<int>> wall; // Dynamic 2D array

    while (getline(file, line)) {
        istringstream iss(line);
        vector<int> row;
        string difficultyStr;

        while (getline(iss, difficultyStr, ',')) {
            try {
                int difficulty = stoi(difficultyStr); // Convert string to integer
                row.push_back(difficulty);
            } catch (const exception& e) {
                cerr << "Error parsing integer from string \"" << difficultyStr << "\": " << e.what() << endl;
                return -1;
            }
        }
        if (!row.empty()) {
            wall.push_back(row);
        }
    }
    file.close();

    int m = wall.size();                                    // Number of rows
    if (m == 0 || (m > 0 && wall[0].size() == 0)) {
        cout << "Wall is empty or malformed." << endl;
        return 0;
    }
    int n = wall[0].size();                                 // Number of columns

    // Wall with only one row
    if (m == 1) {
        return *min_element(wall[0].begin(), wall[0].end());
    }

    // Wall with only one column
    if (n == 1){
        int sum = 0;
        for (int i = 0; i < m; ++i) {
            sum += wall[i][0];
        }
        return sum;
    }

    vector<vector<int>> dp(m, vector<int>(n));

    // Initialize bottom row of DP table
    for (int j = 0; j < n; ++j) {
        dp[m-1][j] = wall[m-1][j];
    }

    // Fill the DP table
    for (int i = m-2; i >= 0; --i) {            // Start from the second to last row
        for (int j = 0; j < n; ++j) {
            int upCost = dp[i+1][j];                                                    // Cost from above
            int leftCost = (j > 0) ? dp[i+1][j-1] : numeric_limits<int>::max();        // Left
            int rightCost = (j < n-1) ? dp[i+1][j+1] : numeric_limits<int>::max();     // Right

            // Cost of the current cell itself (wall[i][j]) + the minimum of the three possible paths leading to it
            dp[i][j] = wall[i][j] + min({upCost, leftCost, rightCost});
        }
    }

    // Debug (print populated dp)
    cout << "DP Matrix:" << endl;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cout << dp[i][j] << " ";
        }
        cout << endl; // Newline at the end of each row for better readability
    }

    return *min_element(dp[0].begin(), dp[0].end());
}