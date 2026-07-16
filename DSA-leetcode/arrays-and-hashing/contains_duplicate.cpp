#include <bits/stdc++.h>
using namespace std;

int main()
{
    int arr[3] = {1, 2, 3};
    int n = sizeof(arr) / sizeof(arr[0]);

    int max_element = 0;
    for (int i = 0; i < n; i++) {
        if (arr[i] > max_element) max_element = arr[i];
    }

    vector<int> hash(max_element + 1, 0);
    for (int i = 0; i < n; i++) {
        hash[arr[i]]++;
    }

    bool is_duplicate = false;
    for (int i = 0; i< hash.size(); i++) {
        if (hash[i] > 1) {
            is_duplicate = true;
            break;
        }
    }
    
    if (is_duplicate) cout<< "contains duplicate\n";
    else cout<< "does not contains duplicate\n";

    return false;
}