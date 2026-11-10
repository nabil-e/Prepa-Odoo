import timeit

# 1. Two Sum
def two_sum(nums: list[int], target: int):
    for i, j in enumerate(nums):
        for k, l in enumerate(nums):
            if j + l == target and i != k:
                return [i, k]

def two_sum_oneliner(nums, target):
    return next((i, k) for i, j in enumerate(nums) for k, l in enumerate(nums[i+1:], i+1) if j + l == target)

def two_sum_dict(nums: list[int], target: int):
    vus = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in vus:
            return [vus[diff], i]
        vus[num] = i

nums_test = list(range(1000))
target_test = 998 + 999  # Les deux derniers éléments

# Mesure des temps
t_two_sum = timeit.timeit(lambda: two_sum(nums_test, target_test), number=10)
t_oneliner = timeit.timeit(lambda: two_sum_oneliner(nums_test, target_test), number=10)
t_dict = timeit.timeit(lambda: two_sum_dict(nums_test, target_test), number=10)

# print(f"two_sum (O(n²)) : {t_two_sum:.6f} secondes")
# print(f"One-Liner (O(n²)) : {t_oneliner:.6f} secondes")
# print(f"Dictionnaire (O(n)) : {t_dict:.6f} secondes")
# print(f"Facteur : {t_two_sum / t_oneliner:.1f}x plus rapide")
# print(f"Facteur : {t_oneliner / t_dict:.1f}x plus rapide")
# print(f"Facteur : {t_two_sum / t_dict:.1f}x plus rapide")

# 14. Longest Common Prefix
def longestCommonPrefix(strs: list[str]):
    res = ""
    for c in zip(*strs):
        if len(set(c)) == 1:
            res += c[0]
        else:
            break
    return res
    # return "".join([(c[0]) for c in zip(*strs) if len(set(c)) == 1])

# 88. Merge Sorted Array
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """
    Do not return anything, modify nums1 in-place instead.
    """
    r1 = m - 1
    r2 = n - 1
    w = m + n - 1
    while r2 >= 0:
        if r1 >= 0 and nums1[r1] > nums2[r2]:
            nums1[w] = nums1[r1]
            r1 -= 1
        else:
            nums1[w] = nums2[r2]
            r2 -= 1
        w -= 1

# 125. Valid Palindrome
def isPalindrome(s: str):
    s = [x.lower() for x in s if x.isalnum()]
    return s == s[::-1]

# 217. Contains Duplicate
def containsDuplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))

# 242. Valid Anagram
def isAnagram(self, s: str, t: str) -> bool:
    return sorted(s) == sorted(t)

