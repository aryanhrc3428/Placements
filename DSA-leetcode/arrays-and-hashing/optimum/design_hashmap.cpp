#include<bits/stdc++.h>
using namespace std;

struct Node {
    int key;
    int value;
    Node* next;

    Node(int k, int v) {
        key = k;
        value = v;
        next = nullptr;
    }
};

class MyHashMap {
private:
    int numBuckets = 10000;
    vector<Node*> buckets;

    int getHash(int key) {
        return key % numBuckets;
    }

    int contains (int key) {
        int hash = getHash(key);
        Node* temp = buckets[hash];
        
        while (temp != nullptr) {
            if (temp -> key == key) return true;
            temp = temp -> next;
        }
        return false;
    }

public:
    MyHashMap() {
        buckets = vector<Node*>(numBuckets, nullptr);
    }
    
    void put(int key, int value) {
        int hash = getHash(key);
        if (contains(key)) {
            Node* temp = buckets[hash];
            while (temp != nullptr) {
                if (temp -> key == key) temp -> value = value;
                temp = temp -> next;
            }
            return;
        }
        if (buckets[hash] == nullptr) {
            buckets[hash] = new Node(key,value);
        }
        else {
            Node* newNode = new Node(key,value);
            newNode -> next = buckets[hash];
            buckets[hash] = newNode;
        }
    }
    
    int get(int key) {
        int hash = getHash(key);
        if (buckets[hash] == nullptr) return -1;

        Node* temp = buckets[hash];
        while (temp != nullptr) {
            if (temp -> key == key) return temp -> value;
            temp = temp -> next;
        }
        return -1;
    }
    
    void remove(int key) {
        if (!contains(key)) return;
        int hash = getHash(key);
        Node* temp = buckets[hash];

        if (temp -> key == key) {
            buckets[hash] = temp -> next;
            delete temp;
            return;
        }
        
        Node* prev = temp;
        temp = temp -> next;

        while (temp != nullptr) {
            if (temp -> key == key) {
                prev -> next = temp -> next;
                delete temp;
                return;
            }
            prev = temp;
            temp = temp -> next;
        }
    }
};

int main()
{
    return 0;
}