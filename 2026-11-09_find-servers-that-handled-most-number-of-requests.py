# LeetCode Daily Coding Challenge — 2026-11-09
# Problem: Find Servers That Handled Most Number of Requests
# Difficulty: Hard
# Topics: Array, Heap (Priority Queue), Simulation, Ordered Set
# Link: https://leetcode.com/problems/find-servers-that-handled-most-number-of-requests/
#
# Problem statement:
# You have k servers numbered from 0 to k-1 that are being used to handle
# multiple requests simultaneously. Each server has infinite computational
# capacity but cannot handle more than one request at a time. Requests are
# assigned to servers according to a specific algorithm:
#   - The i-th (0-indexed) request arrives.
#   - If all servers are busy, the request is dropped (not handled at all).
#   - If the (i % k)-th server is available, assign the request to that server.
#   - Otherwise, assign the request to the next available server (wrapping
#     around the list of servers and starting from 0 if necessary).
# You are given a strictly increasing array `arrival` of positive integers,
# where arrival[i] represents the arrival time of the i-th request, and
# another array `load`, where load[i] represents the load of the i-th request
# (the time it takes to complete). Your goal is to find the busiest server(s).
# A server is considered busiest if it handled the most number of requests
# successfully among all the servers.
# Return a list containing the IDs (0-indexed) of the busiest server(s).
# You may return the IDs in any order.
#
# Examples:
#   Example 1:
#     Input: k = 3, arrival = [1,2,3,4,5], load = [5,2,3,3,3]
#     Output: [1]
#     Explanation: The first 3 requests are handled by the first 3 servers
#     in order. Request 3 comes in. Server 0 is busy, so it is assigned to
#     the next available server, which is 1. Request 4 comes in. It cannot
#     be handled since all servers are busy, so it is dropped. Servers 0
#     and 2 handled one request each, while server 1 handled two requests.
#     Hence server 1 is the busiest server.
#   Example 2:
#     Input: k = 3, arrival = [1,2,3,4], load = [1,2,1,2]
#     Output: [0]
#     Explanation: The first 3 requests are handled by first 3 servers.
#     Request 3 comes in. It is handled by server 0 since the server is
#     available. Server 0 handled two requests, while servers 1 and 2
#     handled one request each. Hence server 0 is the busiest server.
#   Example 3:
#     Input: k = 3, arrival = [1,2,3], load = [10,12,11]
#     Output: [0,1,2]
#     Explanation: Each server handles a single request, so they are all
#     considered the busiest.
#
# Constraints:
#   1 <= k <= 10^5
#   1 <= arrival.length, load.length <= 10^5
#   arrival.length == load.length
#   1 <= arrival[i], load[i] <= 10^9
#   arrival is strictly increasing.
#
# Approach:
#   - A min-heap `busy` holds (free_time, server_id) for servers currently
#     handling a request. Before handling request i, pop every entry with
#     free_time <= arrival[i] and mark that server available again.
#   - Availability is tracked with an iterative segment tree over the k
#     servers (leaf = 1 if available, 0 if busy). It supports point
#     updates and "first available server at or after position p" in
#     O(log k), including the wrap-around to position 0 — this replaces
#     the SortedList of the textbook solution without any third-party
#     dependency.
#   - Count how many requests each server handles; return every server
#     whose count equals the maximum.
#
# Time complexity: O(n log k) for n requests and k servers.
# Space complexity: O(k) for the segment tree, the busy heap and the counts.

import heapq
from typing import List


class Solution:
    def busiestServers(
        self, k: int, arrival: List[int], load: List[int]
    ) -> List[int]:
        n = len(arrival)
        counts = [0] * k

        # Iterative segment tree: tree[i] = number of available servers
        # in the covered range. Leaves start at index `size`.
        size = 1
        while size < k:
            size *= 2
        tree = [0] * (2 * size)
        for i in range(k):
            tree[size + i] = 1
        for i in range(size - 1, 0, -1):
            tree[i] = tree[2 * i] + tree[2 * i + 1]

        def set_available(idx: int, value: int) -> None:
            """Set leaf idx to value (1 = available, 0 = busy)."""
            p = size + idx
            tree[p] = value
            p //= 2
            while p:
                tree[p] = tree[2 * p] + tree[2 * p + 1]
                p //= 2

        def first_available(start: int) -> int:
            """Smallest available server id >= start, or -1 if none."""
            if tree[1] == 0:
                return -1

            def find(node: int, lo: int, hi: int) -> int:
                if tree[node] == 0 or hi <= start:
                    return -1
                if hi - lo == 1:
                    return lo if lo < k else -1
                mid = (lo + hi) // 2
                left = find(2 * node, lo, mid)
                if left != -1:
                    return left
                return find(2 * node + 1, mid, hi)

            return find(1, 0, size)

        busy = []  # heap of (free_time, server_id)

        for i in range(n):
            t = arrival[i]
            # Free every server whose request finished by time t.
            while busy and busy[0][0] <= t:
                _, sid = heapq.heappop(busy)
                set_available(sid, 1)

            if tree[1] == 0:
                continue  # all servers busy: request is dropped

            start = i % k
            sid = first_available(start)
            if sid == -1:  # nothing free in [start, k): wrap to 0
                sid = first_available(0)
            set_available(sid, 0)
            counts[sid] += 1
            heapq.heappush(busy, (t + load[i], sid))

        best = max(counts)
        return [sid for sid in range(k) if counts[sid] == best]


if __name__ == "__main__":
    sol = Solution()
    # Example 1
    assert sorted(sol.busiestServers(3, [1, 2, 3, 4, 5], [5, 2, 3, 3, 3])) == [1]
    # Example 2
    assert sorted(sol.busiestServers(3, [1, 2, 3, 4], [1, 2, 1, 2])) == [0]
    # Example 3
    assert sorted(sol.busiestServers(3, [1, 2, 3], [10, 12, 11])) == [0, 1, 2]
    # Single server: every request after the first is dropped while busy.
    assert sol.busiestServers(1, [1, 2, 10], [5, 1, 1]) == [0]
    # Wrap-around: request 3 starts at server 0 (busy), takes next free server 1.
    assert sol.busiestServers(3, [1, 2, 3, 5], [10, 1, 10, 1]) == [1]
    print("All self-tests passed.")
