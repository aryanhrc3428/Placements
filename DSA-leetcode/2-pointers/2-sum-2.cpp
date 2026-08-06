#include<bits/stdc++.h>
using namespace std;

vector<int> twoSum(vector<int>& numbers, int target) {
    int start = 0;
    int end = numbers.size() - 1;

    while (start < end) {
        int sum = numbers[start] + numbers[end];

        if (sum == target) return {start + 1, end + 1};
        else if (sum < target) start++;
        else end--;
    }
    
    return {-1, -1};

}

int main()
{
    vector<int> numbers = {2,7,11,15};
    int target = 9;
    vector<int> res = twoSum(numbers, target);
    cout << "index 1: " << res[0] << endl;
    cout << "index 2: " << res[1] << endl;
    return 0;
}