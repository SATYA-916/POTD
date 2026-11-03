# LeetCode Problem of the Day — 2026-11-03
# Title: Minimum Moves to Equal Array Elements III
# Difficulty: Easy
# Topics: Array, Math
# Link: https://leetcode.com/problems/minimum-moves-to-equal-array-elements-iii/
#
# Problem statement:
#   You are given an integer array nums.
#   In one move, you may increase the value of any single element nums[i] by 1.
#   Return the minimum total number of moves required so that all elements
#   in nums become equal.
#
# Examples:
#   Input: nums = [2,1,3]  -> Output: 3
#     Raise 2 -> 3 (1 move) and 1 -> 3 (2 moves); total 3.
#   Input: nums = [4,4,5]  -> Output: 2
#     Raise each 4 -> 5 (1 move each); total 2.
#
# Constraints:
#   1 <= nums.length <= 100
#   1 <= nums[i] <= 100
#
# Approach:
#   Moves can only increase elements, never decrease them, so every element
#   must end up at a value >= max(nums). Raising anything above max(nums)
#   would only add extra moves, so the optimal target is exactly max(nums).
#   The answer is therefore sum(max(nums) - x for x in nums).
#
# Time complexity: O(n) — one pass for the max, one pass for the sum.
# Space complexity: O(1) — no extra storage beyond a few variables.
from typing import List


class Solution:
    def minMoves(self, nums: List[int]) -> int:
        target = max(nums)
        return sum(target - x for x in nums)


if __name__ == "__main__":
    s = Solution()
    assert s.minMoves([2, 1, 3]) == 3
    assert s.minMoves([4, 4, 5]) == 2
    assert s.minMoves([5]) == 5 - 5  # single element: 0 moves
    assert s.minMoves([1, 1, 1]) == 0
    assert s.minMoves([1, 100]) == 99
    print("All sample and edge-case tests passed.")
