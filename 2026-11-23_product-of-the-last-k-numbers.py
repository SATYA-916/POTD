# LeetCode Problem of the Day — 2026-11-23
# Title: Product of the Last K Numbers
# Difficulty: Medium
# Topics: Array, Math, Design, Data Stream, Prefix Sum
# Link: https://leetcode.com/problems/product-of-the-last-k-numbers/
#
# Problem statement:
# Design an algorithm that accepts a stream of integers and retrieves the
# product of the last k integers of the stream.
#
# Implement the ProductOfNumbers class:
#   ProductOfNumbers() initializes the object with an empty stream.
#   void add(int num) appends the integer num to the stream.
#   int getProduct(int k) returns the product of the last k numbers in the
#   current list. You can assume the current list always has at least
#   k numbers.
#
# The test cases are generated so that, at any time, the product of any
# contiguous sequence of numbers fits into a single 32-bit integer.
#
# Example:
#   Input:  ["ProductOfNumbers","add","add","add","add","add",
#             "getProduct","getProduct","getProduct","add","getProduct"]
#           [[],[3],[0],[2],[5],[4],[2],[3],[4],[8],[2]]
#   Output: [null,null,null,null,null,null,20,40,0,null,32]
#   Explanation:
#     add(3); add(0); add(2); add(5); add(4);
#     getProduct(2) = 5 * 4 = 20
#     getProduct(3) = 2 * 5 * 4 = 40
#     getProduct(4) = 0 * 2 * 5 * 4 = 0
#     add(8); getProduct(2) = 4 * 8 = 32
#
# Constraints:
#   0 <= num <= 100
#   1 <= k <= 4 * 10^4
#   At most 4 * 10^4 calls will be made to add and getProduct.
#   The product of the stream at any point will fit in a 32-bit integer.
#
# Approach:
# Keep a prefix-products list starting with 1. On add(num), append
# prefix[-1] * num. A zero resets the list back to [1], because any product
# spanning a zero is zero; the length of the list then tells us whether the
# last k numbers contain a zero. getProduct(k) returns 0 when k >=
# len(prefix) (a zero lies within the last k numbers), otherwise it is
# prefix[-1] // prefix[-1 - k], the ratio of two prefix products.
#
# Time complexity: O(1) per add and per getProduct.
# Space complexity: O(n) for the prefix products, n = number of adds
# since the most recent zero (at most the total number of adds).


class ProductOfNumbers:
    def __init__(self):
        # prefix[i] = product of the first i numbers added since the
        # most recent zero; prefix[0] = 1 (empty product).
        self.prefix = [1]

    def add(self, num: int) -> None:
        if num == 0:
            # Any product spanning this zero is 0; restart the list.
            self.prefix = [1]
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):
            # The last k numbers include a zero.
            return 0
        return self.prefix[-1] // self.prefix[-1 - k]


if __name__ == "__main__":
    # LeetCode example.
    obj = ProductOfNumbers()
    obj.add(3)
    obj.add(0)
    obj.add(2)
    obj.add(5)
    obj.add(4)
    assert obj.getProduct(2) == 20
    assert obj.getProduct(3) == 40
    assert obj.getProduct(4) == 0
    obj.add(8)
    assert obj.getProduct(2) == 32

    # No zero in the stream at all.
    obj = ProductOfNumbers()
    for n in (2, 3, 4):
        obj.add(n)
    assert obj.getProduct(1) == 4
    assert obj.getProduct(3) == 24

    # Zero as the very first add, then a fresh stream.
    obj = ProductOfNumbers()
    obj.add(0)
    obj.add(7)
    assert obj.getProduct(1) == 7

    # Zero in the middle: products spanning it are 0, later ones are not.
    obj = ProductOfNumbers()
    obj.add(5)
    obj.add(0)
    obj.add(2)
    obj.add(3)
    assert obj.getProduct(3) == 0
    assert obj.getProduct(2) == 6
    assert obj.getProduct(1) == 3

    # Single element stream and a run of ones.
    obj = ProductOfNumbers()
    obj.add(9)
    assert obj.getProduct(1) == 9
    obj = ProductOfNumbers()
    for _ in range(5):
        obj.add(1)
    assert obj.getProduct(5) == 1

    print("All self-tests passed.")
