#include<iostream>
#include<vector>
using namespace std; 

int removeDuplicates(vector<int>& nums) 
{
    for(int i=0;i<nums.size();i++)
    {
        int j=i;
        while(nums[j]==nums[i] && j<nums.size())
        {
            j++;
        }
        j--;
        nums.erase(nums.begin()+i,nums.begin()+j);
    }
    return nums.size();
}
int main()
{
    vector<int> x{1,1,2};
    cout<<removeDuplicates(x);
}