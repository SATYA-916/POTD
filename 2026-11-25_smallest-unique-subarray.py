# Smallest Unique Subarray
# Date: 2026-11-25
# Difficulty: Hard
# Topics: Array, Hash Table, Binary Search, Rolling Hash, Suffix Array, Hash Function
# LeetCode: https://leetcode.com/problems/smallest-unique-subarray/
#
# Problem:
# You are given an integer array nums.
# Find the minimum length of a subarray that is not identical to any other
# subarray in nums. Return an integer denoting the minimum possible length
# of such a subarray. Two subarrays are identical if they have the same
# length and the same elements in corresponding positions.
#
# Example 1:
#   Input: nums = [3,3,3]
#   Output: 3
#   Explanation: [3] appears 3 times, [3,3] appears 2 times, [3,3,3] once.
#
# Example 2:
#   Input: nums = [2,1,2,3,3]
#   Output: 1
#   Explanation: [1] appears once, so the smallest unique subarray length is 1.
#
# Example 3:
#   Input: nums = [1,1,2,2,1]
#   Output: 2
#   Explanation: every length-1 subarray repeats, but [1,1] (and others)
#   of length 2 appear once.
#
# Constraints:
#   1 <= nums.length <= 10^5
#   1 <= nums[i] <= 10^5
#
# Approach:
# Binary search the answer L. For a fixed L, use a double rolling hash to
# count how many times every length-L subarray occurs; L is feasible if some
# subarray occurs exactly once. Feasibility is monotone: if a subarray of
# length L starting at i is unique, extending it by one element on either
# side (possible whenever L < n) keeps it unique, because any duplicate of
# the longer subarray would contain a duplicate of the unique one.
# The full array (L = n) is always unique, so an answer always exists.
#
# Time complexity: O(n log n)  (binary search over L, O(n) hash scan each)
# Space complexity: O(n)      (hash counts and powers)

from typing import List


class Solution:
    def smallestUniqueSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        MOD1, MOD2 = 1_000_000_007, 1_000_000_009
        BASE = 9113823

        pow1 = [1] * (n + 1)
        pow2 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow1[i] = (pow1[i - 1] * BASE) % MOD1
            pow2[i] = (pow2[i - 1] * BASE) % MOD2

        def has_unique(length: int) -> bool:
            """True if some subarray of the given length occurs exactly once."""
            h1 = h2 = 0
            for i in range(length):
                h1 = (h1 * BASE + nums[i]) % MOD1
                h2 = (h2 * BASE + nums[i]) % MOD2
            counts = {(h1, h2): 1}
            for i in range(1, n - length + 1):
                h1 = (h1 - nums[i - 1] * pow1[length - 1]) % MOD1
                h1 = (h1 * BASE + nums[i + length - 1]) % MOD1
                h2 = (h2 - nums[i - 1] * pow2[length - 1]) % MOD2
                h2 = (h2 * BASE + nums[i + length - 1]) % MOD2
                key = (h1, h2)
                counts[key] = counts.get(key, 0) + 1
            return 1 in counts.values()

        lo, hi, ans = 1, n, n
        while lo <= hi:
            mid = (lo + hi) // 2
            if has_unique(mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans


if __name__ == "__main__":
    sol = Solution()
    assert sol.smallestUniqueSubarray([3, 3, 3]) == 3
    assert sol.smallestUniqueSubarray([2, 1, 2, 3, 3]) == 1
    assert sol.smallestUniqueSubarray([1, 1, 2, 2, 1]) == 2
    assert sol.smallestUniqueSubarray([5]) == 1
    assert sol.smallestUniqueSubarray([1, 2, 3, 4]) == 1
    assert sol.smallestUniqueSubarray([1, 1, 1, 1]) == 4

    # Brute-force cross-check on small random arrays.
    import random
    from collections import Counter

    def brute(nums):
        n = len(nums)
        for length in range(1, n + 1):
            subs = Counter(tuple(nums[i:i + length]) for i in range(n - length + 1))
            if 1 in subs.values():
                return length
        return n

    random.seed(0)
    for _ in range(300):
        arr = [random.randint(1, 3) for _ in range(random.randint(1, 12))]
        assert sol.smallestUniqueSubarray(arr) == brute(arr), arr
    print("All tests passed.")
