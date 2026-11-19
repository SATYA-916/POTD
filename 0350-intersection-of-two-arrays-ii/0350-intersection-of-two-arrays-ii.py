class Solution:
    def intersect(self, nums1: list[int], nums2: list[int]) -> list[int]:
        d={}
        for i in nums1:
            if i in d:
                d[i]=d[i]+1
            else:
                d[i]=1
        ans=[]
        for i in nums2:
            if i in d and d[i]!=0:
                ans.append(i)
                d[i]-=1
        return ans