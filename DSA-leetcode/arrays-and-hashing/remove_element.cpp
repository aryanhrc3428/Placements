#include<bits/stdc++.h>
using namespace std;

int removeElement(vector<int>& nums, int val) {
    int k = 0;
    for (int j =0;j<nums.size();j++) {
            if (nums[j] != val) {
                nums[k] = nums[j];
                k++;
            }
        }
    return k;
}

int main()
{
    vector<int> nums1 = {3,2,2,3};
    vector<int> nums2 = {0,1,2,2,3,0,4,2};

    int res1 = removeElement(nums1, 3);
    int res2 = removeElement(nums2, 2);

    cout << res1 << " - " << res2;
    return 0;
}