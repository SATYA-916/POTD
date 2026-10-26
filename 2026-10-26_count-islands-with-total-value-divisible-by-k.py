"""
Count Islands With Total Value Divisible by K
Date: 2026-10-26
Difficulty: Medium
Topics: Array, Depth-First Search, Breadth-First Search, Union-Find, Matrix
LeetCode: https://leetcode.com/problems/count-islands-with-total-value-divisible-by-k/

Problem statement:
  You are given an m x n matrix grid and a positive integer k.
  An island is a group of positive integers (representing land) that are
  4-directionally connected (horizontally or vertically). The total value
  of an island is the sum of the values of all cells in the island.
  Return the number of islands with a total value divisible by k.

Examples:
  Example 1:
    Input: grid = [[0,2,1,0,0],[0,5,0,0,5],[0,0,1,0,0],
                   [0,1,4,7,0],[0,2,0,0,8]], k = 5
    Output: 2
    Explanation: The grid contains four islands. The islands with a total
    value divisible by 5 are counted; the others are not.

  Example 2:
    Input: grid = [[3,0,3,0],[0,3,0,3],[3,0,3,0]], k = 3
    Output: 6
    Explanation: The grid contains six islands, each with a total value
    divisible by 3.

Constraints:
  m == grid.length, n == grid[i].length
  1 <= m, n <= 1000, 1 <= m * n <= 10^5
  0 <= grid[i][j] <= 10^6
  1 <= k <= 10^6

Approach:
  Flood-fill each unvisited positive cell with an iterative DFS, summing
  the island's values as we go. Count the island if total % k == 0.
  Zeros are water and are never part of an island.
  Time complexity: O(m * n) — each cell visited once.
  Space complexity: O(m * n) worst case for the visited set / stack.
"""

from typing import List


class Solution:
    def countIslands(self, grid: List[List[int]], k: int) -> int:
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        visited = [[False] * n for _ in range(m)]
        count = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] <= 0 or visited[r][c]:
                    continue
                # Flood-fill this island, summing its values.
                total = 0
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    x, y = stack.pop()
                    total += grid[x][y]
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < m and 0 <= ny < n
                                and grid[nx][ny] > 0
                                and not visited[nx][ny]):
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if total % k == 0:
                    count += 1
        return count


if __name__ == "__main__":
    sol = Solution()
    assert sol.countIslands(
        [[0, 2, 1, 0, 0], [0, 5, 0, 0, 5], [0, 0, 1, 0, 0],
         [0, 1, 4, 7, 0], [0, 2, 0, 0, 8]], 5) == 2
    assert sol.countIslands(
        [[3, 0, 3, 0], [0, 3, 0, 3], [3, 0, 3, 0]], 3) == 6
    # Edge cases: no land, single divisible cell, single non-divisible cell.
    assert sol.countIslands([[0, 0], [0, 0]], 7) == 0
    assert sol.countIslands([[6]], 3) == 1
    assert sol.countIslands([[5]], 3) == 0
    print("All self-tests passed.")
