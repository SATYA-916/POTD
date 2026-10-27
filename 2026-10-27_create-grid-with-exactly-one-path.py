# Create Grid With Exactly One Path
# Date: 2026-10-27
# Difficulty: Easy
# Topics: (none listed by LeetCode for this problem)
# LeetCode: https://leetcode.com/problems/create-grid-with-exactly-one-path/
#
# Problem statement:
#   Given m rows and n columns, construct any m x n grid of '.' (free) and
#   '#' (obstacle) such that there is exactly one valid path from the
#   top-left cell (0, 0) to the bottom-right cell (m - 1, n - 1), moving
#   only right or down through free cells.
#
# Examples:
#   Input: m = 2, n = 3 -> one valid answer: ["..#", "#.."]
#     (only path: (0,0) -> (0,1) -> (1,1) -> (1,2))
#   Input: m = 3, n = 3 -> one valid answer: ["..#", "#..", "##."]
#     (only path: (0,0) -> (0,1) -> (1,1) -> (1,2) -> (2,2))
#   Input: m = 1, n = 4 -> ["...."]
#     (only path: straight right across the single row)
#
# Constraints:
#   1 <= m, n <= 25
#
# Approach:
#   Keep exactly one "corridor" free and block everything else: free the
#   entire top row and the entire last column, and fill the rest with '#'.
#   From (0, 0), moving down is blocked, so the path must go right along
#   the top row; once it reaches the last column, moving right is
#   impossible and moving left is blocked, so it must go straight down.
#   Hence exactly one right/down path exists. This also covers the
#   degenerate cases: a single row (just the top row) and a single column
#   (top row and last column coincide), including 1 x 1.
#
# Time complexity: O(m * n) to build the grid.
# Space complexity: O(m * n) for the returned grid.


class Solution:
    def createGrid(self, m: int, n: int) -> list[str]:
        grid = [["#"] * n for _ in range(m)]
        for j in range(n):
            grid[0][j] = "."
        for i in range(m):
            grid[i][n - 1] = "."
        return ["".join(row) for row in grid]


def _count_paths(grid: list[str]) -> int:
    """Count right/down paths from (0, 0) to the bottom-right free cell."""
    m, n = len(grid), len(grid[0])
    if grid[0][0] == "#" or grid[m - 1][n - 1] == "#":
        return 0
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "#" or (i == 0 and j == 0):
                continue
            if i > 0:
                dp[i][j] += dp[i - 1][j]
            if j > 0:
                dp[i][j] += dp[i][j - 1]
    return dp[m - 1][n - 1]


if __name__ == "__main__":
    sol = Solution()
    # Sample inputs: our grid need not match the examples verbatim, but
    # each must be a valid m x n grid with exactly one valid path.
    for m, n in [(2, 3), (3, 3), (1, 4)]:
        grid = sol.createGrid(m, n)
        assert len(grid) == m and all(len(row) == n for row in grid)
        assert set("".join(grid)) <= {".", "#"}
        assert _count_paths(grid) == 1, (m, n, grid)
    # Edge cases, including the smallest and largest allowed grids.
    for m, n in [(1, 1), (1, 25), (25, 1), (25, 25), (5, 1), (1, 5)]:
        grid = sol.createGrid(m, n)
        assert len(grid) == m and all(len(row) == n for row in grid)
        assert _count_paths(grid) == 1, (m, n, grid)
    # Exhaustive check over all small sizes.
    for m in range(1, 8):
        for n in range(1, 8):
            assert _count_paths(sol.createGrid(m, n)) == 1, (m, n)
    print("All self-tests passed.")
