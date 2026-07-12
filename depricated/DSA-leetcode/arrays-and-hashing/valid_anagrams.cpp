#include <bits/stdc++.h>
using namespace std;

bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;

    int count[26];

    for (int i = 0; i < s.size(); i++) {
        count[s[i] - 'a']++;
        count[t[i] - 'a']--;
    }

    for (int i = 0; i < 26; i++) {
        if (count[i] != 0) return false;
    }

    return true;
}

int main() {

    string s = "ggii";
    string t = "eekk";

    bool res = isAnagram(s,t);

    if (res) cout << "contains anagram.\n";
    else cout << "does not contains anagram.\n";

    return 0;
}