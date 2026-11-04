# Minimum Operations to Make Elements Within K Subarrays Equal
# Date: 2026-11-04
# Difficulty: Hard
# Topics: Array, Hash Table, Math, Dynamic Programming, Sliding Window,
#         Heap (Priority Queue)
# LeetCode: https://leetcode.com/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/
#
# Problem statement:
#   You are given an integer array nums and two integers, x and k. You can
#   perform the following operation any number of times (including zero):
#   increase or decrease any element of nums by 1.
#   Return the minimum number of operations needed to have at least k
#   non-overlapping subarrays of size exactly x in nums, where all elements
#   within each subarray are equal.
#
# Examples:
#   Example 1:
#     Input: nums = [5,-2,1,3,7,3,6,4,-1], x = 3, k = 2
#     Output: 8
#     Explanation: Make nums[1..3] all 1 (3 + 2 operations) and
#       nums[5..7] all 4 (1 + 2 operations); 8 operations in total.
#   Example 2:
#     Input: nums = [9,-2,-2,-2,1,5], x = 2, k = 2
#     Output: 3
#     Explanation: Make nums[4] equal to -2 (3 operations), giving the
#       subarrays [-2,-2] at indices 1..2 and 3..4.
#
# Constraints:
#   2 <= nums.length <= 10^5
#   -10^6 <= nums[i] <= 10^6
#   2 <= x <= nums.length
#   1 <= k <= 15
#   2 <= k * x <= nums.length
#
# Approach:
#   For any fixed window, the cheapest value to make all its elements equal
#   is a median, and the cost is the sum of absolute deviations from that
#   median. Compute this cost for every length-x window with a sliding
#   median kept in two heaps (a max-heap for the lower half, a min-heap
#   for the upper half) plus lazy deletion, so each window costs
#   O(log x) instead of sorting it from scratch.
#   Then run a DP over prefixes: dp[t][i] is the cheapest cost of picking
#   t non-overlapping length-x subarrays inside the first i elements.
#   dp[t][i] = min(dp[t][i - 1], dp[t - 1][i - x] + cost[i - x]).
#   Costs are non-negative, so picking exactly k subarrays is as cheap as
#   picking at least k, and the answer is dp[k][n].
#
# Time complexity: O(n log x + k * n)
# Space complexity: O(n + x)  (one cost per window, plus the heaps and DP rows)

import heapq
from collections import Counter
from typing import List


class _SlidingMedian:
    """Two-heap sliding median with lazy deletion, tracking both sums.

    Elements are stored with a unique id (their array index), so removing
    a value that also occurs elsewhere in the window removes exactly the
    right occurrence, even when many values equal the median.
    """

    def __init__(self) -> None:
        self.low = []  # max-heap via (-value, idx): the lower half
        self.high = []  # min-heap via (value, idx): the upper half
        self.delayed = set()  # ids waiting to be pruned from a heap top
        self.side = {}  # idx -> "low" or "high"
        self.low_size = 0
        self.high_size = 0
        self.low_sum = 0
        self.high_sum = 0

    def _prune(self, heap, is_low: bool) -> None:
        while heap:
            idx = heap[0][1]
            if idx in self.delayed:
                heapq.heappop(heap)
                self.delayed.discard(idx)
            else:
                break

    def _rebalance(self) -> None:
        if self.low_size > self.high_size + 1:
            self._prune(self.low, True)
            neg_value, idx = heapq.heappop(self.low)
            value = -neg_value
            self.low_size -= 1
            self.low_sum -= value
            heapq.heappush(self.high, (value, idx))
            self.side[idx] = "high"
            self.high_size += 1
            self.high_sum += value
        elif self.low_size < self.high_size:
            self._prune(self.high, False)
            value, idx = heapq.heappop(self.high)
            self.high_size -= 1
            self.high_sum -= value
            heapq.heappush(self.low, (-value, idx))
            self.side[idx] = "low"
            self.low_size += 1
            self.low_sum += value
        self._prune(self.low, True)
        self._prune(self.high, False)

    def add(self, value: int, idx: int) -> None:
        self._prune(self.low, True)
        if not self.low or value <= -self.low[0][0]:
            heapq.heappush(self.low, (-value, idx))
            self.side[idx] = "low"
            self.low_size += 1
            self.low_sum += value
        else:
            heapq.heappush(self.high, (value, idx))
            self.side[idx] = "high"
            self.high_size += 1
            self.high_sum += value
        self._rebalance()

    def remove(self, value: int, idx: int) -> None:
        if self.side.pop(idx) == "low":
            self.low_size -= 1
            self.low_sum -= value
        else:
            self.high_size -= 1
            self.high_sum -= value
        self.delayed.add(idx)
        self._prune(self.low, True)
        self._prune(self.high, False)
        self._rebalance()

    def cost(self) -> int:
        self._prune(self.low, True)
        median = -self.low[0][0]
        return (
            median * self.low_size - self.low_sum
            + self.high_sum - median * self.high_size
        )


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # Cost of making each length-x window constant.
        median = _SlidingMedian()
        cost = [0] * (n - x + 1)
        for i, value in enumerate(nums):
            median.add(value, i)
            if i >= x:
                median.remove(nums[i - x], i - x)
            if i >= x - 1:
                cost[i - x + 1] = median.cost()

        # DP over prefixes, keeping only the previous row.
        INF = float("inf")
        dp_prev = [0] * (n + 1)
        for _ in range(k):
            dp_cur = [INF] * (n + 1)
            for i in range(1, n + 1):
                best = dp_cur[i - 1]
                if i >= x and dp_prev[i - x] != INF:
                    best = min(best, dp_prev[i - x] + cost[i - x])
                dp_cur[i] = best
            dp_prev = dp_cur
        return dp_prev[n]


if __name__ == "__main__":
    sol = Solution()
    assert sol.minOperations([5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2) == 8
    assert sol.minOperations([9, -2, -2, -2, 1, 5], 2, 2) == 3
    # Already-equal windows cost nothing.
    assert sol.minOperations([4, 4, 4, 4], 2, 2) == 0
    # Single window: median cost of [1, 100] is 99.
    assert sol.minOperations([1, 100], 2, 1) == 99
    print("All sample tests passed.")
