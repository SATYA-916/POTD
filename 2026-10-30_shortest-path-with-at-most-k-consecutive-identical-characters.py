"""LeetCode Problem of the Day — 2026-10-30
Title: Shortest Path With At Most K Consecutive Identical Characters
Difficulty: Medium
Topics: String, Graph Theory, Heap (Priority Queue), Shortest Path
Link: https://leetcode.com/problems/shortest-path-with-at-most-k-consecutive-identical-characters/

Problem statement:
    You are given an integer n representing the number of nodes in a directed
    weighted graph, numbered from 0 to n - 1. This is represented by a 2D
    integer array edges, where edges[i] = [u_i, v_i, w_i] represents a directed
    edge from node u_i to node v_i with weight w_i.
    You are also given a string labels of length n, where labels[i] is the
    character assigned to node i, and an integer k.
    Return the minimum total edge weight of a path from node 0 to node n - 1
    such that the concatenation of the labels of the nodes along the path
    contains at most k consecutive identical characters. If no valid path
    exists, return -1.

Examples:
    Example 1:
        Input: n = 3, edges = [[0,1,1],[1,2,1],[0,2,3]], labels = "aab", k = 1
        Output: 3
        Explanation: Path 0 -> 2 gives "ab", which is valid for k = 1.
    Example 2:
        Input: n = 3, edges = [[0,1,1],[1,2,1],[0,2,3]], labels = "aab", k = 2
        Output: 2
        Explanation: Path 0 -> 1 -> 2 gives "aab", valid for k = 2.
    Example 3:
        Input: n = 3, edges = [[0,1,1],[1,2,1]], labels = "aaa", k = 2
        Output: -1
        Explanation: The only path gives "aaa", which exceeds k = 2.

Constraints:
    1 <= n == labels.length <= 5 * 10^4
    0 <= edges.length <= 5 * 10^4
    edges[i] == [u_i, v_i, w_i]; 0 <= u_i, v_i < n; u_i != v_i; 1 <= w_i <= 10^4
    labels consists of lowercase English letters; 1 <= k <= 50

Approach:
    Dijkstra over an expanded state graph. A state is (node, run), where run
    is the length of the trailing run of identical characters on the path
    ending at node. The last character itself needs no extra dimension: it is
    simply labels[node]. From state (u, run), traversing edge u -> v gives
    new_run = run + 1 if labels[v] == labels[u] else 1; the transition is
    discarded when new_run > k. All weights are positive, so the first time
    Dijkstra pops any state at node n - 1, its distance is the answer.
    (The n == 1 case is a zero-length path with run 1 <= k, so the answer
    is 0.)
    Time:  O(E * k * log(n * k)) — each state has out-degree bounded by the
           graph, and there are at most n * k states.
    Space: O(n * k + E) for the distance table and adjacency list.
"""

import heapq
from typing import List


class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], labels: str, k: int) -> int:
        if n == 1:
            return 0  # single node, run of 1 <= k (k >= 1)

        adj: List[List[tuple]] = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))

        INF = float("inf")
        # dist[node][run] for run in 1..k
        dist = [[INF] * (k + 1) for _ in range(n)]
        dist[0][1] = 0
        heap = [(0, 0, 1)]  # (cost, node, run)

        while heap:
            cost, u, run = heapq.heappop(heap)
            if cost != dist[u][run]:
                continue
            if u == n - 1:
                return cost  # Dijkstra: first pop at target is optimal
            for v, w in adj[u]:
                new_run = run + 1 if labels[v] == labels[u] else 1
                if new_run > k:
                    continue
                new_cost = cost + w
                if new_cost < dist[v][new_run]:
                    dist[v][new_run] = new_cost
                    heapq.heappush(heap, (new_cost, v, new_run))

        return -1


if __name__ == "__main__":
    sol = Solution()
    assert sol.shortestPath(3, [[0, 1, 1], [1, 2, 1], [0, 2, 3]], "aab", 1) == 3
    assert sol.shortestPath(3, [[0, 1, 1], [1, 2, 1], [0, 2, 3]], "aab", 2) == 2
    assert sol.shortestPath(3, [[0, 1, 1], [1, 2, 1]], "aaa", 2) == -1
    # Single node: zero-length path.
    assert sol.shortestPath(1, [], "a", 1) == 0
    # No edges at all: unreachable.
    assert sol.shortestPath(2, [], "ab", 1) == -1
    # A cheaper path that violates k must be skipped in favour of a valid one.
    assert sol.shortestPath(3, [[0, 1, 1], [1, 2, 1], [0, 2, 10]], "aab", 1) == 10
    print("All self-tests passed.")
