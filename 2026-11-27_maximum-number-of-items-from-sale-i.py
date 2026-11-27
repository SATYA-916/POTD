# LeetCode Problem of the Day: Maximum Number of Items From Sale I
# Date: 2026-11-27
# Difficulty: Medium
# Topics: Array, Dynamic Programming, Greedy
# Link: https://leetcode.com/problems/maximum-number-of-items-from-sale-i/
#
# Problem:
# You are given a 2D integer array items, where items[i] = [factor_i, price_i].
# There are unlimited copies of each item. You may buy any number of copies
# such that the total cost is at most budget. For each item i that you bought
# at least one copy of, you receive one free copy of every item j (j != i)
# such that factor_i divides factor_j. Buying multiple copies of the same
# item does not give additional free copies through that item. The same item
# j can be received multiple times for free from purchases of different types.
# Return the maximum total number of item copies you can obtain, including
# both purchased and free copies, while spending at most budget.
#
# Example 1:
#   Input: items = [[6,2],[2,6],[3,4]], budget = 9
#   Output: 4
#   Explanation: Buy 2 copies of item 0 and 1 copy of item 2 (cost 8).
#   Buying item 2 gives 1 free copy of item 0 since 3 divides 6.
#   Total = 3 purchased + 1 free = 4.
#
# Example 2:
#   Input: items = [[2,4],[3,2],[4,1],[6,4],[12,4]], budget = 8
#   Output: 10
#   Explanation: Buy 1 copy of item 0, 1 copy of item 1 and 2 copies of
#   item 2 (cost 8). Free copies: item 0 gives items 2, 3, 4; item 1 gives
#   items 3, 4; item 2 gives item 4. Total = 4 purchased + 6 free = 10.
#
# Constraints:
#   1 <= items.length <= 1000
#   1 <= factor_i, price_i <= 1500
#   1 <= budget <= 1500
#
# Approach:
# The free copies decompose per purchased item type. For item i define
# gain(i) as the number of j != i with factor_i dividing factor_j. Buying
# item i at least once yields 1 purchased copy plus gain(i) free copies, so
# its value is value(i) = 1 + gain(i). Let S be the set of item types bought
# at least once. The total is sum of value(i) over S plus the extra copies
# bought with the remaining budget, which are cheapest bought at the
# minimum price p_min. So the total for a set S is
# sum(value(i)) + (budget - cost(S)) // p_min. Choosing S is a 0/1 knapsack
# over cost up to budget: dp[c] = max total value of a set costing exactly c.
# The answer is the max over c of dp[c] + (budget - c) // p_min.
#
# Time complexity: O(n^2 + n * budget) for the gains and the knapsack.
# Space complexity: O(n + budget).

from typing import List


class Solution:
    def maximumSaleItems(self, items: List[List[int]], budget: int) -> int:
        n = len(items)
        factors = [f for f, _ in items]
        prices = [p for _, p in items]
        p_min = min(prices)

        # value[i] = 1 purchased copy + gain(i) free copies from buying item i
        values = []
        for i in range(n):
            gain = 0
            fi = factors[i]
            for j in range(n):
                if j != i and factors[j] % fi == 0:
                    gain += 1
            values.append(1 + gain)

        # 0/1 knapsack: dp[c] = max total value of a set costing exactly c
        NEG = -10 ** 9
        dp = [NEG] * (budget + 1)
        dp[0] = 0
        for price, val in zip(prices, values):
            for c in range(budget, price - 1, -1):
                if dp[c - price] != NEG:
                    dp[c] = max(dp[c], dp[c - price] + val)

        ans = 0
        for c in range(budget + 1):
            if dp[c] != NEG:
                ans = max(ans, dp[c] + (budget - c) // p_min)
        return ans


if __name__ == "__main__":
    sol = Solution()
    assert sol.maximumSaleItems([[6, 2], [2, 6], [3, 4]], 9) == 4
    assert sol.maximumSaleItems([[2, 4], [3, 2], [4, 1], [6, 4], [12, 4]], 8) == 10
    print("All sample tests passed.")
