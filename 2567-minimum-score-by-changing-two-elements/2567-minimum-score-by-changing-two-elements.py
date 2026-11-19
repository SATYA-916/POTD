class Solution:
    def minimizeSum(self, nums: List[int]) -> int:
    #in total there could be 3 scenarios
        #sum=high +low minimize high and low
        #mini low=best is to make 2 elemet equal can be 0
            #2 operation on low side such that <=nums[2]
            #[1,4,5,7,8]=>[5,5,5,7,8] =>0+3  CODE----------nums[-1]-nums[2]
        #mini hig=best is to make 2 elemet equal can be 0 
            #2 operation on hig side such that >=nums[-3]
            #[1,4,5,7,8]=>[1,4,5,5,5] =>3+0 CODE-----------nums[-3]-nums[0]
        #other choice either side 1 operation nums[1]==nums[0] and nums[-1] ==nums[-2]
            #[hig=max abs diference (max-min)]
            #|8-1| reduce by dec 8 or increase 1 so that diff is min [1,4,5,7,8]
            #[1,4,5,7,8]=>[4,4,5,7,7] =>0+3 CODE----------nums[-2]-nums[1]
        nums.sort()
        return min(nums[-1]-nums[2],nums[-3]-nums[0],nums[-2]-nums[1])
