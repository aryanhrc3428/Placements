#include<bits/stdc++.h>
using namespace std;

vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int,int> hash;

    for(int i = 0; i < nums.size(); i++) {
        hash[nums[i]]++;
    }

    vector<vector<int>> bucket(nums.size() + 1);
    for (auto pair : hash) {
        bucket[pair.second].push_back(pair.first);
    }

    vector<int> res;
    for (int i = bucket.size() - 1; i >= 0; i--) {
        for (auto e : bucket[i]) {
            res.push_back(e);
            if (res.size() == k) return res;
        }
    }
    return {};
}

int main()
{
    vector<int> nums = {1,1,1,2,2,3}; // ans -> [1,2]
    int k = 2;

    vector<int> res = topKFrequent(nums,k);

    for(auto e : res) {
        cout << e << " - ";
    } cout << endl;

    return 0;
}