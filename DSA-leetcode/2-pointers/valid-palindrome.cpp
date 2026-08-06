#include<bits/stdc++.h>
using namespace std;

bool isPalindrome(string s) {
    int start = 0;
    int end = s.size() - 1;

    while (start < end) {
        if (!isalnum(s[start])) {
            start++;
            continue;
        }
        if (!isalnum(s[end])) {
            end--;
            continue;
        }
        if (isupper(s[start])) s[start] = static_cast<char>(tolower(s[start]));
        if (isupper(s[end])) s[end] = static_cast<char>(tolower(s[end]));
        if (s[start] != s[end]) return false;
        start++;
        end--;
    }
    return true;
}

int main()
{
    string s = "A man, a plan, a canal: Panama";
    // string s = "race a car";
    bool isPal = isPalindrome(s);
    cout << "is Palindrome: " << isPal << endl;
    return 0;
}