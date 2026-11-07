# LeetCode Problem of the Day — 2026-11-07
# Title: Process Tasks Using Servers
# Difficulty: Medium
# Topics: Array, Heap (Priority Queue)
# Link: https://leetcode.com/problems/process-tasks-using-servers/
#
# Problem statement:
# You are given two 0-indexed integer arrays `servers` and `tasks` of lengths
# n and m respectively. servers[i] is the weight of the i-th server, and
# tasks[j] is the time needed to process the j-th task in seconds.
#
# Tasks are assigned to the servers using a task queue. Initially, all servers
# are free, and the queue is empty.
#
# At second j, the j-th task is inserted into the queue (starting with the
# 0-th task being inserted at second 0). As long as there are free servers
# and the queue is not empty, the task in the front of the queue will be
# assigned to a free server with the smallest weight, and in case of a tie,
# it is assigned to a free server with the smallest index.
#
# If there are no free servers and the queue is not empty, we wait until a
# server becomes free and immediately assign the next task. If multiple
# servers become free at the same time, then multiple tasks from the queue
# will be assigned in order of insertion following the weight and index
# priorities above.
#
# A server that is assigned task j at second t will be free again at second
# t + tasks[j].
#
# Build an array ans of length m, where ans[j] is the index of the server
# the j-th task will be assigned to. Return the array ans.
#
# Example 1:
#   Input: servers = [3,3,2], tasks = [1,2,3,2,1,2]
#   Output: [2,2,0,2,1,2]
#
# Example 2:
#   Input: servers = [5,1,4,3,2], tasks = [2,1,2,4,5,2,1]
#   Output: [1,4,1,4,1,3,2]
#
# Constraints:
#   servers.length == n, tasks.length == m
#   1 <= n, m <= 2 * 10^5
#   1 <= servers[i], tasks[j] <= 2 * 10^5
#
# Approach:
# Two min-heaps simulate the process. `available` holds free servers keyed by
# (weight, index) so the lightest (then lowest-index) server is picked first.
# `busy` holds occupied servers keyed by (free_time, weight, index). Tasks
# arrive one per second in order, so we walk through them in order, keeping a
# clock that never moves backwards. Before assigning task j, we advance the
# clock to at least j and release every server whose free time has passed.
# If no server is free, we fast-forward the clock to the earliest free time
# and release all servers free by then. The chosen server's free time becomes
# clock + tasks[j].
#
# Time complexity: O((n + m) log n) — each server/task is pushed/popped a
# constant number of times.
# Space complexity: O(n) for the two heaps.

import heapq
from typing import List


class Solution:
    def assignTasks(self, servers: List[int], tasks: List[int]) -> List[int]:
        available = [(weight, index) for index, weight in enumerate(servers)]
        heapq.heapify(available)  # free servers, keyed by (weight, index)

        busy = []  # occupied servers, keyed by (free_time, weight, index)
        ans = [0] * len(tasks)
        clock = 0

        for j, duration in enumerate(tasks):
            clock = max(clock, j)

            # Release every server that has finished by now.
            while busy and busy[0][0] <= clock:
                free_time, weight, index = heapq.heappop(busy)
                heapq.heappush(available, (weight, index))

            # No free server: wait until the earliest one becomes free.
            if not available:
                clock = busy[0][0]
                while busy and busy[0][0] <= clock:
                    free_time, weight, index = heapq.heappop(busy)
                    heapq.heappush(available, (weight, index))

            weight, index = heapq.heappop(available)
            ans[j] = index
            heapq.heappush(busy, (clock + duration, weight, index))

        return ans


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    assert sol.assignTasks([3, 3, 2], [1, 2, 3, 2, 1, 2]) == [2, 2, 0, 2, 1, 2]

    # Example 2
    assert sol.assignTasks([5, 1, 4, 3, 2], [2, 1, 2, 4, 5, 2, 1]) == [1, 4, 1, 4, 1, 3, 2]

    # Single server handles tasks one after another, in order.
    assert sol.assignTasks([10], [5, 5, 5]) == [0, 0, 0]

    # Task arriving while all servers are busy waits for the earliest free one.
    assert sol.assignTasks([1, 2], [5, 5, 1]) == [0, 1, 0]

    print("All sample tests passed.")
