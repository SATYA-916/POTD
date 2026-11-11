# LeetCode Problem of the Day
# Title: Minimum Cost to Acquire Required Items
# Date: 2026-11-11
# Difficulty: Medium
# Topics: Math, Greedy
# Link: https://leetcode.com/problems/minimum-cost-to-acquire-required-items/
#
# Problem:
# You are given five integers cost1, cost2, costBoth, need1, and need2.
# There are three types of items available:
#   - An item of type 1 costs cost1 and contributes 1 unit to the type 1
#     requirement only.
#   - An item of type 2 costs cost2 and contributes 1 unit to the type 2
#     requirement only.
#   - An item of type 3 costs costBoth and contributes 1 unit to both
#     type 1 and type 2 requirements.
# You must collect enough items so that the total contribution toward
# type 1 is at least need1 and toward type 2 is at least need2.
# Return the minimum possible total cost to achieve these requirements.
#
# Examples:
#   Input: cost1 = 3, cost2 = 2, costBoth = 1, need1 = 3, need2 = 2
#   Output: 3
#   Explanation: Buy three type 3 items: 3 * 1 = 3.
#
#   Input: cost1 = 5, cost2 = 4, costBoth = 15, need1 = 2, need2 = 3
#   Output: 22
#   Explanation: Buy 2 type 1 items and 3 type 2 items: 2 * 5 + 3 * 4 = 22.
#
#   Input: cost1 = 5, cost2 = 4, costBoth = 15, need1 = 0, need2 = 0
#   Output: 0
#
# Constraints:
#   1 <= cost1, cost2, costBoth <= 10^6
#   0 <= need1, need2 <= 10^9
#
# Approach:
# Let x be the number of type 3 items bought. Buying more than
# max(need1, need2) of them is never useful, since both requirements
# are already met, and contributions above the requirement are allowed
# ("at least"), so x may exceed min(need1, need2).
# The total cost is piecewise linear in x with breakpoints at 0,
# min(need1, need2) and max(need1, need2):
#   - For 0 <= x <= min(need1, need2):
#     cost(x) = x * costBoth + (need1 - x) * cost1 + (need2 - x) * cost2
#   - For min(need1, need2) <= x <= max(need1, need2):
#     cost(x) = x * costBoth + (max - x) * (cost of the larger need's type)
#   - At x = max(need1, need2): cost = max * costBoth (both needs met).
# A piecewise linear function attains its minimum at a breakpoint,
# so evaluating x = 0, x = min(need1, need2) and x = max(need1, need2)
# and taking the smallest cost is optimal.
#
# Time Complexity: O(1)
# Space Complexity: O(1)


class Solution:
    def minimumCost(self, cost1: int, cost2: int, costBoth: int, need1: int, need2: int) -> int:
        lo = min(need1, need2)
        hi = max(need1, need2)
        # x = 0: buy only single-type items.
        best = need1 * cost1 + need2 * cost2
        # x = lo: type 3 items cover the smaller need entirely.
        best = min(best, lo * costBoth + (need1 - lo) * cost1 + (need2 - lo) * cost2)
        # x = hi: type 3 items alone cover both needs.
        best = min(best, hi * costBoth)
        return best


if __name__ == "__main__":
    sol = Solution()
    # Example 1
    assert sol.minimumCost(3, 2, 1, 3, 2) == 3
    # Example 2
    assert sol.minimumCost(5, 4, 15, 2, 3) == 22
    # Example 3
    assert sol.minimumCost(5, 4, 15, 0, 0) == 0
    # Only one type needed
    assert sol.minimumCost(5, 4, 1, 10, 0) == 10
    # costBoth exactly equals cost1 + cost2 (tie -> same either way)
    assert sol.minimumCost(5, 4, 9, 2, 3) == 22
    # Large needs, cheap type 3
    assert sol.minimumCost(10**6, 10**6, 1, 10**9, 10**9) == 10**9
    print("All tests passed.")
