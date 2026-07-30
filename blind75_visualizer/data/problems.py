"""Problem data for the Blind 75 Visualizer.

Each entry in PROBLEMS is a plain dict:
  slug, number, title, category, difficulty, tags, summary,
  time, space, code, example, approach (list[str]),
  and optionally `steps` (list[dict]) for an animated visualization.

Step shape (only for animated problems):
  {
    "line": <int, source line to highlight>,
    "narration": "<html-safe string>",
    "rows": [{"label": "nums", "items": [{"v": 1, "state": "current"}]}],
    "map": {"label": "seen", "items": [{"v": "1", "added": True}]} | None,
  }
"""

CATEGORIES = [
    {"key": "arrays-hashing", "label": "Arrays & Hashing"},
    {"key": "two-pointers", "label": "Two Pointers"},
    {"key": "sliding-window", "label": "Sliding Window"},
    {"key": "stack", "label": "Stack"},
    {"key": "binary-search", "label": "Binary Search"},
    {"key": "linked-list", "label": "Linked List"},
    {"key": "trees", "label": "Trees"},
    {"key": "tries", "label": "Tries"},
    {"key": "heap", "label": "Heap / Priority Queue"},
    {"key": "backtracking", "label": "Backtracking"},
    {"key": "graphs", "label": "Graphs"},
    {"key": "dp-1d", "label": "1-D Dynamic Programming"},
    {"key": "intervals", "label": "Intervals"},
    {"key": "matrix", "label": "Matrix"},
    {"key": "bit-manipulation", "label": "Bit Manipulation"},
]

