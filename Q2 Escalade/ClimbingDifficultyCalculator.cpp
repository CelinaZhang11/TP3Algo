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

void override_left(vector<int> row, vector<int> override_costs, int pos)
{

    cout << "Failed to go left" << row[pos - 1] << endl;
}

int dingdong(int m, std::vector<vector<int>> wall2)
{

    int r = 0;

    int elements = wall2[0].size();

    vector<int> override_costs;
    int curr = 0;
    int will_try_override = 0;

    while (wall2.size() > 1)
    {
        vector<int> bottom_row = wall2[wall2.size() - 1];
        wall2.pop_back();

        curr = wall2.size() - 1;                                    // Avant dernier row, donc en haut de bottom row

        for (int i = 0; i < elements; i++)
        {
            // Down
            will_try_override = 0;
            int down_cost = bottom_row[i];
            int final_cost = down_cost;

            // Left
            if (i != 0)
            {
                int left_cost = wall2[curr][i - 1];
                if (down_cost < left_cost)
                {
                    will_try_override = 1;
                }
                else
                {
                    final_cost = left_cost;
                }
            }

            wall2[curr][i] += final_cost;                           // wall2[curr][element] = 52 ; final_cost = 30;
            override_costs.push_back(final_cost);
            if (will_try_override == 1)
            {
                int pos = i;
                while (pos > 0)
                {
                    if (wall2[curr][pos] < override_costs[pos - 1])
                    {
                        wall2[curr][pos - 1] = wall2[curr][pos - 1] - override_costs[pos - 1] + wall2[curr][pos];
                        override_costs[pos - 1] = wall2[curr][pos];
                        pos -= 1;
                    }
                    else
                    {
                        pos = -1;
                    }
                }
            }
        }
        override_costs.clear();
    }

    vector<int> bottom_row = wall2[wall2.size() - 1];
    wall2.pop_back();
    int curr_min = bottom_row[0];
    for (int i = 0; i < bottom_row.size(); i++)
    {
        if (curr_min > bottom_row[i])
        {
            curr_min = bottom_row[i];
        }
    }

    return curr_min;                                               // Solution
}

int ClimbingDifficultyCalculator::CalculateClimbingDifficulty(std::string filename)
{
    ifstream file("../Q2 Escalade/" + filename);
    if (!file)
    {
        cerr << "Failed to open file: " << filename << endl;
        return -1;
    }

    string line;
    wall.clear();
    while (getline(file, line))
    {
        istringstream iss(line);
        vector<int> row;
        string difficultyStr;

        while (getline(iss, difficultyStr, ','))
        {
            row.push_back(std::stoi(difficultyStr));
        }
        wall.push_back(row);
    }
    file.close();

    return dingdong(0, wall);
}