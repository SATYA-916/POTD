"""
LeetCode Problem of the Day — 2026-11-05
Title: Find the Distance Value Between Two Arrays
Difficulty: Easy
Topics: Array, Two Pointers, Binary Search, Sorting
Link: https://leetcode.com/problems/find-the-distance-value-between-two-arrays/

Problem statement:
    Given two integer arrays arr1 and arr2, and the integer d, return the
    distance value between the two arrays. The distance value is defined
    as the number of elements arr1[i] such that there is not any element
    arr2[j] where |arr1[i] - arr2[j]| <= d.

Examples:
    Example 1:
        Input: arr1 = [4, 5, 8], arr2 = [10, 9, 1, 8], d = 2
        Output: 2
        Explanation: 4 and 5 have no element of arr2 within distance 2;
        8 does (|8 - 10| = 2, |8 - 9| = 1, |8 - 8| = 0).
    Example 2:
        Input: arr1 = [1, 4, 2, 3], arr2 = [-4, -3, 6, 10, 20, 30], d = 3
        Output: 2
    Example 3:
        Input: arr1 = [2, 1, 100, 3], arr2 = [-5, -2, 10, -3, 7], d = 6
        Output: 1

Constraints:
    1 <= arr1.length, arr2.length <= 500
    -1000 <= arr1[i], arr2[j] <= 1000
    0 <= d <= 100

Approach:
    Sort arr2 once. For each value x in arr1, binary-search the insertion
    point of x in the sorted arr2; only the neighbours around that point
    can be the closest values to x, so x counts toward the distance value
    exactly when neither neighbour lies within distance d of x.
    Time complexity: O(n log n + m log n), where n = len(arr2),
    m = len(arr1) (sorting dominates).
    Space complexity: O(n) for the sorted copy of arr2 (O(1) extra if
    sorting in place is acceptable).
"""

from bisect import bisect_left
from typing import List


class Solution:
    def findTheDistanceValue(self, arr1: List[int], arr2: List[int], d: int) -> int:
        arr2 = sorted(arr2)
        count = 0
        for x in arr1:
            i = bisect_left(arr2, x)
            # Neighbour at or above x.
            if i < len(arr2) and arr2[i] - x <= d:
                continue
            # Neighbour just below x.
            if i > 0 and x - arr2[i - 1] <= d:
                continue
            count += 1
        return count


if __name__ == "__main__":
    sol = Solution()
    assert sol.findTheDistanceValue([4, 5, 8], [10, 9, 1, 8], 2) == 2
    assert sol.findTheDistanceValue([1, 4, 2, 3], [-4, -3, 6, 10, 20, 30], 3) == 2
    assert sol.findTheDistanceValue([2, 1, 100, 3], [-5, -2, 10, -3, 7], 6) == 1
    # Edge cases: exact match with d = 0, and an empty-ish gap.
    assert sol.findTheDistanceValue([1], [1], 0) == 0
    assert sol.findTheDistanceValue([1], [2], 0) == 1
    print("All self-tests passed.")
