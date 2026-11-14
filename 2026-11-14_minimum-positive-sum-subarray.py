# LeetCode Problem of the Day - 2026-11-14
# Title: Minimum Positive Sum Subarray
# Difficulty: Easy
# Topics: Array, Sliding Window, Prefix Sum
# Link: https://leetcode.com/problems/minimum-positive-sum-subarray/
#
# Problem statement:
# You are given an integer array nums and two integers l and r. Your task is
# to find the minimum sum of a subarray whose size is between l and r
# (inclusive) and whose sum is greater than 0.
# Return the minimum sum of such a subarray. If no such subarray exists,
# return -1.
# A subarray is a contiguous non-empty sequence of elements within an array.
#
# Example 1:
#   Input: nums = [3, -2, 1, 4], l = 2, r = 3
#   Output: 1
#   Explanation: The subarrays of length between l = 2 and r = 3 where the
#   sum is greater than 0 are [3, -2] (sum 1), [1, 4] (sum 5),
#   [3, -2, 1] (sum 2) and [-2, 1, 4] (sum 3). The smallest positive sum is 1.
#
# Example 2:
#   Input: nums = [-2, 2, -3, 1], l = 2, r = 3
#   Output: -1
#   Explanation: There is no subarray of length between l and r that has a
#   sum greater than 0.
#
# Example 3:
#   Input: nums = [1, 2, 3, 4], l = 2, r = 4
#   Output: 3
#   Explanation: The subarray [1, 2] has a length of 2 and the minimum sum
#   greater than 0.
#
# Constraints:
#   1 <= nums.length <= 100
#   1 <= l <= r <= nums.length
#   -1000 <= nums[i] <= 1000
#
# Approach:
# Build a prefix-sum array so any subarray sum is an O(1) difference.
# For every right endpoint i and every allowed length k in [l, r], the
# subarray nums[i - k + 1 .. i] has sum prefix[i + 1] - prefix[i + 1 - k];
# keep the smallest sum that is strictly positive. With n <= 100 this is
# at most 10^4 subarray sums, far below any limit.
#
# Time complexity: O(n * (r - l + 1)) <= O(n^2).
# Space complexity: O(n) for the prefix sums.

from typing import List


class Solution:
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i, v in enumerate(nums):
            prefix[i + 1] = prefix[i] + v

        best = None
        for end in range(n):
            for k in range(l, r + 1):
                start = end - k + 1
                if start < 0:
                    break
                s = prefix[end + 1] - prefix[start]
                if s > 0 and (best is None or s < best):
                    best = s
        return best if best is not None else -1


if __name__ == "__main__":
    sol = Solution()
    # Sample examples from the statement.
    assert sol.minimumSumSubarray([3, -2, 1, 4], 2, 3) == 1
    assert sol.minimumSumSubarray([-2, 2, -3, 1], 2, 3) == -1
    assert sol.minimumSumSubarray([1, 2, 3, 4], 2, 4) == 3
    # Edge cases.
    assert sol.minimumSumSubarray([5], 1, 1) == 5
    assert sol.minimumSumSubarray([-5], 1, 1) == -1
    assert sol.minimumSumSubarray([0, 0, 0], 1, 3) == -1
    assert sol.minimumSumSubarray([2, -1, 2], 1, 3) == 1  # [2, -1] sums to 1
    assert sol.minimumSumSubarray([-1, 3], 1, 2) == 2  # [3] vs [-1, 3] = 2

    # Brute-force cross-check on random small arrays.
    import random

    def brute(nums, l, r):
        n = len(nums)
        best = None
        for a in range(n):
            s = 0
            for b in range(a, n):
                s += nums[b]
                if l <= b - a + 1 <= r and s > 0:
                    best = s if best is None else min(best, s)
        return best if best is not None else -1

    rng = random.Random(20261114)
    for _ in range(500):
        m = rng.randint(1, 12)
        arr = [rng.randint(-5, 5) for _ in range(m)]
        ll = rng.randint(1, m)
        rr = rng.randint(ll, m)
        got = sol.minimumSumSubarray(arr, ll, rr)
        want = brute(arr, ll, rr)
        assert got == want, (arr, ll, rr, got, want)
    print("All self-tests passed.")
