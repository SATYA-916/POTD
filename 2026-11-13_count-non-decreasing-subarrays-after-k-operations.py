# LeetCode Problem of the Day - 2026-11-13
# Title: Count Non-Decreasing Subarrays After K Operations
# Difficulty: Hard
# Topics: Array, Stack, Segment Tree, Queue, Sliding Window, Monotonic Stack, Monotonic Queue
# Link: https://leetcode.com/problems/count-non-decreasing-subarrays-after-k-operations/
#
# Problem statement:
# You are given an array nums of n integers and an integer k.
# For each subarray of nums, you can apply up to k operations on it. In each
# operation, you increment any element of the subarray by 1. Each subarray is
# considered independently, meaning changes made to one subarray do not persist
# to another. Return the number of subarrays that you can make non-decreasing
# after performing at most k operations.
# An array is non-decreasing if each element is >= its previous element.
#
# Example 1:
#   Input: nums = [6,3,1,2,4,4], k = 7
#   Output: 17
#   Explanation: Out of all 21 possible subarrays, only [6,3,1], [6,3,1,2],
#   [6,3,1,2,4] and [6,3,1,2,4,4] cannot be made non-decreasing with k = 7.
#
# Example 2:
#   Input: nums = [6,3,1,3,6], k = 4
#   Output: 12
#
# Constraints:
#   1 <= nums.length <= 10^5
#   1 <= nums[i] <= 10^9
#   1 <= k <= 10^9
#
# Approach:
# For a subarray nums[l..r], the cheapest way to make it non-decreasing using
# only increments is to scan left to right keeping the running maximum: each
# element nums[i] must be raised to at least max(nums[l..i-1]), so
#   cost(l, r) = sum_{i=l+1..r} max(0, max(nums[l..i-1]) - nums[i]).
# The running maxima from l form the "next greater element" chain
# l = p1 < p2 < ... < pm (each pi+1 is the first index after pi with a
# strictly larger value). Inside the segment (pj, pj+1) every element is
# capped at nums[pj], so its contribution is
#   nums[pj] * (pj+1 - pj - 1) - (prefix[pj+1] - prefix[pj+1]),
# computable in O(1) with prefix sums. Binary lifting over the next-greater
# jumps evaluates cost(l, r) in O(log n).
# cost(l, r) is non-decreasing in r for fixed l, so the smallest valid l is
# monotone in r: a two-pointer sliding window counts, for each r, all
# l in [left, r] with cost(l, r) <= k.
#
# Time complexity: O(n log n) (binary lifting table + O(n) cost queries).
# Space complexity: O(n log n) for the lifting tables.

from typing import List


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        prefix = [0] * (n + 1)
        for i, v in enumerate(nums):
            prefix[i + 1] = prefix[i] + v

        # nxt[i] = first index > i with nums[j] > nums[i], or n if none.
        nxt = [n] * (n + 1)
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            nxt[i] = stack[-1] if stack else n
            stack.append(i)

        LOG = (n + 1).bit_length()
        up = [nxt]
        # seg[0][i] = contribution of the full segment starting at record i:
        # sum_{j=i+1}^{nxt[i]-1} (nums[i] - nums[j]).
        seg0 = [0] * (n + 1)
        for i in range(n):
            j = nxt[i]
            seg0[i] = nums[i] * (j - i - 1) - (prefix[j] - prefix[i + 1])
        seg = [seg0]
        for _ in range(1, LOG):
            prev_up, prev_seg = up[-1], seg[-1]
            cur_up = [prev_up[v] for v in prev_up]
            cur_seg = [s + prev_seg[m] for s, m in zip(prev_seg, prev_up)]
            up.append(cur_up)
            seg.append(cur_seg)

        def cost(l: int, r: int) -> int:
            # Minimum increments to make nums[l..r] non-decreasing.
            cur = l
            total = 0
            for lv in range(LOG - 1, -1, -1):
                if up[0][cur] > r:
                    break  # no further record lies inside [l, r]
                jump = up[lv][cur]
                if jump <= r:
                    total += seg[lv][cur]
                    cur = jump
            # Final partial segment (cur, r].
            total += nums[cur] * (r - cur) - (prefix[r + 1] - prefix[cur + 1])
            return total

        left = 0
        ans = 0
        for r in range(n):
            while cost(left, r) > k:
                left += 1
            ans += r - left + 1
        return ans


if __name__ == "__main__":
    sol = Solution()
    # Sample examples from the statement.
    assert sol.countNonDecreasingSubarrays([6, 3, 1, 2, 4, 4], 7) == 17
    assert sol.countNonDecreasingSubarrays([6, 3, 1, 3, 6], 4) == 12
    # Edge cases.
    assert sol.countNonDecreasingSubarrays([5], 1) == 1
    assert sol.countNonDecreasingSubarrays([1, 2, 3, 4], 1) == 10
    assert sol.countNonDecreasingSubarrays([4, 3, 2, 1], 1) == 7  # 4 singles + 3 adjacent pairs, each costing 1
    assert sol.countNonDecreasingSubarrays([2, 2, 2], 1) == 6

    # Brute-force cross-check on random small arrays.
    import random

    def brute(nums, k):
        n = len(nums)
        total = 0
        for l in range(n):
            mx = nums[l]
            c = 0
            for r in range(l, n):
                if r > l:
                    c += max(0, mx - nums[r])
                    mx = max(mx, nums[r])
                if c <= k:
                    total += 1
        return total

    rng = random.Random(20261113)
    for _ in range(300):
        m = rng.randint(1, 12)
        arr = [rng.randint(1, 6) for _ in range(m)]
        kk = rng.randint(1, 10)
        got = sol.countNonDecreasingSubarrays(arr, kk)
        want = brute(arr, kk)
        assert got == want, (arr, kk, got, want)
    print("All self-tests passed.")
