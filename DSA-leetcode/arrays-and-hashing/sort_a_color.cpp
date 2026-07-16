#include<bits/stdc++.h>
using namespace std;

// int getMax(vector<int> &nums) {
//     int maxVal = nums[0];
//     int n = nums.size();
    
//     for (int i = 1; i < n; i++) {
//         if (nums[i] > maxVal) maxVal = nums[i];
//     }
//     return maxVal;
// }

// void sortColors(vector<int> &nums) {
//      // 2-pass algorithm
//     int n = nums.size();
//     if (n == 0) return;

//     int maxVal = getMax(nums);

//     vector<int> count(maxVal + 1, 0);
//     vector<int> output(n);

//     for (int i = 0; i < n; i++) count[nums[i]]++;

//     for (int i = 1; i <= maxVal; i++) count[i] += count[i - 1];

//     for (int i = n - 1; i >= 0; i--) {
//         output[count[nums[i]] - 1] = nums[i];
//         count[nums[i]]--;
//     }

//     for (int i = 0; i < n; i++) {
//         nums[i] = output[i];
//     }
// }

void sortColors(vector<int>& nums) {
    int low = 0, high = nums.size()- 1, current = 0;

    while (current <= high) {

        if (nums[current] == 0) {
            int temp = nums[current];
            nums[current] = nums[low];
            nums[low] = temp;
            low++;
            current++;
        }

        else if (nums[current] == 1) current++;

        else {
            int temp = nums[current];
            nums[current] = nums[high];
            nums[high] = temp;
            high--;
        }
    }
}

int main()
{
    vector<int> nums = {2,0,2,1,1,0};
    sortColors(nums);

    for(auto e : nums) {
        cout << e << ", ";
    } cout << endl;
    return 0;
}