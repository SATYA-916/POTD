# LeetCode Problem of the Day — 2026-11-16
# Title: Calculate Digit Sum of a String
# Difficulty: Easy
# Topics: String, Simulation
# Link: https://leetcode.com/problems/calculate-digit-sum-of-a-string/
#
# Problem:
# You are given a string s consisting of digits and an integer k.
# A round can be completed if the length of s is greater than k. In one
# round, do the following:
#   1. Divide s into consecutive groups of size k (the last group may be
#      smaller than k).
#   2. Replace each group with a string representing the sum of all its
#      digits. For example, "346" is replaced with "13" because
#      3 + 4 + 6 = 13.
#   3. Merge consecutive groups together to form a new string. If the
#      length of the string is greater than k, repeat from step 1.
# Return s after all rounds have been completed.
#
# Example 1:
#   Input: s = "11111222223", k = 3
#   Output: "135"
#   Explanation: Round 1: groups "111", "112", "222", "23" -> "3", "4",
#   "6", "5" -> s = "3465". Round 2: groups "346", "5" -> "13", "5" ->
#   s = "135". Now len(s) <= k, so return "135".
#
# Example 2:
#   Input: s = "00000000", k = 3
#   Output: "000"
#   Explanation: Groups "000", "000", "00" -> "0", "0", "0" -> s = "000",
#   whose length equals k, so return "000".
#
# Constraints:
#   1 <= s.length <= 100
#   2 <= k <= 100
#   s consists of digits only.
#
# Approach:
# Simulate the rounds exactly as described. In each round, walk s in
# chunks of size k, compute the digit sum of each chunk with sum(map(int,
# chunk)), and join the stringified sums. Stop once len(s) <= k.
#
# Time Complexity: O(n * rounds) — each round scans the string once and
#   the string shrinks by roughly a factor of k each round (n <= 100).
# Space Complexity: O(n) for the rebuilt string each round.


class Solution:
    def digitSum(self, s: str, k: int) -> str:
        while len(s) > k:
            parts = []
            for i in range(0, len(s), k):
                group = s[i:i + k]
                parts.append(str(sum(int(ch) for ch in group)))
            s = "".join(parts)
        return s


if __name__ == "__main__":
    sol = Solution()
    # Example 1
    assert sol.digitSum("11111222223", 3) == "135"
    # Example 2
    assert sol.digitSum("00000000", 3) == "000"
    # Already short enough: no rounds needed
    assert sol.digitSum("12", 5) == "12"
    # Single round, exact groups
    assert sol.digitSum("123", 2) == "33"
    # Multiple rounds with a multi-digit group sum
    assert sol.digitSum("999", 2) == "99"
    print("All self-tests passed.")
