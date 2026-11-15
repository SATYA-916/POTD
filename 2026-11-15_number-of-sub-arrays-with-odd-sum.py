# LeetCode Problem of the Day — 2026-11-15
# Problem: Number of Sub-arrays With Odd Sum
# Difficulty: Medium
# Topics: Array, Math, Dynamic Programming, Prefix Sum
# Link: https://leetcode.com/problems/number-of-sub-arrays-with-odd-sum/
#
# Problem statement:
#   Given an array of integers arr, return the number of subarrays with an
#   odd sum. Since the answer can be very large, return it modulo 10^9 + 7.
#
# Examples:
#   Example 1:
#     Input: arr = [1, 3, 5]
#     Output: 4
#     Explanation: All subarrays are [[1], [1,3], [1,3,5], [3], [3,5], [5]].
#     Their sums are [1, 4, 9, 3, 8, 5]. Odd sums are [1, 9, 3, 5], so the
#     answer is 4.
#   Example 2:
#     Input: arr = [2, 4, 6]
#     Output: 0
#     Explanation: All subarray sums are even, so the answer is 0.
#   Example 3:
#     Input: arr = [1, 2, 3, 4, 5, 6, 7]
#     Output: 16
#
# Constraints:
#   1 <= arr.length <= 10^5
#   1 <= arr[i] <= 100
#
# Approach:
#   A subarray sum is odd exactly when its two bounding prefix sums have
#   opposite parity. Scan the array once, tracking the running prefix parity
#   and how many prefix sums seen so far were even vs odd (starting with one
#   empty prefix, which is even). Each element contributes the count of
#   previous prefixes with the opposite parity, then the current prefix parity
#   count is updated. All counts are taken modulo 10^9 + 7.
#
# Time complexity: O(n)
# Space complexity: O(1)

from typing import List

MOD = 10 ** 9 + 7


class Solution:
    def numOfSubarrays(self, arr: List[int]) -> int:
        # even / odd: number of prefix sums with that parity seen so far.
        # The empty prefix (sum 0) counts as one even prefix.
        even = 1
        odd = 0
        prefix_parity = 0  # 0 = even, 1 = odd
        result = 0
        for num in arr:
            prefix_parity ^= num & 1
            if prefix_parity == 0:
                # Current prefix is even: subarrays ending here with odd sum
                # start after an odd prefix.
                result = (result + odd) % MOD
                even += 1
            else:
                # Current prefix is odd: subarrays ending here with odd sum
                # start after an even prefix.
                result = (result + even) % MOD
                odd += 1
        return result


if __name__ == "__main__":
    sol = Solution()
    assert sol.numOfSubarrays([1, 3, 5]) == 4
    assert sol.numOfSubarrays([2, 4, 6]) == 0
    assert sol.numOfSubarrays([1, 2, 3, 4, 5, 6, 7]) == 16
    # Extra checks: single odd / single even element.
    assert sol.numOfSubarrays([1]) == 1
    assert sol.numOfSubarrays([2]) == 0
    print("All sample tests passed.")
