# Palindromic Path Queries in a Tree
# Date: 2026-10-29
# Difficulty: Hard
# Topics: Array, String, Divide and Conquer, Bit Manipulation, Tree,
#         Depth-First Search, Binary Indexed Tree, Segment Tree
# LeetCode: https://leetcode.com/problems/palindromic-path-queries-in-a-tree/
#
# Problem statement:
#   Given an undirected tree with n nodes (0..n-1) and a string s where
#   s[i] is the character at node i, process queries:
#     "update u c": set s[u] = c
#     "query u v":  can the characters on the unique path from u to v
#                  (inclusive) be rearranged into a palindrome?
#   Return a boolean array with one entry per "query" query, in order.
#
# Examples:
#   Example 1:
#     Input:  n = 3, edges = [[0,1],[1,2]], s = "aac",
#             queries = ["query 0 2", "update 1 b", "query 0 2"]
#     Output: [True, False]
#     Explanation: path 0-1-2 is "aac" -> "aca" (palindrome); after the
#     update it is "abc", which cannot be rearranged into a palindrome.
#   Example 2:
#     Input:  n = 4, edges = [[0,1],[0,2],[0,3]], s = "abca",
#             queries = ["query 1 2", "update 0 b", "query 2 3",
#                        "update 3 a", "query 1 3"]
#     Output: [False, False, True]
#
# Constraints:
#   1 <= n == len(s) <= 5 * 10**4
#   edges.length == n - 1, edges form a valid tree
#   1 <= len(queries) <= 5 * 10**4
#   queries[i] is "update u c" or "query u v" with c a lowercase letter.
#
# Approach:
#   A string can be rearranged into a palindrome iff at most one character
#   has odd count. Encode parity as a 26-bit mask: bit k is set iff the
#   character ('a' + k) occurs an odd number of times. A path is good iff
#   its mask has at most one bit set: mask & (mask - 1) == 0.
#   Let pref[x] be the XOR of single-bit masks on the root-to-x path
#   (inclusive). For u, v with w = lca(u, v), the path mask is
#   pref[u] ^ pref[v] ^ (1 << char[w]): ancestors above w cancel in pairs,
#   w itself cancels twice in pref[u] ^ pref[v] and is restored once.
#   Updates: changing s[u] toggles pref[x] for every descendant x of u
#   (including u) by delta = old_bit ^ new_bit. With an Euler tour, the
#   subtree of u is a contiguous interval, so this is a range-XOR-update /
#   point-query on a Fenwick tree; pref[x] = initial_pref[x] ^ bit_query(x).
#   LCA is answered with binary lifting.
#
# Time complexity:  O((n + q) log n)  (Fenwick + binary lifting)
# Space complexity: O(n log n) for the binary-lifting table
#                   (O(n) if LCA used a single parent chain instead).

from typing import List


class Solution:
    def palindromePath(self, n: int, edges: List[List[int]], s: str,
                       queries: List[str]) -> List[bool]:
        # --- Build the tree and an Euler tour (iterative DFS) ---
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        LOG = (n).bit_length()  # 2**LOG > n
        up = [[-1] * n for _ in range(LOG)]
        depth = [0] * n
        tin = [0] * n
        tout = [0] * n
        init_pref = [0] * n
        chars = [ord(c) - 97 for c in s]

        timer = 0
        # Stack entries: (node, parent, iterator-state) 0 = enter, 1 = exit
        stack = [(0, -1, 0)]
        init_pref[0] = 1 << chars[0]
        while stack:
            node, parent, state = stack.pop()
            if state == 0:
                tin[node] = timer
                timer += 1
                up[0][node] = parent
                stack.append((node, parent, 1))
                for nb in reversed(adj[node]):
                    if nb == parent:
                        continue
                    depth[nb] = depth[node] + 1
                    init_pref[nb] = init_pref[node] ^ (1 << chars[nb])
                    stack.append((nb, node, 0))
            else:
                tout[node] = timer - 1

        for k in range(1, LOG):
            prev, cur = up[k - 1], up[k]
            for v in range(n):
                anc = prev[v]
                cur[v] = prev[anc] if anc != -1 else -1

        def lca(a: int, b: int) -> int:
            if depth[a] < depth[b]:
                a, b = b, a
            diff = depth[a] - depth[b]
            bit = 0
            while diff:
                if diff & 1:
                    a = up[bit][a]
                diff >>= 1
                bit += 1
            if a == b:
                return a
            for k in range(LOG - 1, -1, -1):
                if up[k][a] != up[k][b]:
                    a = up[k][a]
                    b = up[k][b]
            return up[0][a]

        # --- Fenwick tree for range-XOR-update / point-query ---
        size = n + 2
        bit = [0] * size

        def bit_add(i: int, val: int) -> None:
            i += 1  # to 1-based
            while i < size:
                bit[i] ^= val
                i += i & -i

        def range_xor(l: int, r: int, val: int) -> None:
            if val == 0 or l > r:
                return
            bit_add(l, val)
            bit_add(r + 1, val)

        def point_query(i: int) -> int:
            i += 1
            res = 0
            while i > 0:
                res ^= bit[i]
                i -= i & -i
            return res

        def pref(node: int) -> int:
            return init_pref[node] ^ point_query(tin[node])

        # --- Process queries ---
        answer: List[bool] = []
        for q in queries:
            parts = q.split()
            if parts[0] == "update":
                u = int(parts[1])
                new_c = ord(parts[2]) - 97
                old_c = chars[u]
                if new_c != old_c:
                    delta = (1 << old_c) ^ (1 << new_c)
                    range_xor(tin[u], tout[u], delta)
                    chars[u] = new_c
            else:  # "query u v"
                u = int(parts[1])
                v = int(parts[2])
                w = lca(u, v)
                mask = pref(u) ^ pref(v) ^ (1 << chars[w])
                answer.append(mask & (mask - 1) == 0)
        return answer


if __name__ == "__main__":
    sol = Solution()
    # Example 1
    assert sol.palindromePath(
        3, [[0, 1], [1, 2]], "aac",
        ["query 0 2", "update 1 b", "query 0 2"]) == [True, False]
    # Example 2
    assert sol.palindromePath(
        4, [[0, 1], [0, 2], [0, 3]], "abca",
        ["query 1 2", "update 0 b", "query 2 3",
         "update 3 a", "query 1 3"]) == [False, False, True]
    # Single node: always a palindrome; update keeps it one.
    assert sol.palindromePath(
        1, [], "z", ["query 0 0", "update 0 a", "query 0 0"]) == [True, True]
    # Chain where an update flips the answer both ways.
    assert sol.palindromePath(
        4, [[0, 1], [1, 2], [2, 3]], "abba",
        ["query 0 3", "update 0 c", "query 0 3",
         "update 0 a", "query 0 3"]) == [True, False, True]
    # Ancestor query (u is the LCA) and a no-op update.
    assert sol.palindromePath(
        3, [[0, 1], [1, 2]], "aba",
        ["query 0 2", "update 1 b", "query 0 1"]) == [True, False]
    print("All self-tests passed.")
