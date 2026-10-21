# LeetCode Problem of the Day — 2026-10-21
# Title: Minimum Operations to Sort a String
# Difficulty: Medium
# Topics: String
# Link: https://leetcode.com/problems/minimum-operations-to-sort-a-string/
#
# Problem statement:
# You are given a string s consisting of lowercase English letters.
# In one operation, you can select any substring of s that is not the entire
# string and sort it in non-descending alphabetical order.
# Return the minimum number of operations required to make s sorted in
# non-descending order. If it is not possible, return -1.
#
# Examples:
#   Example 1: Input: s = "dog"  -> Output: 1
#     Sort substring "og" to "go"; s becomes "dgo", which is sorted.
#   Example 2: Input: s = "card" -> Output: 2
#     Sort "car" -> "acr" (s = "acrd"), then sort "rd" -> "dr" (s = "acdr").
#   Example 3: Input: s = "gf"   -> Output: -1 (impossible)
#
# Constraints:
#   1 <= s.length <= 10^5
#   s consists of only lowercase English letters.
#
# Approach:
# Let t = sorted(s). One operation can sort any *proper* substring.
#   - 0 ops: s is already sorted.
#   - 1 op : if the first char is already correct (s[0] == t[0]), sorting the
#            suffix s[1:] fixes everything; likewise if the last char is
#            already correct (s[-1] == t[-1]), sorting the prefix s[:n-1]
#            fixes everything.
#   - -1   : n == 2 and s unsorted — every proper substring has length 1, so
#            no operation can change anything.
#   - 2 ops: otherwise, whenever the global minimum occurs somewhere in
#            s[:n-1] (i.e. s[-1] is not the *unique* minimum), sorting
#            s[:n-1] then s[1:] yields t; symmetrically, if the global
#            maximum occurs in s[1:] (s[0] not the unique maximum), sorting
#            s[1:] then s[:n-1] yields t. At least one of these holds unless
#            s[0] is the unique maximum AND s[-1] is the unique minimum.
#   - 3 ops: the remaining case (s[0] is the unique max, s[-1] the unique
#            min, n >= 3). Any single operation leaves a string whose first
#            and last chars are still wrong (the unique max/min can never be
#            placed correctly by one proper-substring sort), so 2 ops are
#            impossible; sorting s[:n-1] once breaks the deadlock and the
#            result falls into the 2-op case.
# The answer is therefore always in {0, 1, 2, 3, -1}.
#
# Time complexity:  O(n) — a constant number of scans/sorts of the string.
# Space complexity: O(n) for the sorted copy.

class Solution:
    def minOperations(self, s: str) -> int:
        n = len(s)
        t = sorted(s)
        if list(s) == t:
            return 0
        if s[0] == t[0] or s[-1] == t[-1]:
            return 1
        if n == 2:
            return -1
        # 3-op case: first char is the unique maximum and last char the unique minimum.
        if s[0] == t[-1] and s.count(s[0]) == 1 and s[-1] == t[0] and s.count(s[-1]) == 1:
            return 3
        return 2


if __name__ == "__main__":
    sol = Solution()
    # Sample examples from the statement.
    assert sol.minOperations("dog") == 1
    assert sol.minOperations("card") == 2
    assert sol.minOperations("gf") == -1
    # Edge cases.
    assert sol.minOperations("a") == 0
    assert sol.minOperations("ab") == 0
    assert sol.minOperations("ba") == -1
    assert sol.minOperations("abc") == 0
    assert sol.minOperations("cba") == 3      # unique max first, unique min last
    assert sol.minOperations("dcba") == 3
    assert sol.minOperations("bca") == 2      # min unique at end, but max 'c' sits in s[1:]
    assert sol.minOperations("acb") == 1      # s[0] == 'a' == t[0]
    assert sol.minOperations("bac") == 1      # s[-1] == 'c' == t[-1]
    assert sol.minOperations("cabb") == 2     # t='abbc': ends wrong, starts wrong, 'b' not unique min
    assert sol.minOperations("aaab") == 0
    assert sol.minOperations("baaa") == 2     # t='aaab': min 'a' repeats, so strategy A sorts in 2
    print("All self-tests passed.")
