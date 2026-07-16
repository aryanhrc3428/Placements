#include<bits/stdc++.h>
using namespace std;

struct Node {
    int key;
    Node* next;

    Node(int k) {
        key = k;
        next = nullptr;
    }
};

class MyHashSet {
private:
    int numBuckets = 10000;
    vector<Node*> buckets;

    int getHash(int key) {
        return key % numBuckets;
    }
public:
    MyHashSet() {
        buckets = vector<Node*>(numBuckets, nullptr);
    }
    
    void add(int key) {
        if (contains(key)) return;
        int hash = getHash(key);
        if (buckets[hash] == nullptr) {
            buckets[hash] = new Node(key);
        }
        else {
            Node* newNode = new Node(key);
            newNode -> next = buckets[hash];
            buckets[hash] = newNode;
        }
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
    
    bool contains(int key) {
        int hash = getHash(key);
        Node* temp = buckets[hash];
        
        while (temp != nullptr) {
            if (temp -> key == key) return true;
            temp = temp -> next;
        }
        return false;
    }
};

/**
 * Your MyHashSet object will be instantiated and called as such:
 * MyHashSet* obj = new MyHashSet();
 * obj->add(key);
 * obj->remove(key);
 * bool param_3 = obj->contains(key);
 */

int main()
{
    return 0;
}