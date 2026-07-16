#include<bits/stdc++.h>
using namespace std;

class NumMatrix {
    vector<vector<int>> prefix_sum;
public:
    NumMatrix(vector<vector<int>>& matrix) {
        int rows = matrix.size();
        int cols = matrix[0].size();
        
        prefix_sum = matrix;

        for (int i = 1; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                prefix_sum[i][j] += prefix_sum[i - 1][j];
            }
        }

        for (int i = 0; i < rows; i++) {
            for (int j = 1; j < cols; j++) {
                prefix_sum[i][j] += prefix_sum[i][j - 1];
            }
        }
    }
    
    int sumRegion(int row1, int col1, int row2, int col2) {
        int res = prefix_sum[row2][col2];

        if (row1 != 0)
            res -= prefix_sum[row1 - 1][col2];

        if (col1 != 0)
            res -= prefix_sum[row2][col1 - 1];

        if (row1 != 0 && col1 != 0)
            res += prefix_sum[row1 - 1][col1 - 1];

        return res;
    }
};

/**
 * Your NumMatrix object will be instantiated and called as such:
 * NumMatrix* obj = new NumMatrix(matrix);
 * int param_1 = obj->sumRegion(row1,col1,row2,col2);
 */

int main()
{
    vector<vector<int>> matrix = 
    {{3, 0, 1, 4, 2}, 
    {5, 6, 3, 2, 1}, 
    {1, 2, 0, 1, 5}, 
    {4, 1, 0, 1, 7}, 
    {1, 0, 3, 0, 5}};

    NumMatrix* obj = new NumMatrix(matrix);
    int res = obj -> sumRegion(0,1,1,3);
    cout << res << endl;
    return 0;
}