# Number of Closed Islands
# Date: 2026-10-25 | Difficulty: Medium | Topics: Array, Depth-First Search, Breadth-First Search, Union-Find, Matrix
# LeetCode: https://leetcode.com/problems/number-of-closed-islands/
#
# Problem statement:
#   Given a 2D grid consisting of 0s (land) and 1s (water). An island is a
#   maximal 4-directionally connected group of 0s, and a closed island is
#   an island totally (all left, top, right, bottom) surrounded by 1s.
#   Return the number of closed islands.
#
# Examples:
#   1. grid = [[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],
#              [1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]] -> 2
#   2. grid = [[0,0,1,0,0],[0,1,0,1,0],[0,1,1,1,0]] -> 1
#   3. grid = [[1,1,1,1,1,1,1],[1,0,0,0,0,0,1],[1,0,1,1,1,0,1],
#              [1,0,1,0,1,0,1],[1,0,1,1,1,0,1],[1,0,0,0,0,0,1],
#              [1,1,1,1,1,1,1]] -> 2
#
# Constraints:
#   1 <= grid.length, grid[0].length <= 100
#   0 <= grid[i][j] <= 1
#
# Approach:
#   Any island that touches the border can never be closed, so first
#   flood-fill (iterative DFS) every border-connected 0 into water (1).
#   Whatever 0s remain belong to closed islands only: scan the grid and,
#   for each remaining 0, flood-fill its whole island and count one.
#
# Time complexity:  O(m * n) — each cell is visited a constant number of times.
# Space complexity: O(m * n) in the worst case for the DFS stack.

from typing import List


class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        g = [row[:] for row in grid]

        def flood_fill(r: int, c: int) -> None:
            stack = [(r, c)]
            g[r][c] = 1
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and g[nx][ny] == 0:
                        g[nx][ny] = 1
                        stack.append((nx, ny))

        # Phase 1: sink all border-connected land.
        for i in range(m):
            for j in (0, n - 1):
                if g[i][j] == 0:
                    flood_fill(i, j)
        for j in range(n):
            for i in (0, m - 1):
                if g[i][j] == 0:
                    flood_fill(i, j)

        # Phase 2: count the islands that remain.
        count = 0
        for i in range(m):
            for j in range(n):
                if g[i][j] == 0:
                    count += 1
                    flood_fill(i, j)
        return count


if __name__ == "__main__":
    s = Solution()
    # Provided examples
    assert s.closedIsland([[1, 1, 1, 1, 1, 1, 1, 0],
                           [1, 0, 0, 0, 0, 1, 1, 0],
                           [1, 0, 1, 0, 1, 1, 1, 0],
                           [1, 0, 0, 0, 0, 1, 0, 1],
                           [1, 1, 1, 1, 1, 1, 1, 0]]) == 2
    assert s.closedIsland([[0, 0, 1, 0, 0],
                           [0, 1, 0, 1, 0],
                           [0, 1, 1, 1, 0]]) == 1
    assert s.closedIsland([[1, 1, 1, 1, 1, 1, 1],
                           [1, 0, 0, 0, 0, 0, 1],
                           [1, 0, 1, 1, 1, 0, 1],
                           [1, 0, 1, 0, 1, 0, 1],
                           [1, 0, 1, 1, 1, 0, 1],
                           [1, 0, 0, 0, 0, 0, 1],
                           [1, 1, 1, 1, 1, 1, 1]]) == 2
    # Edge cases
    assert s.closedIsland([[1]]) == 0
    assert s.closedIsland([[0]]) == 0          # touches the border
    assert s.closedIsland([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]]) == 1    # single enclosed cell
    assert s.closedIsland([[1, 1],
                           [1, 1]]) == 0       # no land at all
    print("All self-tests passed.")
