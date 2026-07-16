#include<bits/stdc++.h>
using namespace std;

// vector<int> productExceptSelf(vector<int>& nums) {
//     // time: O(n), space: O(n)
//     vector<int> res(nums.size(), 1);
//     vector<int> left(nums.size(), 1);
//     vector<int> right(nums.size(), 1);

//     left[1] = nums[0];
//     for (int i = 2; i < nums.size(); i++) {
//         left[i] = left[i - 1] * nums[i - 1];
//     }

//     right[nums.size() - 2] = nums[nums.size() - 1];
//     for (int i = nums.size() - 3; i >= 0; i--) {
//         right[i] = nums[i + 1] * right[i + 1];
//     }

//     for (int i = 0; i < nums.size(); i++) {
//         res[i] = left[i] * right[i];
//     }

//     return res;
// }

vector<int> productExceptSelf(vector<int>& nums) {
    // time: O(n), space: O(1)
    int n = nums.size();
    vector<int> res(n, 1);

    for (int i = 1; i < n; i++) {
        res[i] = res[i - 1] * nums[i - 1];
    }

    int right_product = 1;
    for (int i = n - 1; i >= 0; i--) {
        res[i] = res[i] * right_product;
        right_product = right_product * nums[i]; 
    }

    return res;
}

int main()
{
    vector<int> nums = {-1, 1, 0, -3, 3};
    vector<int> res = productExceptSelf(nums);

    for(auto e : res) {
        cout << e << " - ";
    } cout << endl;
    return 0;
}