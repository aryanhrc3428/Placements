#include<bits/stdc++.h>
using namespace std;

// int majorityElement(vector<int>& nums) {
//     unordered_map<int,int> hash;

//     for (int i = 0; i < nums.size(); i++) {
//         hash[nums[i]]++;
//     }

//     for (auto const& pair : hash) {
//         int current_num = pair.first;
//         int frequency = pair.second;
        
//         if (frequency > nums.size()/2) {
//             return current_num;
//         }
//     }

//     return -1;
// }

int majorityElement(vector<int>& nums){
    // Boyer-Moore Voting Algorithm (battle royale)
    int candidate = -1, count = 0;

    for (int i = 0; i < nums.size(); i++) {
        if (count == 0) candidate = nums[i];
        if (nums[i] == candidate) count++;
        else count--;
    }

    return candidate;
}

int main()
{
    vector<int> nums1 = {3,2,3};
    vector<int> nums2 = {2,2,1,1,1,2,2};

    int res1 = majorityElement(nums1);
    int res2 = majorityElement(nums2);

    cout << res1 << " - " << res2 << endl;
    return 0;
}