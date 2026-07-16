#include<bits/stdc++.h>
using namespace std;

vector<int> majorityElement(vector<int>& nums){
    // Boyer-Moore Voting Algorithm (battle royale)
    vector<int> candidates;
    int candidate = -1;
    int count = 0;

    for (int i = 0; i < nums.size(); i++) {
        if (count == 0) candidate = nums[i];
        if (nums[i] == candidate) count++;
        else count--;
    }

    return candidates;
}

int main()
{
    return 0;
}