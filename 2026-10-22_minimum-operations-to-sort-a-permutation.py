# Minimum Operations to Sort a Permutation
# Date: 2026-10-22 | Difficulty: Medium | Topics: Array
# LeetCode: https://leetcode.com/problems/minimum-operations-to-sort-a-permutation/
#
# Problem statement:
#   You are given an integer array nums of length n, where nums is a permutation
#   of the integers from 0 to n - 1.
#   You may perform ONLY the following operations:
#     - Reverse the entire array.
#     - Rotate Left by One: move the first element to the end, and the rest
#       left by one position.
#   Return the minimum number of operations required to sort the array in
#   increasing order. If it is not possible, return -1.
#
# Examples:
#   1. nums = [0,2,1] -> 2
#        Rotate left: [2,1,0], then reverse: [0,1,2]
#   2. nums = [1,0,2] -> 2
#        Reverse: [2,0,1], then rotate left: [0,1,2]
#   3. nums = [2,0,1,3] -> -1 (impossible)
#
# Constraints:
#   1 <= n == nums.length <= 10^5
#   0 <= nums[i] <= n - 1
#   nums is a permutation of integers from 0 to n - 1.
#
# Approach:
#   The two operations generate the dihedral group of order 2n: every reachable
#   configuration is either a rotation of nums or a rotation of reversed(nums).
#   Represent a configuration as (rev, k) = "rotate-left-k of (nums or its
#   reverse)". Transitions:
#     - Rotate left:  (rev, k) -> (rev, (k+1) % n)
#     - Reverse:      (rev, k) -> (1-rev, (n-k) % n)
#       (reverse of rotate-left-k of X = rotate-right-k of reverse(X))
#   A state is the sorted target iff its rotation offset k lines up the base
#   with 0..n-1, i.e. base[i] == (i - k) % n for all i; the needed k is forced
#   by base[0]: k = (-base[0]) % n. BFS from (0, 0) over the 2n states finds
#   the minimum number of operations; if no target state is reachable, -1.
#
# Time complexity:  O(n) — at most 2n states, O(1) work per state.
# Space complexity: O(n) for the visited set / BFS queue.

from collections import deque
from typing import List


class Solution:
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        base0 = nums
        base1 = nums[::-1]

        def target_offset(base: List[int]):
            """Rotation k such that rot-left-k(base) == [0..n-1], else None."""
            k = (-base[0]) % n
            for i, v in enumerate(base):
                if v != (i - k) % n:
                    return None
            return k

        k0 = target_offset(base0)
        k1 = target_offset(base1)
        targets = set()
        if k0 is not None:
            targets.add((0, k0))
        if k1 is not None:
            targets.add((1, k1))
        if not targets:
            return -1

        start = (0, 0)
        if start in targets:
            return 0
        dist = {start: 0}
        q = deque([start])
        while q:
            rev, k = q.popleft()
            d = dist[(rev, k)] + 1
            for nxt in ((rev, (k + 1) % n), (1 - rev, (n - k) % n)):
                if nxt not in dist:
                    if nxt in targets:
                        return d
                    dist[nxt] = d
                    q.append(nxt)
        return -1


if __name__ == "__main__":
    s = Solution()
    # Provided examples
    assert s.minOperations([0, 2, 1]) == 2
    assert s.minOperations([1, 0, 2]) == 2
    assert s.minOperations([2, 0, 1, 3]) == -1
    # Edge cases
    assert s.minOperations([0]) == 0
    assert s.minOperations([0, 1, 2]) == 0
    assert s.minOperations([1, 0]) == 1          # one reverse
    assert s.minOperations([1, 2, 0]) == 2       # two left-rotations
    # Exhaustive cross-check vs brute-force array BFS for all perms of 0..4
    from itertools import permutations

    def brute(nums):
        target = tuple(sorted(nums))
        seen = {tuple(nums): 0}
        q = deque([tuple(nums)])
        while q:
            cur = q.popleft()
            d = seen[cur]
            if cur == target:
                return d
            rot = cur[1:] + cur[:1]
            rev = cur[::-1]
            for nxt in (rot, rev):
                if nxt not in seen:
                    seen[nxt] = d + 1
                    q.append(nxt)
        return -1

    for p in permutations(range(5)):
        assert s.minOperations(list(p)) == brute(list(p)), p
    print("All self-tests passed.")
