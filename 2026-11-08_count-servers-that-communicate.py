# LeetCode Problem of the Day — 2026-11-08
# Title: Count Servers that Communicate
# Difficulty: Medium
# Topics: Array, Depth-First Search, Breadth-First Search, Union-Find, Matrix, Counting
# URL: https://leetcode.com/problems/count-servers-that-communicate/
#
# Problem:
# You are given a map of a server center, represented as an m * n integer matrix
# grid, where 1 means that on that cell there is a server and 0 means that it is
# no server. Two servers are said to communicate if they are on the same row or
# on the same column.
#
# Return the number of servers that communicate with any other server.
#
# Example 1:
#   Input: grid = [[1,0],[0,1]]
#   Output: 0
#   Explanation: No servers can communicate with others.
#
# Example 2:
#   Input: grid = [[1,0],[1,1]]
#   Output: 3
#   Explanation: All three servers can communicate with at least one other server.
#
# Example 3:
#   Input: grid = [[1,1,0,0],[0,0,1,0],[0,0,1,0],[0,0,0,1]]
#   Output: 4
#   Explanation: The two servers in the first row can communicate with each
#   other. The two servers in the third column can communicate with each other.
#   The server at right bottom corner can't communicate with any other server.
#
# Constraints:
#   m == grid.length
#   n == grid[i].length
#   1 <= m <= 250
#   1 <= n <= 250
#   grid[i][j] == 0 or 1
#
# Approach:
# A server communicates iff there is at least one other server in its row or
# its column. Count how many servers sit in each row and each column in one
# pass, then count every server whose row count > 1 or column count > 1.
#
# Time complexity: O(m * n) — two passes over the grid.
# Space complexity: O(m + n) — one count per row and per column.
from typing import List


class Solution:
    def countServers(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        row_count = [0] * m
        col_count = [0] * n

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    row_count[i] += 1
                    col_count[j] += 1

        total = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and (row_count[i] > 1 or col_count[j] > 1):
                    total += 1
        return total


if __name__ == "__main__":
    sol = Solution()
    assert sol.countServers([[1, 0], [0, 1]]) == 0
    assert sol.countServers([[1, 0], [1, 1]]) == 3
    assert sol.countServers([[1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) == 4
    # Extra checks: single server, full grid, one row of servers.
    assert sol.countServers([[1]]) == 0
    assert sol.countServers([[1, 1], [1, 1]]) == 4
    assert sol.countServers([[1, 1, 1]]) == 3
    print("All sample tests passed.")
