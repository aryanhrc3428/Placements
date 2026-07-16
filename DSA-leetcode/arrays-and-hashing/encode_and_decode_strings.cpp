#include<bits/stdc++.h>
using namespace std;

string encode(vector<string>& messages) {
    string res = "";

    for (int i = 0; i < messages.size(); i++) {
        res += to_string(messages[i].size()) + "#" + messages[i];
    }
    return res;
}

vector<string> decode(string message) {
    vector<string> res;
    
    int i = 0;
    int num = 0;
    while (i <= message.size() - 1) {
        if (message[i] != '#') {
            num = num*10 + (message[i] - '0');
            i++;
        }
        else {
            res.push_back(message.substr(i + 1, num));
            i += num - 1;
            num = 0;
        }
    }
    return res;
}

int main()
{
    vector<string> messages = {"Hello", "World"};
    string encoded_message = encode(messages);
    vector<string> decoded_message = decode(encoded_message);
    for (auto e : decoded_message) cout << e << " - ";
    // cout << endl;
    return 0;
}