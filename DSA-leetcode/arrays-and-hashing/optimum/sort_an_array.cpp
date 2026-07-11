#include<bits/stdc++.h>
using namespace std;

void max_heapify(vector<int>& A, int n, int heap_size) {
    int l = 2*n + 1;
    int r = 2*n + 2;
    int largest = n;

    if (l < heap_size && A[l] > A[largest]) largest = l;
    if (r < heap_size && A[r] > A[largest]) largest = r;

    if (largest != n) {
        int temp = A[n];
        A[n] = A[largest];
        A[largest] = temp;

        max_heapify(A,largest,heap_size);
    }
}

void build_max_heap(vector<int>& A) {
    int heap_size = A.size();

    for (int i = (heap_size / 2) - 1; i >= 0; i--) {
        max_heapify(A,i,heap_size);
    }
}

vector<int> heap_sort(vector<int>& nums){
    build_max_heap(nums);
    
    int heap_size = nums.size();
    for (int i = nums.size() - 1; i > 0; i--) {
        int temp = nums[i];
        nums[i] = nums[0];
        nums[0] = temp;

        heap_size--;
        max_heapify(nums,0, heap_size);
    }
    return nums;
}

int main()
{
    vector<int> nums = {5,2,3,1,6};
    vector<int> res = heap_sort(nums);

    for (auto e : res) {
        cout << e << ", ";
    } cout << endl;
    return 0;
}