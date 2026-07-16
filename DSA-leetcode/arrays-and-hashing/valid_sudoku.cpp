#include<bits/stdc++.h>
using namespace std;

bool isValidSudoku(vector<vector<char>>& board) {
    vector<unordered_set<char>> rows(9);
    vector<unordered_set<char>> columns(9);
    vector<unordered_set<char>> blocks(9);

    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            char curr = board[i][j];

            if (curr == '.') continue;

            int boxIdx = (i / 3) * 3 + ( j / 3);

            if (rows[i].count(curr) || columns[j].count(curr) || blocks[boxIdx].count(curr)) return false;

            rows[i].insert(curr);
            columns[j].insert(curr);
            blocks[boxIdx].insert(curr);
        }
    }

    return true;
}

int main()
{
    vector<vector<char>> board = 
        {{'5','3','.','.','7','.','.','.','.'}
        ,{'6','.','.','1','9','5','.','.','.'}
        ,{'.','9','8','.','.','.','.','6','.'}
        ,{'8','.','.','.','6','.','.','.','3'}
        ,{'4','.','.','8','.','3','.','.','1'}
        ,{'7','.','.','.','2','.','.','.','6'}
        ,{'.','6','.','.','.','.','2','8','.'}
        ,{'.','.','.','4','1','9','.','.','5'}
        ,{'.','.','.','.','8','.','.','7','9'}};

    bool res = isValidSudoku(board);
    cout << res << endl;
    return 0;
}