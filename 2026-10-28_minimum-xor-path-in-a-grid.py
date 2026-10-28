# LeetCode Problem of the Day - 2026-10-28
# Title: Minimum XOR Path in a Grid
# Difficulty: Medium
# Topics: Array, Dynamic Programming, Bit Manipulation, Matrix
# URL: https://leetcode.com/problems/minimum-xor-path-in-a-grid/
#
# Problem statement:
# You are given a 2D integer array grid of size m * n. You start at the
# top-left cell (0, 0) and want to reach the bottom-right cell (m - 1, n - 1).
# At each step, you may move either right or down. The cost of a path is
# defined as the bitwise XOR of all the values in the cells along that path,
# including the start and end cells. Return the minimum possible XOR value
# among all valid paths from (0, 0) to (m - 1, n - 1).
#
# Examples:
#   Input: grid = [[1,2],[3,4]]  -> Output: 6
#     Paths: 1^2^4 = 7, 1^3^4 = 6; minimum is 6.
#   Input: grid = [[6,7],[5,8]]  -> Output: 9
#     Paths: 6^7^8 = 9, 6^5^8 = 11; minimum is 9.
#   Input: grid = [[2,7,5]]      -> Output: 0
#     Only path: 2^7^5 = 0.
#
# Constraints:
#   1 <= m == grid.length <= 1000
#   1 <= n == grid[i].length <= 1000
#   m * n <= 1000
#   0 <= grid[i][j] <= 1023
#
# Approach:
# DP over the set of achievable XOR values at each cell. Because every grid
# value is < 1024 (10 bits), any path XOR is also < 1024, so each cell's set
# has at most 1024 entries. A cell's set is the union of its top and left
# neighbours' sets, each XORed with the cell's own value. Only the previous
# row is kept, so memory stays small. The answer is the minimum of the
# destination cell's set.
#
# Time complexity: O(m * n * 1024) worst case (at most 1000 cells).
# Space complexity: O(n * 1024) for one row of sets.

from typing import List


class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        # prev[j] = set of achievable XORs reaching cell (current row - 1, j)
        prev = [set() for _ in range(n)]
        for i in range(m):
            cur = [set() for _ in range(n)]
            for j in range(n):
                v = grid[i][j]
                if i == 0 and j == 0:
                    cur[j] = {v}
                else:
                    reachable = set()
                    if i > 0:
                        reachable.update(x ^ v for x in prev[j])
                    if j > 0:
                        reachable.update(x ^ v for x in cur[j - 1])
                    cur[j] = reachable
            prev = cur
        return min(prev[n - 1])


if __name__ == "__main__":
    s = Solution()
    assert s.minCost([[1, 2], [3, 4]]) == 6
    assert s.minCost([[6, 7], [5, 8]]) == 9
    assert s.minCost([[2, 7, 5]]) == 0
    assert s.minCost([[5]]) == 5
    assert s.minCost([[0, 0], [0, 0]]) == 0
    # Brute-force cross-check on a small grid: enumerate all right/down paths.
    import itertools

    def brute(grid):
        m, n = len(grid), len(grid[0])
        best = None
        for moves in itertools.product("RD", repeat=m + n - 2):
            if moves.count("R") != n - 1:
                continue
            x = grid[0][0]
            r = c = 0
            for mv in moves:
                if mv == "R":
                    c += 1
                else:
                    r += 1
                x ^= grid[r][c]
            best = x if best is None else min(best, x)
        return best

    assert s.minCost([[1, 3, 2], [4, 0, 5], [2, 1, 3]]) == brute(
        [[1, 3, 2], [4, 0, 5], [2, 1, 3]]
    )
    print("All sample and brute-force tests passed.")
