# Count Zero Request Servers
# Date: 2026-11-06
# Difficulty: Medium
# Topics: Array, Hash Table, Sliding Window, Sorting
# LeetCode: https://leetcode.com/problems/count-zero-request-servers/
#
# Problem statement:
# You are given an integer n denoting the total number of servers and a 2D
# 0-indexed integer array logs, where logs[i] = [server_id, time] denotes that
# the server with id server_id received a request at time time.
# You are also given an integer x and a 0-indexed integer array queries.
# Return a 0-indexed integer array arr of length queries.length where arr[i]
# represents the number of servers that did not receive any requests during
# the time interval [queries[i] - x, queries[i]].
# Note that the time intervals are inclusive.
#
# Example 1:
#   Input: n = 3, logs = [[1,3],[2,6],[1,5]], x = 5, queries = [10,11]
#   Output: [1,2]
#   Explanation:
#     For queries[0]: servers 1 and 2 get requests in [5, 10], so only server 3
#     gets zero requests.
#     For queries[1]: only server 2 gets a request in [6, 11], so servers 1 and 3
#     get zero requests.
#
# Example 2:
#   Input: n = 3, logs = [[2,4],[2,1],[1,2],[3,1]], x = 2, queries = [3,4]
#   Output: [0,1]
#   Explanation:
#     For queries[0]: all servers get at least one request in [1, 3].
#     For queries[1]: only server 3 gets no request in [2, 4].
#
# Constraints:
#   1 <= n <= 10^5
#   1 <= logs.length <= 10^5
#   1 <= queries.length <= 10^5
#   logs[i].length == 2
#   1 <= logs[i][0] <= n
#   1 <= logs[i][1] <= 10^6
#   1 <= x <= 10^5
#   x < queries[i] <= 10^6
#
# Approach:
# Sort logs by time and process the queries in increasing order, keeping a
# sliding window of logs whose times fall inside [query - x, query]. A hash map
# counts how many in-window requests each server has; a counter tracks how
# many distinct servers have at least one request in the window. As the window
# slides forward, logs older than query - x drop out (decrementing their
# server's count, and the distinct count when it hits zero) and logs up to
# query enter. The answer for a query is n minus the distinct servers in its
# window. Sorting dominates the cost.
#
# Time complexity: O((L + Q) log (L + Q)) for sorting logs and queries,
#   where L = len(logs), Q = len(queries); the sweep itself is O(L + Q).
# Space complexity: O(L + Q) for the sorted copies and the per-server counts.

from typing import List


class Solution:
    def countServers(self, n: int, logs: List[List[int]], x: int,
                     queries: List[int]) -> List[int]:
        logs.sort(key=lambda log: log[1])
        ordered = sorted(range(len(queries)), key=lambda i: queries[i])

        counts = {}          # server_id -> requests inside the window
        distinct = 0         # servers with >= 1 request inside the window
        left = 0             # first log index still inside the window
        right = 0            # next log index to enter the window
        answer = [0] * len(queries)

        for qi in ordered:
            q = queries[qi]
            start = q - x

            while right < len(logs) and logs[right][1] <= q:
                server = logs[right][0]
                if counts.get(server, 0) == 0:
                    distinct += 1
                counts[server] = counts.get(server, 0) + 1
                right += 1

            while left < right and logs[left][1] < start:
                server = logs[left][0]
                counts[server] -= 1
                if counts[server] == 0:
                    distinct -= 1
                left += 1

            answer[qi] = n - distinct

        return answer


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    assert sol.countServers(
        3, [[1, 3], [2, 6], [1, 5]], 5, [10, 11]) == [1, 2]

    # Example 2
    assert sol.countServers(
        3, [[2, 4], [2, 1], [1, 2], [3, 1]], 2, [3, 4]) == [0, 1]

    # Edge: single server, request inside the window
    assert sol.countServers(1, [[1, 1]], 1, [2]) == [0]

    # Edge: no log falls inside the window
    assert sol.countServers(2, [[1, 5]], 3, [10]) == [2]

    # Edge: unordered queries, same server hit twice in one window
    assert sol.countServers(
        2, [[1, 2], [1, 3], [2, 9]], 5, [9, 4]) == [1, 1]

    print("All sample tests passed.")
