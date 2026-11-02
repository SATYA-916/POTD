# Minimum Moves to Equal Array Elements II
# Date: 2026-11-02
# Difficulty: Medium
# Topics: Array, Math, Sorting
# LeetCode: https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/
#
# Problem statement:
# Given an integer array nums of size n, return the minimum number of moves
# required to make all array elements equal. In one move, you can increment
# or decrement an element of the array by 1. Test cases are designed so that
# the answer will fit in a 32-bit integer.
#
# Examples:
#   Example 1:
#     Input: nums = [1, 2, 3]
#     Output: 2
#     Explanation: [1, 2, 3] -> [2, 2, 3] -> [2, 2, 2]
#   Example 2:
#     Input: nums = [1, 10, 2, 9]
#     Output: 16
#
# Constraints:
#   n == nums.length
#   1 <= nums.length <= 10^5
#   -10^9 <= nums[i] <= 10^9
#
# Approach:
# The target value that minimises the sum of absolute deviations is a
# median of nums: moving the target one step toward/away from the median
# changes the total by (#elements on one side) - (#elements on the other),
# so the total is minimised at any median. Sort nums, pick the middle
# element (for even n, either of the two middle values works), and sum
# |x - median| over all x.
#
# Time complexity: O(n log n) for sorting.
# Space complexity: O(1) extra (sorting in place; O(n) if a copy is kept).

from typing import List


class Solution:
    def minMoves2(self, nums: List[int]) -> int:
        nums = sorted(nums)
        median = nums[len(nums) // 2]
        return sum(abs(x - median) for x in nums)


if __name__ == "__main__":
    s = Solution()
    assert s.minMoves2([1, 2, 3]) == 2
    assert s.minMoves2([1, 10, 2, 9]) == 16
    # Edge cases
    assert s.minMoves2([5]) == 0
    assert s.minMoves2([1, 1, 1]) == 0
    assert s.minMoves2([1, 2]) == 1
    assert s.minMoves2([-5, 5]) == 10
    print("All self-tests passed.")