PROBLEMS = [
    # ---------------------------------------------------------------- Arrays & Hashing
    {
        "slug": "contains-duplicate",
        "number": 217,
        "title": "Contains Duplicate",
        "category": "arrays-hashing",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Set"],
        "summary": "Return true if any value appears at least twice in the array.",
        "time": "O(n)",
        "space": "O(n)",
        "example": "nums = [1, 2, 3, 1]  →  True",
        "approach": [
            "Walk the array once, keeping a set of numbers seen so far.",
            "Before adding the current number, check whether it's already in the set.",
            "If it is, a duplicate exists — return True immediately.",
            "If the loop finishes with no match, every number was unique.",
        ],
        "code": '''from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False''',
        "steps": [
            {"line": 5, "narration": "Start with an empty set to track numbers we've seen.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "pending"}, {"v": 2, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 1, "state": "pending"}]}],
             "map": {"label": "seen (set)", "items": []}},
            {"line": 7, "narration": "Check if <b>1</b> is in <code>seen</code> — the set is empty, so no.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "current"}, {"v": 2, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 1, "state": "pending"}]}],
             "map": {"label": "seen (set)", "items": []}},
            {"line": 9, "narration": "Not found — add <b>1</b> to <code>seen</code>.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 1, "state": "pending"}]}],
             "map": {"label": "seen (set)", "items": [{"v": 1, "added": True}]}},
            {"line": 7, "narration": "Check if <b>2</b> is in <code>seen</code> — not yet.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "current"}, {"v": 3, "state": "pending"}, {"v": 1, "state": "pending"}]}],
             "map": {"label": "seen (set)", "items": [{"v": 1, "added": False}]}},
            {"line": 9, "narration": "Not found — add <b>2</b> to <code>seen</code>.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 3, "state": "pending"}, {"v": 1, "state": "pending"}]}],
             "map": {"label": "seen (set)", "items": [{"v": 1, "added": False}, {"v": 2, "added": True}]}},
            {"line": 7, "narration": "Check if <b>3</b> is in <code>seen</code> — not yet.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 3, "state": "current"}, {"v": 1, "state": "pending"}]}],
             "map": {"label": "seen (set)", "items": [{"v": 1, "added": False}, {"v": 2, "added": False}]}},
            {"line": 9, "narration": "Not found — add <b>3</b> to <code>seen</code>.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 3, "state": "done"}, {"v": 1, "state": "pending"}]}],
             "map": {"label": "seen (set)", "items": [{"v": 1, "added": False}, {"v": 2, "added": False}, {"v": 3, "added": True}]}},
            {"line": 7, "narration": "Check if <b>1</b> is in <code>seen</code> — yes, added back at index 0!",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 3, "state": "done"}, {"v": 1, "state": "current"}]}],
             "map": {"label": "seen (set)", "items": [{"v": 1, "added": False}, {"v": 2, "added": False}, {"v": 3, "added": False}]}},
            {"line": 8, "narration": "<b>Duplicate found — return True.</b>",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "hit"}, {"v": 2, "state": "done"}, {"v": 3, "state": "done"}, {"v": 1, "state": "hit"}]}],
             "map": {"label": "seen (set)", "items": [{"v": 1, "added": False}, {"v": 2, "added": False}, {"v": 3, "added": False}]}},
        ],
    },
    {
        "slug": "valid-anagram",
        "number": 242,
        "title": "Valid Anagram",
        "category": "arrays-hashing",
        "difficulty": "Easy",
        "tags": ["String", "Hash Map"],
        "summary": "Determine if t is an anagram of s (same letters, same counts).",
        "time": "O(n)",
        "space": "O(1) — at most 26 letters",
        "example": 's = "anagram", t = "nagaram"  →  True',
        "approach": [
            "If the lengths differ, they can't be anagrams.",
            "Count every character in s into a frequency map.",
            "Walk t, decrementing the count for each character.",
            "If a character is missing or its count hits zero early, it's not an anagram.",
            "If every character in t cancels out a count from s, they match.",
        ],
        "code": '''class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        counts = {}
        for ch in s:
            counts[ch] = counts.get(ch, 0) + 1
        for ch in t:
            if ch not in counts or counts[ch] == 0:
                return False
            counts[ch] -= 1
        return True''',
        "steps": [
            {"line": 3, "narration": "Lengths match (7 = 7) — an anagram is still possible.",
             "rows": [{"label": "s", "items": [{"v": c, "state": "pending"} for c in "anagram"]}, {"label": "t", "items": [{"v": c, "state": "pending"} for c in "nagaram"]}],
             "map": {"label": "char counts", "items": []}},
            {"line": 7, "narration": "Count each character in <b>s</b>: a→3, n→1, g→1, r→1, m→1.",
             "rows": [{"label": "s", "items": [{"v": c, "state": "done"} for c in "anagram"]}, {"label": "t", "items": [{"v": c, "state": "pending"} for c in "nagaram"]}],
             "map": {"label": "char counts", "items": [{"v": "a:3", "added": True}, {"v": "n:1", "added": True}, {"v": "g:1", "added": True}, {"v": "r:1", "added": True}, {"v": "m:1", "added": True}]}},
            {"line": 9, "narration": "t[0]='n' is present with count 1 — ok so far.",
             "rows": [{"label": "s", "items": [{"v": c, "state": "done"} for c in "anagram"]}, {"label": "t", "items": [{"v": "n", "state": "current"}] + [{"v": c, "state": "pending"} for c in "agaram"]}],
             "map": {"label": "char counts", "items": [{"v": "a:3"}, {"v": "n:1"}, {"v": "g:1"}, {"v": "r:1"}, {"v": "m:1"}]}},
            {"line": 11, "narration": "Decrement n → 0.",
             "rows": [{"label": "s", "items": [{"v": c, "state": "done"} for c in "anagram"]}, {"label": "t", "items": [{"v": "n", "state": "done"}] + [{"v": c, "state": "pending"} for c in "agaram"]}],
             "map": {"label": "char counts", "items": [{"v": "a:3"}, {"v": "n:0"}, {"v": "g:1"}, {"v": "r:1"}, {"v": "m:1"}]}},
            {"line": 9, "narration": "Continue matching the rest of t the same way — a, g, a, r, a, m each found with count > 0, decrementing as we go.",
             "rows": [{"label": "s", "items": [{"v": c, "state": "done"} for c in "anagram"]}, {"label": "t", "items": [{"v": c, "state": "done"} for c in "nagaram"]}],
             "map": {"label": "char counts", "items": [{"v": "a:0"}, {"v": "n:0"}, {"v": "g:0"}, {"v": "r:0"}, {"v": "m:0"}]}},
            {"line": 12, "narration": "<b>Every count reached zero — return True.</b> t is an anagram of s.",
             "rows": [{"label": "s", "items": [{"v": c, "state": "done"} for c in "anagram"]}, {"label": "t", "items": [{"v": c, "state": "hit"} for c in "nagaram"]}],
             "map": {"label": "char counts", "items": [{"v": "a:0"}, {"v": "n:0"}, {"v": "g:0"}, {"v": "r:0"}, {"v": "m:0"}]}},
        ],
    },
    {
        "slug": "two-sum",
        "number": 1,
        "title": "Two Sum",
        "category": "arrays-hashing",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Map"],
        "summary": "Return indices of the two numbers that add up to target.",
        "time": "O(n)",
        "space": "O(n)",
        "example": "nums = [2, 7, 11, 15], target = 9  →  [0, 1]",
        "approach": [
            "Keep a map from value → index of numbers seen so far.",
            "For each number, compute the complement needed to reach target.",
            "If that complement is already in the map, you've found the pair.",
            "Otherwise record the current number's index and keep going.",
        ],
        "code": '''from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []''',
        "steps": [
            {"line": 5, "narration": "Start with an empty map from value → index.",
             "rows": [{"label": "nums", "items": [{"v": 2, "state": "pending"}, {"v": 7, "state": "pending"}, {"v": 11, "state": "pending"}, {"v": 15, "state": "pending"}]}],
             "map": {"label": "seen (value → index)", "items": []}},
            {"line": 7, "narration": "complement = target - 2 = 7.",
             "rows": [{"label": "nums", "items": [{"v": 2, "state": "current"}, {"v": 7, "state": "pending"}, {"v": 11, "state": "pending"}, {"v": 15, "state": "pending"}]}],
             "map": {"label": "seen (value → index)", "items": []}},
            {"line": 8, "narration": "7 is not in <code>seen</code> yet.",
             "rows": [{"label": "nums", "items": [{"v": 2, "state": "current"}, {"v": 7, "state": "pending"}, {"v": 11, "state": "pending"}, {"v": 15, "state": "pending"}]}],
             "map": {"label": "seen (value → index)", "items": []}},
            {"line": 10, "narration": "Store 2 → index 0.",
             "rows": [{"label": "nums", "items": [{"v": 2, "state": "done"}, {"v": 7, "state": "pending"}, {"v": 11, "state": "pending"}, {"v": 15, "state": "pending"}]}],
             "map": {"label": "seen (value → index)", "items": [{"v": "2→0", "added": True}]}},
            {"line": 7, "narration": "complement = target - 7 = 2.",
             "rows": [{"label": "nums", "items": [{"v": 2, "state": "done"}, {"v": 7, "state": "current"}, {"v": 11, "state": "pending"}, {"v": 15, "state": "pending"}]}],
             "map": {"label": "seen (value → index)", "items": [{"v": "2→0"}]}},
            {"line": 8, "narration": "2 is in <code>seen</code> at index 0 — match found.",
             "rows": [{"label": "nums", "items": [{"v": 2, "state": "hit"}, {"v": 7, "state": "current"}, {"v": 11, "state": "pending"}, {"v": 15, "state": "pending"}]}],
             "map": {"label": "seen (value → index)", "items": [{"v": "2→0"}]}},
            {"line": 9, "narration": "<b>Return [0, 1]</b> — nums[0] + nums[1] = 9.",
             "rows": [{"label": "nums", "items": [{"v": 2, "state": "hit"}, {"v": 7, "state": "hit"}, {"v": 11, "state": "pending"}, {"v": 15, "state": "pending"}]}],
             "map": {"label": "seen (value → index)", "items": [{"v": "2→0"}]}},
        ],
    },
    {
        "slug": "group-anagrams",
        "number": 49,
        "title": "Group Anagrams",
        "category": "arrays-hashing",
        "difficulty": "Medium",
        "tags": ["Array", "Hash Map", "String"],
        "summary": "Group strings that are anagrams of each other.",
        "time": "O(n · k log k) — n strings, average length k",
        "space": "O(n · k)",
        "example": 'strs = ["eat","tea","tan","ate","nat","bat"]',
        "approach": [
            "Anagrams share the same letters, so sorting a word's letters gives a canonical key.",
            "Use a map from that sorted-letters key to the list of original words sharing it.",
            "For each word, compute its key and append it to that key's group.",
            "Return all the groups (the map's values).",
        ],
        "code": '''from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            key = "".join(sorted(s))
            groups[key].append(s)
        return list(groups.values())''',
        "steps": [
            {"line": 6, "narration": "Start with an empty map from sorted-letters key → list of words.",
             "rows": [{"label": "strs", "items": [{"v": w, "state": "pending"} for w in ["eat", "tea", "tan", "ate", "nat", "bat"]]}],
             "map": {"label": "groups (key → words)", "items": []}},
            {"line": 8, "narration": "'eat' sorted → 'aet'.",
             "rows": [{"label": "strs", "items": [{"v": "eat", "state": "current"}, {"v": "tea", "state": "pending"}, {"v": "tan", "state": "pending"}, {"v": "ate", "state": "pending"}, {"v": "nat", "state": "pending"}, {"v": "bat", "state": "pending"}]}],
             "map": {"label": "groups (key → words)", "items": []}},
            {"line": 9, "narration": "Add 'eat' under key 'aet'.",
             "rows": [{"label": "strs", "items": [{"v": "eat", "state": "done"}, {"v": "tea", "state": "pending"}, {"v": "tan", "state": "pending"}, {"v": "ate", "state": "pending"}, {"v": "nat", "state": "pending"}, {"v": "bat", "state": "pending"}]}],
             "map": {"label": "groups (key → words)", "items": [{"v": "aet: [eat]", "added": True}]}},
            {"line": 8, "narration": "'tea' sorted → 'aet' too — same key as 'eat'.",
             "rows": [{"label": "strs", "items": [{"v": "eat", "state": "done"}, {"v": "tea", "state": "current"}, {"v": "tan", "state": "pending"}, {"v": "ate", "state": "pending"}, {"v": "nat", "state": "pending"}, {"v": "bat", "state": "pending"}]}],
             "map": {"label": "groups (key → words)", "items": [{"v": "aet: [eat]"}]}},
            {"line": 9, "narration": "Append 'tea' to the 'aet' group.",
             "rows": [{"label": "strs", "items": [{"v": "eat", "state": "done"}, {"v": "tea", "state": "done"}, {"v": "tan", "state": "pending"}, {"v": "ate", "state": "pending"}, {"v": "nat", "state": "pending"}, {"v": "bat", "state": "pending"}]}],
             "map": {"label": "groups (key → words)", "items": [{"v": "aet: [eat, tea]", "added": True}]}},
            {"line": 8, "narration": "'tan' sorted → 'ant' — a brand new key.",
             "rows": [{"label": "strs", "items": [{"v": "eat", "state": "done"}, {"v": "tea", "state": "done"}, {"v": "tan", "state": "current"}, {"v": "ate", "state": "pending"}, {"v": "nat", "state": "pending"}, {"v": "bat", "state": "pending"}]}],
             "map": {"label": "groups (key → words)", "items": [{"v": "aet: [eat, tea]"}]}},
            {"line": 9, "narration": "Continue the same way: 'ate'→aet (joins eat/tea), 'nat'→ant (joins tan), 'bat'→abt (new group).",
             "rows": [{"label": "strs", "items": [{"v": w, "state": "done"} for w in ["eat", "tea", "tan", "ate", "nat", "bat"]]}],
             "map": {"label": "groups (key → words)", "items": [{"v": "aet: [eat, tea, ate]", "added": True}, {"v": "ant: [tan, nat]", "added": True}, {"v": "abt: [bat]", "added": True}]}},
            {"line": 10, "narration": "<b>Return the grouped lists</b> — each group is a full set of anagrams.",
             "rows": [{"label": "strs", "items": [{"v": w, "state": "hit"} for w in ["eat", "tea", "tan", "ate", "nat", "bat"]]}],
             "map": {"label": "groups (key → words)", "items": [{"v": "aet: [eat, tea, ate]"}, {"v": "ant: [tan, nat]"}, {"v": "abt: [bat]"}]}},
        ],
    },
    {
        "slug": "top-k-frequent-elements",
        "number": 347,
        "title": "Top K Frequent Elements",
        "category": "arrays-hashing",
        "difficulty": "Medium",
        "tags": ["Array", "Hash Map", "Bucket Sort", "Heap"],
        "summary": "Return the k most frequent elements in the array.",
        "time": "O(n) — bucket sort avoids an O(n log n) sort",
        "space": "O(n)",
        "example": "nums = [1,1,1,2,2,3], k = 2  →  [1, 2]",
        "approach": [
            "Count how often each number appears with a hash map.",
            "Bucket numbers by frequency: bucket[f] holds every number that appears f times.",
            "A number can appear at most n times, so there are only n+1 possible buckets.",
            "Walk the buckets from highest frequency to lowest, collecting numbers until we have k.",
        ],
        "code": '''from typing import List
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            buckets[freq].append(num)

        result = []
        for freq in range(len(buckets) - 1, 0, -1):
            for num in buckets[freq]:
                result.append(num)
                if len(result) == k:
                    return result
        return result''',
        "steps": [
            {"line": 6, "narration": "Count frequency of each number: 1→3, 2→2, 3→1.",
             "rows": [{"label": "nums", "items": [{"v": v, "state": "pending"} for v in [1, 1, 1, 2, 2, 3]]}],
             "map": {"label": "count", "items": [{"v": "1:3", "added": True}, {"v": "2:2", "added": True}, {"v": "3:1", "added": True}]}},
            {"line": 9, "narration": "Bucket numbers by frequency (bucket index = frequency): bucket[3]=[1], bucket[2]=[2], bucket[1]=[3].",
             "rows": [{"label": "nums", "items": [{"v": v, "state": "done"} for v in [1, 1, 1, 2, 2, 3]]}],
             "map": {"label": "buckets (freq → nums)", "items": [{"v": "3 → [1]", "added": True}, {"v": "2 → [2]", "added": True}, {"v": "1 → [3]", "added": True}]}},
            {"line": 13, "narration": "Walk buckets from highest frequency down. freq=3: take 1.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "current"}, {"v": 1, "state": "done"}, {"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 2, "state": "done"}, {"v": 3, "state": "done"}]}],
             "map": {"label": "buckets (freq → nums)", "items": [{"v": "3 → [1]"}, {"v": "2 → [2]"}, {"v": "1 → [3]"}]}},
            {"line": 14, "narration": "Add 1 to result → [1]. Not yet k=2 items.",
             "rows": [{"label": "result", "items": [{"v": 1, "state": "done"}]}],
             "map": {"label": "buckets (freq → nums)", "items": [{"v": "3 → [1]"}, {"v": "2 → [2]"}, {"v": "1 → [3]"}]}},
            {"line": 13, "narration": "freq=2: take 2.",
             "rows": [{"label": "result", "items": [{"v": 1, "state": "done"}]}],
             "map": {"label": "buckets (freq → nums)", "items": [{"v": "3 → [1]"}, {"v": "2 → [2]"}, {"v": "1 → [3]"}]}},
            {"line": 14, "narration": "Add 2 to result → [1, 2].",
             "rows": [{"label": "result", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "done"}]}],
             "map": {"label": "buckets (freq → nums)", "items": [{"v": "3 → [1]"}, {"v": "2 → [2]"}, {"v": "1 → [3]"}]}},
            {"line": 16, "narration": "<b>len(result) == k — return [1, 2].</b> Reached the 2 most frequent elements.",
             "rows": [{"label": "result", "items": [{"v": 1, "state": "hit"}, {"v": 2, "state": "hit"}]}],
             "map": {"label": "buckets (freq → nums)", "items": [{"v": "3 → [1]"}, {"v": "2 → [2]"}, {"v": "1 → [3]"}]}},
        ],
    },
    {
        "slug": "product-of-array-except-self",
        "number": 238,
        "title": "Product of Array Except Self",
        "category": "arrays-hashing",
        "difficulty": "Medium",
        "tags": ["Array", "Prefix Sum"],
        "summary": "Return an array where each element is the product of all others (no division).",
        "time": "O(n)",
        "space": "O(1) extra — output array doesn't count",
        "example": "nums = [1, 2, 3, 4]  →  [24, 12, 8, 6]",
        "approach": [
            "result[i] should be the product of everything to the left of i, times everything to the right.",
            "First pass (left to right): fill result[i] with the running product of everything before i (prefix).",
            "Second pass (right to left): multiply result[i] by the running product of everything after i (postfix).",
            "No division needed, and only the output array uses extra space.",
        ],
        "code": '''from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n

        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]

        postfix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= postfix
            postfix *= nums[i]

        return result''',
        "steps": [
            {"line": 6, "narration": "Initialize result with all 1s.",
             "rows": [{"label": "nums", "items": [{"v": v, "state": "pending"} for v in [1, 2, 3, 4]]}, {"label": "result", "items": [{"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}]}],
             "map": None},
            {"line": 10, "narration": "result[0] = prefix (1); then prefix *= nums[0] → 1.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "current"}, {"v": 2, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 4, "state": "pending"}]}, {"label": "result", "items": [{"v": 1, "state": "done"}, {"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}]}],
             "map": None},
            {"line": 10, "narration": "result[1] = prefix (1); prefix *= nums[1] → 2.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "current"}, {"v": 3, "state": "pending"}, {"v": 4, "state": "pending"}]}, {"label": "result", "items": [{"v": 1, "state": "done"}, {"v": 1, "state": "done"}, {"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}]}],
             "map": None},
            {"line": 10, "narration": "result[2] = prefix (2); prefix *= nums[2] → 6.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 3, "state": "current"}, {"v": 4, "state": "pending"}]}, {"label": "result", "items": [{"v": 1, "state": "done"}, {"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 1, "state": "pending"}]}],
             "map": None},
            {"line": 10, "narration": "result[3] = prefix (6); prefix *= nums[3] → 24. Left pass done: result = [1, 1, 2, 6].",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 3, "state": "done"}, {"v": 4, "state": "current"}]}, {"label": "result", "items": [{"v": 1, "state": "done"}, {"v": 1, "state": "done"}, {"v": 2, "state": "done"}, {"v": 6, "state": "done"}]}],
             "map": None},
            {"line": 15, "narration": "Now sweep from the right, tracking the running product of everything to the right (postfix, starts at 1).",
             "rows": [{"label": "nums", "items": [{"v": v, "state": "pending"} for v in [1, 2, 3, 4]]}, {"label": "result", "items": [{"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 2, "state": "pending"}, {"v": 6, "state": "pending"}]}],
             "map": None},
            {"line": 15, "narration": "result[3] = 6 × postfix(1) = 6; postfix *= nums[3] → 4.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "pending"}, {"v": 2, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 4, "state": "current"}]}, {"label": "result", "items": [{"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 2, "state": "pending"}, {"v": 6, "state": "done"}]}],
             "map": None},
            {"line": 15, "narration": "result[2] = 2 × postfix(4) = 8; postfix *= nums[2] → 12.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "pending"}, {"v": 2, "state": "pending"}, {"v": 3, "state": "current"}, {"v": 4, "state": "done"}]}, {"label": "result", "items": [{"v": 1, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 8, "state": "done"}, {"v": 6, "state": "done"}]}],
             "map": None},
            {"line": 15, "narration": "result[1] = 1 × postfix(12) = 12; postfix *= nums[1] → 24.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "pending"}, {"v": 2, "state": "current"}, {"v": 3, "state": "done"}, {"v": 4, "state": "done"}]}, {"label": "result", "items": [{"v": 1, "state": "pending"}, {"v": 12, "state": "done"}, {"v": 8, "state": "done"}, {"v": 6, "state": "done"}]}],
             "map": None},
            {"line": 18, "narration": "<b>result[0] = 1 × postfix(24) = 24.</b> Final: [24, 12, 8, 6] — no division used.",
             "rows": [{"label": "nums", "items": [{"v": 1, "state": "hit"}, {"v": 2, "state": "done"}, {"v": 3, "state": "done"}, {"v": 4, "state": "done"}]}, {"label": "result", "items": [{"v": 24, "state": "hit"}, {"v": 12, "state": "hit"}, {"v": 8, "state": "hit"}, {"v": 6, "state": "hit"}]}],
             "map": None},
        ],
    },
    {
        "slug": "valid-sudoku",
        "number": 36,
        "title": "Valid Sudoku",
        "category": "arrays-hashing",
        "difficulty": "Medium",
        "tags": ["Array", "Hash Set", "Matrix"],
        "summary": "Check whether a partially filled 9x9 Sudoku board is valid so far.",
        "time": "O(1) — board is fixed at 81 cells",
        "space": "O(1) — 27 sets of at most 9 digits",
        "example": 'board[i][j] is a digit "1"-"9" or "."',
        "approach": [
            "Keep one set per row, per column, and per 3×3 box (9 of each) to track digits already placed.",
            "Scan every cell of the 9x9 board; skip empty cells (\".\").",
            "Compute which box a cell belongs to with (r // 3) * 3 + c // 3.",
            "If the digit is already in that row's, column's, or box's set, the board is invalid — return False.",
            "Otherwise record the digit in all three sets and continue; no conflicts after a full scan means it's valid.",
        ],
        "code": '''from typing import List

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == ".":
                    continue
                b = (r // 3) * 3 + c // 3
                if val in rows[r] or val in cols[c] or val in boxes[b]:
                    return False
                rows[r].add(val)
                cols[c].add(val)
                boxes[b].add(val)
        return True''',
    },
    {
        "slug": "longest-consecutive-sequence",
        "number": 128,
        "title": "Longest Consecutive Sequence",
        "category": "arrays-hashing",
        "difficulty": "Medium",
        "tags": ["Array", "Hash Set"],
        "summary": "Find the length of the longest run of consecutive integers, in O(n).",
        "time": "O(n)",
        "space": "O(n)",
        "example": "nums = [100, 4, 200, 1, 3, 2]  →  4  (the run 1, 2, 3, 4)",
        "approach": [
            "Put every number in a set for O(1) membership checks.",
            "A number only starts a sequence if num - 1 is NOT in the set.",
            "For each sequence start, count forward (num+1, num+2, ...) while values are in the set.",
            "Track the longest streak found; every number is only ever counted as the start of its own run, so the whole scan is O(n).",
        ],
        "code": '''from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0

        for num in num_set:
            if num - 1 not in num_set:
                length = 1
                while num + length in num_set:
                    length += 1
                longest = max(longest, length)

        return longest''',
        "steps": [
            {"line": 4, "narration": "Put every number in a set for O(1) lookups.",
             "rows": [{"label": "nums", "items": [{"v": v, "state": "pending"} for v in [100, 4, 200, 1, 3, 2]]}],
             "map": {"label": "num_set", "items": [{"v": 100, "added": True}, {"v": 4, "added": True}, {"v": 200, "added": True}, {"v": 1, "added": True}, {"v": 3, "added": True}, {"v": 2, "added": True}]}},
            {"line": 8, "narration": "100: is 99 in the set? No — 100 could start a streak.",
             "rows": [{"label": "nums", "items": [{"v": 100, "state": "current"}, {"v": 4, "state": "pending"}, {"v": 200, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 2, "state": "pending"}]}],
             "map": {"label": "num_set", "items": [{"v": 100}, {"v": 4}, {"v": 200}, {"v": 1}, {"v": 3}, {"v": 2}]}},
            {"line": 10, "narration": "Count forward from 100: 101 is not in the set, so this streak has length 1. Best so far: 1.",
             "rows": [{"label": "nums", "items": [{"v": 100, "state": "done"}, {"v": 4, "state": "pending"}, {"v": 200, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 2, "state": "pending"}]}],
             "map": {"label": "num_set", "items": [{"v": 100}, {"v": 4}, {"v": 200}, {"v": 1}, {"v": 3}, {"v": 2}]}},
            {"line": 8, "narration": "4: is 3 in the set? Yes — so 4 is NOT a streak start; skip it.",
             "rows": [{"label": "nums", "items": [{"v": 100, "state": "done"}, {"v": 4, "state": "current"}, {"v": 200, "state": "pending"}, {"v": 1, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 2, "state": "pending"}]}],
             "map": {"label": "num_set", "items": [{"v": 100}, {"v": 4}, {"v": 200}, {"v": 1}, {"v": 3}, {"v": 2}]}},
            {"line": 8, "narration": "200: is 199 in the set? No — 200 could start a streak. Counting forward finds length 1 (best stays 1).",
             "rows": [{"label": "nums", "items": [{"v": 100, "state": "done"}, {"v": 4, "state": "done"}, {"v": 200, "state": "current"}, {"v": 1, "state": "pending"}, {"v": 3, "state": "pending"}, {"v": 2, "state": "pending"}]}],
             "map": {"label": "num_set", "items": [{"v": 100}, {"v": 4}, {"v": 200}, {"v": 1}, {"v": 3}, {"v": 2}]}},
            {"line": 8, "narration": "1: is 0 in the set? No — 1 could start a streak.",
             "rows": [{"label": "nums", "items": [{"v": 100, "state": "done"}, {"v": 4, "state": "done"}, {"v": 200, "state": "done"}, {"v": 1, "state": "current"}, {"v": 3, "state": "pending"}, {"v": 2, "state": "pending"}]}],
             "map": {"label": "num_set", "items": [{"v": 100}, {"v": 4}, {"v": 200}, {"v": 1}, {"v": 3}, {"v": 2}]}},
            {"line": 10, "narration": "Count forward from 1: 2, 3, 4 are all in the set, 5 is not → streak length 4.",
             "rows": [{"label": "nums", "items": [{"v": 100, "state": "done"}, {"v": 4, "state": "hit"}, {"v": 200, "state": "done"}, {"v": 1, "state": "hit"}, {"v": 3, "state": "hit"}, {"v": 2, "state": "hit"}]}],
             "map": {"label": "num_set", "items": [{"v": 100}, {"v": 4}, {"v": 200}, {"v": 1}, {"v": 3}, {"v": 2}]}},
            {"line": 11, "narration": "New best streak: 4 (1 → 2 → 3 → 4). The remaining numbers (3, 2) fail the 'num - 1 not in set' check and are skipped.",
             "rows": [{"label": "nums", "items": [{"v": 100, "state": "done"}, {"v": 4, "state": "hit"}, {"v": 200, "state": "done"}, {"v": 1, "state": "hit"}, {"v": 3, "state": "hit"}, {"v": 2, "state": "hit"}]}],
             "map": {"label": "num_set", "items": [{"v": 100}, {"v": 4}, {"v": 200}, {"v": 1}, {"v": 3}, {"v": 2}]}},
            {"line": 13, "narration": "<b>Return 4</b> — the longest run is 1 → 2 → 3 → 4.",
             "rows": [{"label": "nums", "items": [{"v": 100, "state": "done"}, {"v": 4, "state": "hit"}, {"v": 200, "state": "done"}, {"v": 1, "state": "hit"}, {"v": 3, "state": "hit"}, {"v": 2, "state": "hit"}]}],
             "map": {"label": "num_set", "items": [{"v": 100}, {"v": 4}, {"v": 200}, {"v": 1}, {"v": 3}, {"v": 2}]}},
        ],
    },
]
