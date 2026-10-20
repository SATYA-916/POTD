# LeetCode Problem of the Day - 2026-10-20
# Title: Sum of Sortable Integers
# Difficulty: Hard
# Topics: Array, Math, Sorting, Enumeration
# URL: https://leetcode.com/problems/sum-of-sortable-integers/
#
# Problem statement:
# You are given an integer array nums of length n.
# An integer k is called sortable if k divides n and you can sort nums in
# non-decreasing order by sequentially performing the following operations:
#   1. Partition nums into consecutive subarrays of length k.
#   2. Cyclically rotate each subarray independently any number of times
#      to the left or to the right.
# Return an integer denoting the sum of all possible sortable integers k.
#
# Example 1:
#   Input: nums = [3,1,2]
#   Output: 3
#   Explanation: divisors of 3 are 1 and 3. k=1 cannot sort; k=3 works by
#   rotating [3,1,2] once into [1,2,3]. Only k=3 is sortable -> answer 3.
#
# Example 2:
#   Input: nums = [7,6,5]
#   Output: 0
#   Explanation: k=1 cannot sort; [7,6,5] cannot be rotated into sorted
#   order either. No k is sortable.
#
# Example 3:
#   Input: nums = [5,8]
#   Output: 3
#   Explanation: [5,8] is already sorted, so every divisor (1 and 2) is
#   sortable -> answer 1 + 2 = 3.
#
# Constraints:
#   1 <= n == nums.length <= 10^5
#   1 <= nums[i] <= 10^5
#
# Approach:
# Fix a divisor k of n and let S = sorted(nums). Rotating each length-k
# block preserves its multiset, so after the operations the whole array must
# equal S exactly; block i (positions [i*k, (i+1)*k)) must become S[i*k:(i+1)*k].
# Block B = nums[i*k:(i+1)*k] can be rotated into the sorted segment T =
# S[i*k:(i+1)*k] iff B is a rotation of T, which holds iff BOTH:
#   (a) sorted(B) == T  (same multiset), and
#   (b) B has at most one "cyclic descent", i.e. at most one index j with
#       B[j] > B[(j+1) % k]. (A rotation of a non-decreasing sequence has at
#       most one wrap-around drop; conversely such an array rotated at the
#       drop becomes non-decreasing, hence equals sorted(B).)
# Condition (b) is checked in O(1) per block with prefix sums over the
# adjacent-descent indicator array; (a) uses sorting of each block.
# Sum every divisor k for which all n/k blocks satisfy (a) and (b).
#
# Time complexity: O(n log n + n * d(n)) where d(n) is the number of divisors
#   (<= 128 for n <= 10^5); per divisor we do O(n) work.
# Space complexity: O(n) for the sorted copy and the prefix sums.

from typing import List


class Solution:
    def sortableIntegers(self, nums: List[int]) -> int:
        n = len(nums)
        s = sorted(nums)

        # pref[i] = number of descents nums[j] > nums[j+1] for j < i
        pref = [0] * (n + 1)
        for i in range(n - 1):
            pref[i + 1] = pref[i] + (1 if nums[i] > nums[i + 1] else 0)
        pref[n] = pref[n - 1]

        # collect divisors of n
        divisors = []
        k = 1
        while k * k <= n:
            if n % k == 0:
                divisors.append(k)
                if k * k != n:
                    divisors.append(n // k)
            k += 1

        ans = 0
        for k in divisors:
            ok = True
            for L in range(0, n, k):
                # cyclic descents inside block [L, L+k):
                # internal adjacent pairs + the wrap-around pair
                internal = pref[L + k - 1] - pref[L]
                wrap = 1 if nums[L + k - 1] > nums[L] else 0
                if internal + wrap > 1:
                    ok = False
                    break
                if sorted(nums[L:L + k]) != s[L:L + k]:
                    ok = False
                    break
            if ok:
                ans += k
        return ans


if __name__ == "__main__":
    sol = Solution()

    # Sample tests from the problem statement
    assert sol.sortableIntegers([3, 1, 2]) == 3
    assert sol.sortableIntegers([7, 6, 5]) == 0
    assert sol.sortableIntegers([5, 8]) == 3

    # Edge cases
    assert sol.sortableIntegers([1]) == 1            # k=1 trivially sortable
    assert sol.sortableIntegers([2, 1]) == 2         # rotate whole array
    assert sol.sortableIntegers([1, 2, 3, 4]) == 1 + 2 + 4  # already sorted: all divisors
    assert sol.sortableIntegers([2, 2, 1, 1]) == 4   # rotate whole array by 2
    assert sol.sortableIntegers([4, 3, 2, 1]) == 0   # no block rotatable to sorted
    assert sol.sortableIntegers([1, 3, 2, 4]) == 0   # blocks {1,3}/{2,4} mismatch S segments; whole array not a rotation of sorted

    # Cross-check against brute force on random small arrays
    import random
    from itertools import product

    def brute(nums):
        n = len(nums)
        S = sorted(nums)
        ans = 0
        for k in range(1, n + 1):
            if n % k != 0:
                continue
            blocks = [nums[i:i + k] for i in range(0, n, k)]
            rot_choices = [[b[j:] + b[:j] for j in range(k)] for b in blocks]
            if any(
                [x for blk in combo for x in blk] == S
                for combo in product(*rot_choices)
            ):
                ans += k
        return ans

    rng = random.Random(20261020)
    for _ in range(300):
        n = rng.randint(1, 8)
        arr = [rng.randint(1, 4) for _ in range(n)]
        assert sol.sortableIntegers(arr) == brute(arr), arr

    print("All tests passed.")
