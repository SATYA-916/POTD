# LeetCode Problem of the Day - 2026-11-22
# Title: Check if All A's Appears Before All B's
# Difficulty: Easy
# Topics: String
# Link: https://leetcode.com/problems/check-if-all-as-appears-before-all-bs/
#
# Problem Statement:
# Given a string s consisting of only the characters 'a' and 'b', return true
# if every 'a' appears before every 'b' in the string. Otherwise, return false.
#
# Example 1:
#   Input: s = "aaabbb"
#   Output: true
#   Explanation: The 'a's are at indices 0, 1, and 2, while the 'b's are at
#   indices 3, 4, and 5. Hence, every 'a' appears before every 'b'.
#
# Example 2:
#   Input: s = "abab"
#   Output: false
#   Explanation: There is an 'a' at index 2 and a 'b' at index 1.
#
# Example 3:
#   Input: s = "bbb"
#   Output: true
#   Explanation: There are no 'a's, hence every 'a' appears before every 'b'.
#
# Constraints:
#   1 <= s.length <= 100
#   s[i] is either 'a' or 'b'.
#
# Approach:
# Every 'a' appears before every 'b' exactly when the string never switches
# back from 'b' to 'a', i.e. the substring "ba" never occurs. A single scan
# (or a substring check) is enough.
#
# Time Complexity: O(n), where n is the length of s.
# Space Complexity: O(1).


class Solution:
    def checkString(self, s: str) -> bool:
        return "ba" not in s


if __name__ == "__main__":
    sol = Solution()
    assert sol.checkString("aaabbb") is True
    assert sol.checkString("abab") is False
    assert sol.checkString("bbb") is True
    assert sol.checkString("aaa") is True
    assert sol.checkString("a") is True
    assert sol.checkString("b") is True
    assert sol.checkString("ab") is True
    assert sol.checkString("ba") is False
    assert sol.checkString("aabbaa") is False
    print("All sample tests passed!")
