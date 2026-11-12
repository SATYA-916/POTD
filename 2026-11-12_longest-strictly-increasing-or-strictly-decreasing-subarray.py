"""
LeetCode Problem of the Day - 2026-11-12
Title: Longest Strictly Increasing or Strictly Decreasing Subarray
Difficulty: Easy
Topics: Array
Link: https://leetcode.com/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/

Problem Statement:
You are given an array of integers nums. Return the length of the longest
subarray of nums which is either strictly increasing or strictly decreasing.

Example 1:
    Input: nums = [1,4,3,3,2]
    Output: 2
    Explanation: The longest strictly increasing subarray is [1,4] and the
    longest strictly decreasing subarrays are [4,3] and [3,2], so we return 2.

Example 2:
    Input: nums = [3,3,3,3]
    Output: 1

Example 3:
    Input: nums = [3,2,1]
    Output: 3
    Explanation: The whole array [3,2,1] is strictly decreasing.

Constraints:
    1 <= nums.length <= 50
    1 <= nums[i] <= 50

Approach:
Single pass keeping the length of the strictly increasing run and the
strictly decreasing run ending at the current index. An upward step extends
the increasing run and resets the decreasing run to 1, a downward step does
the opposite, and equal neighbours reset both runs to 1. The answer is the
maximum run length seen.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def longestMonotonicSubarray(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return len(nums)

        ans = inc = dec = 1
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                inc += 1
                dec = 1
            elif nums[i] < nums[i - 1]:
                dec += 1
                inc = 1
            else:
                inc = dec = 1
            ans = max(ans, inc, dec)
        return ans


if __name__ == "__main__":
    sol = Solution()
    assert sol.longestMonotonicSubarray([1, 4, 3, 3, 2]) == 2
    assert sol.longestMonotonicSubarray([3, 3, 3, 3]) == 1
    assert sol.longestMonotonicSubarray([3, 2, 1]) == 3
    assert sol.longestMonotonicSubarray([1]) == 1
    assert sol.longestMonotonicSubarray([1, 2, 3, 4]) == 4
    assert sol.longestMonotonicSubarray([5, 4, 3, 2, 1, 2]) == 5
    print("All sample tests passed.")
