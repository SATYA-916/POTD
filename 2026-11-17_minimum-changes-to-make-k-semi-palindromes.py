# Minimum Changes to Make K Semi-palindromes
# LeetCode Problem of the Day - 2026-11-17
# Difficulty: Hard
# Topics: Two Pointers, String, Dynamic Programming
# Link: https://leetcode.com/problems/minimum-changes-to-make-k-semi-palindromes/
#
# Problem:
# Given a string s and an integer k, partition s into k substrings such that
# the letter changes needed to make each substring a semi-palindrome are
# minimized. Return the minimum number of letter changes required.
#
# A semi-palindrome is a string that can be divided into palindromes based on
# a repeating pattern. To check if a string is a semi-palindrome:
#   1. Choose a positive divisor d of the string's length, 1 <= d < length.
#      (A string of length 1 has no valid divisor.)
#   2. Split the string into d groups: group r holds the characters at
#      positions r, r + d, r + 2d, ... (0-based within the substring).
#   3. The string is a semi-palindrome if every group forms a palindrome.
#
# Example 1:
#   Input: s = "abcac", k = 2
#   Output: 1
#   Explanation: Divide s into "ab" and "cac". "cac" is already a
#   semi-palindrome. Change "ab" to "aa" and it becomes a semi-palindrome
#   with d = 1.
#
# Example 2:
#   Input: s = "abcdef", k = 2
#   Output: 2
#   Explanation: Divide s into "abc" and "def". Each needs one change to
#   become a semi-palindrome.
#
# Example 3:
#   Input: s = "aabbaa", k = 3
#   Output: 0
#   Explanation: Divide s into "aa", "bb" and "aa". All are already
#   semi-palindromes.
#
# Constraints:
#   2 <= s.length <= 200
#   1 <= k <= s.length / 2
#   s contains only lowercase English letters.
#
# Approach:
#   1. Precompute, for every step d and residue r, the cost of turning any
#      contiguous run of the subsequence s[r], s[r+d], s[r+2d], ... into a
#      palindrome (mismatched symmetric pairs). This is a classic
#      interval DP: cost[a][b] = cost[a+1][b-1] + (chars differ).
#   2. semi_cost(l, r): for each divisor d of the substring length
#      (1 <= d < length), add up the palindrome costs of the d residue
#      groups and take the minimum. Length-1 substrings cost infinity
#      (they have no valid divisor).
#   3. Partition DP: dp[t][i] = min cost to split the first i characters
#      into t semi-palindromes, trying every split point for the last part.
#
# Time complexity: O(n^2 * sqrt-ish) for the precomputation plus
# O(k * n^2) for the partition DP (n <= 200).
# Space complexity: O(n^2) for the precomputed tables and the DP.


class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        INF = float("inf")

        # pal[(d, r)] = (idx, f) where idx lists the positions r, r+d, ...
        # and f[a][b] is the cost of making idx[a..b] a palindrome.
        pal = {}
        for d in range(1, n):
            for r in range(d):
                idx = list(range(r, n, d))
                m = len(idx)
                f = [[0] * m for _ in range(m)]
                for length in range(2, m + 1):
                    for a in range(m - length + 1):
                        b = a + length - 1
                        f[a][b] = f[a + 1][b - 1] + (s[idx[a]] != s[idx[b]])
                pal[(d, r)] = (idx, f)

        def semi_cost(l: int, r: int) -> int:
            """Min changes to make s[l..r] a semi-palindrome (inf if impossible)."""
            length = r - l + 1
            if length == 1:
                return INF
            best = INF
            for d in range(1, length):
                if length % d:
                    continue
                total = 0
                for rho in range(d):
                    start = l + rho
                    res = start % d
                    _, f = pal[(d, res)]
                    a = (start - res) // d
                    b = (r - res) // d
                    if b >= a:
                        total += f[a][b]
                best = min(best, total)
            return best

        # cost[l][r]: min changes to make s[l..r] a semi-palindrome.
        cost = [[INF] * n for _ in range(n)]
        for l in range(n):
            for r in range(l + 1, n):
                cost[l][r] = semi_cost(l, r)

        # dp[t][i]: min cost to partition the first i characters into t parts.
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        dp[0][0] = 0
        for t in range(1, k + 1):
            for i in range(1, n + 1):
                for j in range(t - 1, i - 1):
                    if dp[t - 1][j] < INF and cost[j][i - 1] < INF:
                        dp[t][i] = min(dp[t][i], dp[t - 1][j] + cost[j][i - 1])
        return dp[k][n]


if __name__ == "__main__":
    sol = Solution()
    # LeetCode examples
    assert sol.minimumChanges("abcac", 2) == 1
    assert sol.minimumChanges("abcdef", 2) == 2
    assert sol.minimumChanges("aabbaa", 3) == 0
    # Extra hand-checked cases
    assert sol.minimumChanges("aa", 1) == 0
    assert sol.minimumChanges("ab", 1) == 1
    assert sol.minimumChanges("abcd", 1) == 2
    assert sol.minimumChanges("abca", 1) == 1
    assert sol.minimumChanges("abcabc", 1) == 0  # d = 3 groups "aa","bb","cc"
    assert sol.minimumChanges("aaaa", 1) == 0
    assert sol.minimumChanges("abcaab", 1) == 0  # d = 2 groups "aca","bab"
    assert sol.minimumChanges("abcdef", 1) == 2  # best d = 2: "ace","bdf" -> 1 + 1
    print("All self-tests passed.")
