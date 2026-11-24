import math
class Solution:
    def maxLength(self, nums: List[int]) -> int:
        ans=1
        for i in range(len(nums)):
            g,l,x=nums[i],nums[i],nums[i]
            for j in range(i+1,len(nums)):
                x*=nums[j]
                g=math.gcd(g,nums[j])
                l=l*nums[j]//math.gcd(l,nums[j])
                if x==l*g:
                    ans=max(ans,j-i+1)
        return ans

