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

int ClimbingDifficultyCalculator::CalculateClimbingDifficulty(std::string filename) {
    ifstream file("../Q2 Escalade/" + filename);
    if (!file) {
        cerr << "Failed to open file: " << filename << endl;
        return -1;
    }

    string line;
    while (getline(file, line)) {
        istringstream iss(line);
        vector<int> row;
        string difficultyStr;

        while (getline(iss, difficultyStr, ',')) {
            row.push_back(std::stoi(difficultyStr));
        }
        wall.push_back(row);
    }
    file.close();

    // debugging
    cout << "Wall Matrix:" << endl;
    for (const auto& row : wall) {
        for (int cell : row) {
            cout << cell << " ";
        }
        cout << endl;
    }

    m = wall.size();
    n = wall[0].size();
    dp.assign(m, std::vector<int>(n, -1)); // Initialize memoization matrix

    // Initialize the bottom row of dp with the bottom row of the wall matrix
    for (int c = 0; c < n; ++c) {
        dp[m-1][c] = wall[m-1][c];
    }

    int minCost = numeric_limits<int>::max();
    for (int c = 0; c < n; ++c) {
        minCost = min(minCost, calculateMinCost(0, c));
    }

    // debugging
    cout << "DP Memo Matrix:" << endl;
    for (const auto& row : dp) {
        for (int cost : row) {
            if (cost == numeric_limits<int>::max()) {
                cout << "X "; // Use 'X' or a similar placeholder for uninitialized or max int values
            } else {
                cout << cost << " ";
            }
        }
        cout << endl;
    }

    return minCost;
}

void override_left(vector<int> row, vector<int> override_costs, int pos){
    if(pos <= 0){
        return;
    }

    if(row[pos] < override_costs[pos - 1]){
        row[pos - 1] = row[pos - 1] - override_costs[pos - 1] + row[pos];
        override_costs[pos - 1] = row[pos];
        override_left(row, override_costs, pos);
    }

}

int dingdong(int m) {

    int r = 0;

    int elements = dp[0].size();

    vector<int> override_costs;
    int curr = 0;
    int will_try_override = 0;

    while(dp.size() > 1){
        vector<int> bottom = dp.pop();
        curr = dp.size() -1; // Avant dernier row, donc en haut de bottom row.

        for(int i=0; i<elements; i++){
            //down
            will_try_override = 0;
            int down_cost = bottom_row[element];
            int final_cost = down_cost;
            
            //left
            if(i != 0){
                
                int left_cost = dp[curr][i - 1];
                if( down_cost < left_cost){
                    will_try_override = 1;
                }
                else{
                    final_cost = left_cost;

                }
            
            }
            dp[curr][element] += final_cost; // dp[curr][element] = 52 ; final_cost = 30;
            override_costs.push_back(final_cost);
            if(will_try_override == 1){
                override_left(dp[curr], override_costs, i);
            }
        }
        override_costs.clear();
    }

    vector<int> bottom = dp.pop();
    int curr_min = bottom[0];
    for(int i = 0; i<bottom.size(); i++){
        if(curr_min > bottom[i]){
            curr_min = bottom[i];
        }
    }

    return curr_min; //Sol
}

int ClimbingDifficultyCalculator::calculateMinCost(int r, int c) {
    if (c < 0 || c >= n) return numeric_limits<int>::max(); // Out of bounds check for columns
    if (r == m-1) return wall[r][c]; // Base case: bottom row

    if (dp[r][c] != -1) return dp[r][c]; // Use memoized result if available

    // Recursive calls to find minimum cost from cell directly below, left below, and right below
    int downCost = calculateMinCost(r + 1, c);
    int costLeft = c > 0 ? calculateMinCost(r + 1, c - 1) : numeric_limits<int>::max();
    int costRight = c < n - 1 ? calculateMinCost(r + 1, c + 1) : numeric_limits<int>::max();

    // Accumulate cost and memoize
    dp[r][c] = wall[r][c] + min({downCost, costLeft, costRight});

    // debugging
    cout << "Calculating Min Cost for (" << r << ", " << c << "): "
         << "DownCost: " << downCost << ", LeftCost: " << costLeft << ", RightCost: " << costRight
         << ", Chosen Cost: " << dp[r][c] << endl;

    return dp[r][c];
}