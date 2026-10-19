"""
LeetCode 2089. Find Target Indices After Sorting Array
Date: 2026-10-19 | Difficulty: Easy
Topics: Array, Binary Search, Sorting
Link: https://leetcode.com/problems/find-target-indices-after-sorting-array/

Problem:
You are given a 0-indexed integer array nums and a target element target.
A target index is an index i such that nums[i] == target after sorting nums.
Return a list of the target indices sorted in increasing order.

Example 1:
  Input: nums = [1,2,5,2,3], target = 2
  Output: [1,2]
  Explanation: After sorting, nums is [1,2,2,3,5]. Indices 1 and 2 hold 2.

Example 2:
  Input: nums = [1,2,5,2,3], target = 3
  Output: [3]

Example 3:
  Input: nums = [1,2,5,2,3], target = 5
  Output: [4]

Constraints:
  1 <= nums.length <= 100
  1 <= nums[i], target <= 100

Approach (counting - O(n) time, O(1) extra space):
  After sorting, every element smaller than target sits before every
  occurrence of target. So the first target index is simply the count of
  elements < target, and the run of target indices has length equal to the
  count of elements == target. No sorting needed.
"""

from typing import List


class Solution:
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        less = sum(1 for x in nums if x < target)
        equal = sum(1 for x in nums if x == target)
        return list(range(less, less + equal))


if __name__ == "__main__":
    s = Solution()
    assert s.targetIndices([1, 2, 5, 2, 3], 2) == [1, 2]
    assert s.targetIndices([1, 2, 5, 2, 3], 3) == [3]
    assert s.targetIndices([1, 2, 5, 2, 3], 5) == [4]
    assert s.targetIndices([1], 1) == [0]
    assert s.targetIndices([3, 1, 2], 4) == []
    assert s.targetIndices([2, 2, 2], 2) == [0, 1, 2]
    print("All sample tests passed.")
