#include<bits/stdc++.h>
using namespace std;

int longestConsecutive(vector<int>& nums) {
    if (nums.empty()) return 0;

    unordered_set<int> Set(nums.begin(), nums.end());
    int longestSequence = 0;

    for (int num : Set) {
        if (Set.find(num - 1) == Set.end()) {
            int currentNum = num;
            int currentSequence = 1;

            while (Set.find(currentNum + 1) != Set.end()) {
                currentNum++;
                currentSequence++;
            }
            longestSequence = max(longestSequence, currentSequence);
        }
    }
    return longestSequence;
}

int main()
{
    return 0;
}