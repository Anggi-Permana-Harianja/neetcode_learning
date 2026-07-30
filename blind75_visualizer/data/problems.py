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
        "inputs": [{"name": "nums", "label": "nums", "type": "int-array", "default": "1, 2, 3, 1", "maxLen": 30}],
        "js": '''function generateSteps(nums) {
  var steps = [];
  var seen = [];
  var seenSet = {};

  steps.push({
    line: 5,
    narration: "Start with an empty set to track numbers we've seen.",
    rows: [{ label: "nums", items: nums.map(function (v) { return { v: v, state: "pending" }; }) }],
    map: { label: "seen (set)", items: [] }
  });

  for (var i = 0; i < nums.length; i++) {
    var num = nums[i];
    var found = Object.prototype.hasOwnProperty.call(seenSet, num);

    steps.push({
      line: 7,
      narration: "Check if <b>" + num + "</b> is in <code>seen</code> — " + (found ? "yes!" : "no."),
      rows: [{ label: "nums", items: nums.map(function (v, idx) {
        return { v: v, state: idx < i ? "done" : idx === i ? "current" : "pending" };
      }) }],
      map: { label: "seen (set)", items: seen.map(function (v) { return { v: v }; }) }
    });

    if (found) {
      var firstIdx = nums.indexOf(num);
      steps.push({
        line: 8,
        narration: "<b>Duplicate found — return True.</b>",
        rows: [{ label: "nums", items: nums.map(function (v, idx) {
          return { v: v, state: (idx === i || idx === firstIdx) ? "hit" : (idx < i ? "done" : "pending") };
        }) }],
        map: { label: "seen (set)", items: seen.map(function (v) { return { v: v }; }) }
      });
      return steps;
    }

    seenSet[num] = true;
    seen.push(num);
    steps.push({
      line: 9,
      narration: "Not found — add <b>" + num + "</b> to <code>seen</code>.",
      rows: [{ label: "nums", items: nums.map(function (v, idx) {
        return { v: v, state: idx <= i ? "done" : "pending" };
      }) }],
      map: { label: "seen (set)", items: seen.map(function (v, idx) { return { v: v, added: idx === seen.length - 1 }; }) }
    });
  }

  steps.push({
    line: 10,
    narration: "<b>No duplicates found — return False.</b>",
    rows: [{ label: "nums", items: nums.map(function (v) { return { v: v, state: "done" }; }) }],
    map: { label: "seen (set)", items: seen.map(function (v) { return { v: v }; }) }
  });
  return steps;
}''',
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
        "inputs": [
            {"name": "s", "label": "s", "type": "string", "default": "anagram", "maxLen": 24},
            {"name": "t", "label": "t", "type": "string", "default": "nagaram", "maxLen": 24},
        ],
        "js": '''function generateSteps(s, t) {
  var steps = [];
  var sArr = s.split("");
  var tArr = t.split("");

  function sItems(doneUpTo) {
    return sArr.map(function (c, idx) { return { v: c, state: idx < doneUpTo ? "done" : "pending" }; });
  }
  function tItemsPending() {
    return tArr.map(function (c) { return { v: c, state: "pending" }; });
  }

  steps.push({
    line: 3,
    narration: "Lengths: s has " + sArr.length + ", t has " + tArr.length + ". " +
      (sArr.length === tArr.length ? "They match — continue." : "They differ — cannot be anagrams."),
    rows: [{ label: "s", items: sItems(0) }, { label: "t", items: tItemsPending() }],
    map: { label: "char counts", items: [] }
  });

  if (sArr.length !== tArr.length) {
    steps.push({
      line: 4,
      narration: "<b>Lengths differ — return False.</b>",
      rows: [{ label: "s", items: sItems(0) }, { label: "t", items: tItemsPending() }],
      map: { label: "char counts", items: [] }
    });
    return steps;
  }

  var counts = {};
  function countItems(highlightCh) {
    return Object.keys(counts).map(function (k) {
      return { v: k + ":" + counts[k], added: k === highlightCh };
    });
  }

  for (var i = 0; i < sArr.length; i++) {
    var ch = sArr[i];
    counts[ch] = (counts[ch] || 0) + 1;
    steps.push({
      line: 7,
      narration: "s[" + i + "]='" + ch + "' → count " + ch + ":" + counts[ch] + ".",
      rows: [{ label: "s", items: sItems(i + 1) }, { label: "t", items: tItemsPending() }],
      map: { label: "char counts", items: countItems(ch) }
    });
  }

  var sDone = sItems(sArr.length);

  for (var j = 0; j < tArr.length; j++) {
    var tch = tArr[j];
    var tCur = tArr.map(function (c, idx) {
      return { v: c, state: idx < j ? "done" : idx === j ? "current" : "pending" };
    });
    var present = counts[tch] > 0;
    steps.push({
      line: 9,
      narration: "t[" + j + "]='" + tch + "': " + (present ? ("present with count " + counts[tch] + " — ok.") : "missing or count already 0 — not an anagram."),
      rows: [{ label: "s", items: sDone }, { label: "t", items: tCur }],
      map: { label: "char counts", items: countItems(null) }
    });
    if (!present) {
      steps.push({
        line: 10,
        narration: "<b>Return False.</b>",
        rows: [{ label: "s", items: sDone }, { label: "t", items: tCur }],
        map: { label: "char counts", items: countItems(null) }
      });
      return steps;
    }
    counts[tch] -= 1;
    var tDoneSoFar = tArr.map(function (c, idx) {
      return { v: c, state: idx <= j ? "done" : "pending" };
    });
    steps.push({
      line: 11,
      narration: "Decrement " + tch + " → " + counts[tch] + ".",
      rows: [{ label: "s", items: sDone }, { label: "t", items: tDoneSoFar }],
      map: { label: "char counts", items: countItems(tch) }
    });
  }

  steps.push({
    line: 12,
    narration: "<b>All counts reached zero — return True.</b>",
    rows: [{ label: "s", items: sDone }, { label: "t", items: tArr.map(function (c) { return { v: c, state: "hit" }; }) }],
    map: { label: "char counts", items: countItems(null) }
  });
  return steps;
}''',
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
        "inputs": [
            {"name": "nums", "label": "nums", "type": "int-array", "default": "2, 7, 11, 15", "maxLen": 30},
            {"name": "target", "label": "target", "type": "int", "default": "9"},
        ],
        "js": '''function generateSteps(nums, target) {
  var steps = [];
  var seenMap = {};
  var order = [];

  steps.push({
    line: 5,
    narration: "Start with an empty map from value → index.",
    rows: [{ label: "nums", items: nums.map(function (v) { return { v: v, state: "pending" }; }) }],
    map: { label: "seen (value → index)", items: [] }
  });

  for (var i = 0; i < nums.length; i++) {
    var num = nums[i];
    var complement = target - num;

    steps.push({
      line: 7,
      narration: "complement = target - " + num + " = " + complement + ".",
      rows: [{ label: "nums", items: nums.map(function (v, idx) {
        return { v: v, state: idx < i ? "done" : idx === i ? "current" : "pending" };
      }) }],
      map: { label: "seen (value → index)", items: order.map(function (v) { return { v: v + "→" + seenMap[v] }; }) }
    });

    if (Object.prototype.hasOwnProperty.call(seenMap, complement)) {
      var j = seenMap[complement];
      steps.push({
        line: 8,
        narration: complement + " is in <code>seen</code> at index " + j + " — match found.",
        rows: [{ label: "nums", items: nums.map(function (v, idx) {
          return { v: v, state: (idx === i || idx === j) ? "hit" : (idx < i ? "done" : "pending") };
        }) }],
        map: { label: "seen (value → index)", items: order.map(function (v) { return { v: v + "→" + seenMap[v] }; }) }
      });
      steps.push({
        line: 9,
        narration: "<b>Return [" + j + ", " + i + "]</b> — nums[" + j + "] + nums[" + i + "] = " + target + ".",
        rows: [{ label: "nums", items: nums.map(function (v, idx) {
          return { v: v, state: (idx === i || idx === j) ? "hit" : (idx < i ? "done" : "pending") };
        }) }],
        map: { label: "seen (value → index)", items: order.map(function (v) { return { v: v + "→" + seenMap[v] }; }) }
      });
      return steps;
    }

    steps.push({
      line: 8,
      narration: complement + " is not in <code>seen</code> yet.",
      rows: [{ label: "nums", items: nums.map(function (v, idx) {
        return { v: v, state: idx < i ? "done" : idx === i ? "current" : "pending" };
      }) }],
      map: { label: "seen (value → index)", items: order.map(function (v) { return { v: v + "→" + seenMap[v] }; }) }
    });

    seenMap[num] = i;
    order.push(num);
    steps.push({
      line: 10,
      narration: "Store " + num + " → index " + i + ".",
      rows: [{ label: "nums", items: nums.map(function (v, idx) {
        return { v: v, state: idx <= i ? "done" : "pending" };
      }) }],
      map: { label: "seen (value → index)", items: order.map(function (v, idx) {
        return { v: v + "→" + seenMap[v], added: idx === order.length - 1 };
      }) }
    });
  }

  steps.push({
    line: 11,
    narration: "<b>No pair found — return [].</b>",
    rows: [{ label: "nums", items: nums.map(function (v) { return { v: v, state: "done" }; }) }],
    map: { label: "seen (value → index)", items: order.map(function (v) { return { v: v + "→" + seenMap[v] }; }) }
  });
  return steps;
}''',
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
        "inputs": [{"name": "strs", "label": "strs", "type": "string-array", "default": "eat, tea, tan, ate, nat, bat", "maxLen": 12}],
        "js": '''function generateSteps(strs) {
  var steps = [];
  var groups = {};
  var order = [];

  function groupItems(highlightKey) {
    return order.map(function (k) {
      return { v: k + ": [" + groups[k].join(", ") + "]", added: k === highlightKey };
    });
  }

  steps.push({
    line: 6,
    narration: "Start with an empty map from sorted-letters key → list of words.",
    rows: [{ label: "strs", items: strs.map(function (w) { return { v: w, state: "pending" }; }) }],
    map: { label: "groups (key → words)", items: [] }
  });

  for (var i = 0; i < strs.length; i++) {
    var w = strs[i];
    var key = w.split("").sort().join("");

    steps.push({
      line: 8,
      narration: "'" + w + "' sorted → '" + key + "'.",
      rows: [{ label: "strs", items: strs.map(function (v, idx) {
        return { v: v, state: idx < i ? "done" : idx === i ? "current" : "pending" };
      }) }],
      map: { label: "groups (key → words)", items: groupItems(null) }
    });

    if (!Object.prototype.hasOwnProperty.call(groups, key)) {
      groups[key] = [];
      order.push(key);
    }
    groups[key].push(w);

    steps.push({
      line: 9,
      narration: "Add '" + w + "' under key '" + key + "'.",
      rows: [{ label: "strs", items: strs.map(function (v, idx) {
        return { v: v, state: idx <= i ? "done" : "pending" };
      }) }],
      map: { label: "groups (key → words)", items: groupItems(key) }
    });
  }

  steps.push({
    line: 10,
    narration: "<b>Return the grouped lists</b> — each group is a full set of anagrams.",
    rows: [{ label: "strs", items: strs.map(function (v) { return { v: v, state: "hit" }; }) }],
    map: { label: "groups (key → words)", items: groupItems(null) }
  });
  return steps;
}''',
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
        "inputs": [
            {"name": "nums", "label": "nums", "type": "int-array", "default": "1, 1, 1, 2, 2, 3", "maxLen": 30},
            {"name": "k", "label": "k", "type": "int", "default": "2"},
        ],
        "js": '''function generateSteps(nums, k) {
  var steps = [];
  var counts = {};
  var countOrder = [];
  nums.forEach(function (n) {
    if (!Object.prototype.hasOwnProperty.call(counts, n)) { counts[n] = 0; countOrder.push(n); }
    counts[n] += 1;
  });

  steps.push({
    line: 6,
    narration: "Count frequency of each number: " + countOrder.map(function (n) { return n + "→" + counts[n]; }).join(", ") + ".",
    rows: [{ label: "nums", items: nums.map(function (v) { return { v: v, state: "pending" }; }) }],
    map: { label: "count", items: countOrder.map(function (n) { return { v: n + ":" + counts[n], added: true }; }) }
  });

  var maxFreq = nums.length;
  var buckets = [];
  for (var f = 0; f <= maxFreq; f++) buckets.push([]);
  countOrder.forEach(function (n) { buckets[counts[n]].push(n); });

  function bucketItems() {
    var arr = [];
    for (var f2 = buckets.length - 1; f2 >= 1; f2--) {
      if (buckets[f2].length) arr.push({ v: f2 + " → [" + buckets[f2].join(", ") + "]" });
    }
    return arr;
  }

  steps.push({
    line: 9,
    narration: "Bucket numbers by frequency (bucket index = frequency).",
    rows: [{ label: "nums", items: nums.map(function (v) { return { v: v, state: "done" }; }) }],
    map: { label: "buckets (freq → nums)", items: bucketItems() }
  });

  var result = [];
  for (var freq = buckets.length - 1; freq >= 1; freq--) {
    for (var b = 0; b < buckets[freq].length; b++) {
      var num = buckets[freq][b];
      steps.push({
        line: 13,
        narration: "freq=" + freq + ": take " + num + ".",
        rows: [{ label: "result", items: result.map(function (v) { return { v: v, state: "done" }; }) }],
        map: { label: "buckets (freq → nums)", items: bucketItems() }
      });
      result.push(num);
      steps.push({
        line: 14,
        narration: "Add " + num + " to result → [" + result.join(", ") + "].",
        rows: [{ label: "result", items: result.map(function (v) { return { v: v, state: "done" }; }) }],
        map: { label: "buckets (freq → nums)", items: bucketItems() }
      });
      if (result.length === k) {
        steps.push({
          line: 16,
          narration: "<b>len(result) == k — return [" + result.join(", ") + "].</b>",
          rows: [{ label: "result", items: result.map(function (v) { return { v: v, state: "hit" }; }) }],
          map: { label: "buckets (freq → nums)", items: bucketItems() }
        });
        return steps;
      }
    }
  }

  steps.push({
    line: 17,
    narration: "<b>Return [" + result.join(", ") + "].</b>",
    rows: [{ label: "result", items: result.map(function (v) { return { v: v, state: "hit" }; }) }],
    map: { label: "buckets (freq → nums)", items: bucketItems() }
  });
  return steps;
}''',
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
        "inputs": [{"name": "nums", "label": "nums", "type": "int-array", "default": "1, 2, 3, 4", "maxLen": 20}],
        "js": '''function generateSteps(nums) {
  var steps = [];
  var n = nums.length;
  var result = new Array(n).fill(1);

  steps.push({
    line: 6,
    narration: "Initialize result with all 1s.",
    rows: [
      { label: "nums", items: nums.map(function (v) { return { v: v, state: "pending" }; }) },
      { label: "result", items: result.map(function (v) { return { v: v, state: "pending" }; }) }
    ],
    map: null
  });

  var prefix = 1;
  for (var i = 0; i < n; i++) {
    var before = prefix;
    result[i] = prefix;
    var nextPrefix = prefix * nums[i];
    steps.push({
      line: 10,
      narration: "result[" + i + "] = prefix (" + before + "); prefix *= nums[" + i + "] → " + nextPrefix + ".",
      rows: [
        { label: "nums", items: nums.map(function (v, idx) { return { v: v, state: idx < i ? "done" : idx === i ? "current" : "pending" }; }) },
        { label: "result", items: result.map(function (v, idx) { return { v: v, state: idx <= i ? "done" : "pending" }; }) }
      ],
      map: null
    });
    prefix = nextPrefix;
  }

  steps.push({
    line: 13,
    narration: "Now sweep from the right, tracking postfix (starts at 1).",
    rows: [
      { label: "nums", items: nums.map(function (v) { return { v: v, state: "pending" }; }) },
      { label: "result", items: result.map(function (v) { return { v: v, state: "pending" }; }) }
    ],
    map: null
  });

  var postfix = 1;
  for (var j = n - 1; j >= 0; j--) {
    var beforeVal = result[j];
    var beforePostfix = postfix;
    result[j] = result[j] * postfix;
    var nextPostfix = postfix * nums[j];
    steps.push({
      line: 15,
      narration: "result[" + j + "] = " + beforeVal + " × postfix(" + beforePostfix + ") = " + result[j] + "; postfix *= nums[" + j + "] → " + nextPostfix + ".",
      rows: [
        { label: "nums", items: nums.map(function (v, idx) { return { v: v, state: idx > j ? "done" : idx === j ? "current" : "pending" }; }) },
        { label: "result", items: result.map(function (v, idx) { return { v: v, state: idx >= j ? "done" : "pending" }; }) }
      ],
      map: null
    });
    postfix = nextPostfix;
  }

  steps.push({
    line: 18,
    narration: "<b>Return [" + result.join(", ") + "]</b> — no division used.",
    rows: [
      { label: "nums", items: nums.map(function (v) { return { v: v, state: "hit" }; }) },
      { label: "result", items: result.map(function (v) { return { v: v, state: "hit" }; }) }
    ],
    map: null
  });
  return steps;
}''',
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
        "inputs": [{"name": "nums", "label": "nums", "type": "int-array", "default": "100, 4, 200, 1, 3, 2", "maxLen": 30}],
        "js": '''function generateSteps(nums) {
  var steps = [];
  var uniq = [];
  var seenVal = {};
  nums.forEach(function (v) {
    if (!Object.prototype.hasOwnProperty.call(seenVal, v)) { seenVal[v] = true; uniq.push(v); }
  });
  var numSet = {};
  uniq.forEach(function (v) { numSet[v] = true; });

  var state = {};
  nums.forEach(function (v) { state[v] = "pending"; });

  function rowsSnapshot() {
    return nums.map(function (v) { return { v: v, state: state[v] }; });
  }
  function setItems() {
    return uniq.map(function (v) { return { v: v }; });
  }

  steps.push({
    line: 4,
    narration: "Put every number in a set for O(1) lookups.",
    rows: [{ label: "nums", items: rowsSnapshot() }],
    map: { label: "num_set", items: uniq.map(function (v) { return { v: v, added: true }; }) }
  });

  var longest = 0;
  for (var i = 0; i < uniq.length; i++) {
    var num = uniq[i];
    state[num] = "current";
    var hasLower = Object.prototype.hasOwnProperty.call(numSet, num - 1);
    steps.push({
      line: 8,
      narration: num + ": is " + (num - 1) + " in the set? " + (hasLower ? "Yes — not a streak start; skip." : "No — could start a streak."),
      rows: [{ label: "nums", items: rowsSnapshot() }],
      map: { label: "num_set", items: setItems() }
    });

    if (hasLower) {
      state[num] = "done";
      continue;
    }

    var length = 1;
    while (Object.prototype.hasOwnProperty.call(numSet, num + length)) length += 1;

    var isNewBest = length > longest;
    if (isNewBest) {
      longest = length;
      for (var k = 0; k < length; k++) state[num + k] = "hit";
    } else {
      state[num] = "done";
    }

    steps.push({
      line: 10,
      narration: "Count forward from " + num + ": streak length " + length + ". " + (isNewBest ? ("New best: " + length + ".") : ""),
      rows: [{ label: "nums", items: rowsSnapshot() }],
      map: { label: "num_set", items: setItems() }
    });
  }

  steps.push({
    line: 13,
    narration: "<b>Return " + longest + "</b> — the longest run has length " + longest + ".",
    rows: [{ label: "nums", items: rowsSnapshot() }],
    map: { label: "num_set", items: setItems() }
  });
  return steps;
}''',
    },

    # ---------------------------------------------------------------- Two Pointers
    {
        "slug": "valid-palindrome",
        "number": 125,
        "title": "Valid Palindrome",
        "category": "two-pointers",
        "difficulty": "Easy",
        "tags": ["String", "Two Pointers"],
        "summary": "Check if a string is a palindrome, ignoring non-alphanumeric characters and case.",
        "time": "O(n)",
        "space": "O(1)",
        "example": 's = "A man, a plan, a canal: Panama"  →  True',
        "approach": [
            "Use two pointers starting at both ends of the string, moving inward.",
            "Skip any character that isn't alphanumeric on either side.",
            "Compare the two characters case-insensitively; mismatch means not a palindrome.",
            "If the pointers meet without a mismatch, it's a palindrome.",
        ],
        "code": '''class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True''',
    },
    {
        "slug": "3sum",
        "number": 15,
        "title": "3Sum",
        "category": "two-pointers",
        "difficulty": "Medium",
        "tags": ["Array", "Two Pointers", "Sorting"],
        "summary": "Find all unique triplets in the array that sum to zero.",
        "time": "O(n²)",
        "space": "O(1) extra (excluding sort/output)",
        "example": "nums = [-1, 0, 1, 2, -1, -4]  →  [[-1,-1,2], [-1,0,1]]",
        "approach": [
            "Sort the array so duplicates sit next to each other and two pointers can work.",
            "Fix the first number nums[i], then use two pointers on the rest to find pairs summing to -nums[i].",
            "Skip duplicate values for i and for the left pointer to avoid duplicate triplets.",
            "Move the pointers inward based on whether the current sum is too low or too high.",
        ],
        "code": '''from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            if nums[i] > 0:
                break
            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    res.append([nums[i], nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
        return res''',
    },
    {
        "slug": "container-with-most-water",
        "number": 11,
        "title": "Container With Most Water",
        "category": "two-pointers",
        "difficulty": "Medium",
        "tags": ["Array", "Two Pointers", "Greedy"],
        "summary": "Choose two lines that, together with the x-axis, hold the most water.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "height = [1,8,6,2,5,4,8,3,7]  →  49",
        "approach": [
            "Start pointers at both ends — the widest possible container.",
            "The area is limited by the shorter of the two lines, so track the best area seen.",
            "Move the pointer at the shorter line inward — moving the taller one can only shrink width without helping height.",
            "Repeat until the pointers meet.",
        ],
        "code": '''from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            area = (right - left) * min(height[left], height[right])
            best = max(best, area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return best''',
    },

    # ---------------------------------------------------------------- Sliding Window
    {
        "slug": "best-time-to-buy-and-sell-stock",
        "number": 121,
        "title": "Best Time to Buy and Sell Stock",
        "category": "sliding-window",
        "difficulty": "Easy",
        "tags": ["Array", "Sliding Window", "DP"],
        "summary": "Maximize profit from one buy and one later sell.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "prices = [7,1,5,3,6,4]  →  5  (buy at 1, sell at 6)",
        "approach": [
            "Track the lowest price seen so far while scanning left to right.",
            "At each price, compute the profit if sold today (price - min_price).",
            "Keep the best profit seen; update the running minimum as you go.",
        ],
        "code": '''from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float("inf")
        best = 0
        for price in prices:
            min_price = min(min_price, price)
            best = max(best, price - min_price)
        return best''',
    },
    {
        "slug": "longest-substring-without-repeating-characters",
        "number": 3,
        "title": "Longest Substring Without Repeating Characters",
        "category": "sliding-window",
        "difficulty": "Medium",
        "tags": ["String", "Sliding Window", "Hash Map"],
        "summary": "Find the length of the longest substring with no repeated characters.",
        "time": "O(n)",
        "space": "O(min(n, charset))",
        "example": 's = "abcabcbb"  →  3  ("abc")',
        "approach": [
            "Maintain a window [left, right] with a map of the last index each character was seen at.",
            "When the character at right was already seen inside the current window, jump left past that occurrence.",
            "Update the character's last-seen index every step.",
            "Track the max window length (right - left + 1) as you slide.",
        ],
        "code": '''class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        left = 0
        best = 0
        for right, ch in enumerate(s):
            if ch in seen and seen[ch] >= left:
                left = seen[ch] + 1
            seen[ch] = right
            best = max(best, right - left + 1)
        return best''',
    },
    {
        "slug": "longest-repeating-character-replacement",
        "number": 424,
        "title": "Longest Repeating Character Replacement",
        "category": "sliding-window",
        "difficulty": "Medium",
        "tags": ["String", "Sliding Window", "Hash Map"],
        "summary": "Longest substring achievable by replacing at most k characters with any letter.",
        "time": "O(n)",
        "space": "O(1) — 26 letters",
        "example": 's = "AABABBA", k = 1  →  4',
        "approach": [
            "Grow a window while tracking counts of each letter inside it.",
            "A window is valid if (window length - most frequent letter's count) <= k — that's how many replacements it needs.",
            "If the window becomes invalid, shrink it from the left by one.",
            "Track the best valid window length throughout; max_count doesn't need to shrink accurately since only its peak matters.",
        ],
        "code": '''class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        counts = {}
        left = 0
        max_count = 0
        best = 0
        for right, ch in enumerate(s):
            counts[ch] = counts.get(ch, 0) + 1
            max_count = max(max_count, counts[ch])
            while (right - left + 1) - max_count > k:
                counts[s[left]] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best''',
    },
    {
        "slug": "minimum-window-substring",
        "number": 76,
        "title": "Minimum Window Substring",
        "category": "sliding-window",
        "difficulty": "Hard",
        "tags": ["String", "Sliding Window", "Hash Map"],
        "summary": "Smallest substring of s containing every character of t (with multiplicity).",
        "time": "O(n + m)",
        "space": "O(charset)",
        "example": 's = "ADOBECODEBANC", t = "ABC"  →  "BANC"',
        "approach": [
            "Count required characters from t; track how many distinct required counts are still 'missing'.",
            "Expand the window's right edge, decrementing need[ch] and reducing missing when a needed char is fully covered.",
            "Once missing reaches 0, the window contains all of t — try to shrink from the left while it stays valid, recording the best window.",
            "Continue expanding right until s is exhausted.",
        ],
        "code": '''from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""
        need = Counter(t)
        missing = len(t)
        left = 0
        best_left, best_right = 0, 0
        best_len = float("inf")

        for right, ch in enumerate(s, 1):
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1

            if missing == 0:
                while left < right and need[s[left]] < 0:
                    need[s[left]] += 1
                    left += 1
                if right - left < best_len:
                    best_len = right - left
                    best_left, best_right = left, right

        return s[best_left:best_right] if best_len != float("inf") else ""''',
    },

    # ---------------------------------------------------------------- Stack
    {
        "slug": "valid-parentheses",
        "number": 20,
        "title": "Valid Parentheses",
        "category": "stack",
        "difficulty": "Easy",
        "tags": ["String", "Stack"],
        "summary": "Check if brackets in a string are properly opened and closed in order.",
        "time": "O(n)",
        "space": "O(n)",
        "example": 's = "()[]{}"  →  True',
        "approach": [
            "Push opening brackets onto a stack as you scan left to right.",
            "On a closing bracket, it must match the bracket on top of the stack — pop and compare.",
            "If the stack is empty or the top doesn't match, the string is invalid.",
            "At the end, the stack must be empty — no unclosed brackets remain.",
        ],
        "code": '''class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for ch in s:
            if ch in pairs:
                if not stack or stack.pop() != pairs[ch]:
                    return False
            else:
                stack.append(ch)
        return not stack''',
    },

    # ---------------------------------------------------------------- Binary Search
    {
        "slug": "find-minimum-in-rotated-sorted-array",
        "number": 153,
        "title": "Find Minimum in Rotated Sorted Array",
        "category": "binary-search",
        "difficulty": "Medium",
        "tags": ["Array", "Binary Search"],
        "summary": "Find the minimum element in an ascending array that's been rotated.",
        "time": "O(log n)",
        "space": "O(1)",
        "example": "nums = [4,5,6,7,0,1,2]  →  0",
        "approach": [
            "Binary search, comparing nums[mid] to nums[right] to decide which half is sorted.",
            "If nums[mid] > nums[right], the minimum is in the right half (past mid) — move left = mid + 1.",
            "Otherwise the minimum is at mid or to its left — move right = mid.",
            "When left == right, that's the minimum.",
        ],
        "code": '''from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        return nums[left]''',
    },
    {
        "slug": "search-in-rotated-sorted-array",
        "number": 33,
        "title": "Search in Rotated Sorted Array",
        "category": "binary-search",
        "difficulty": "Medium",
        "tags": ["Array", "Binary Search"],
        "summary": "Search for target in an ascending array rotated at an unknown pivot.",
        "time": "O(log n)",
        "space": "O(1)",
        "example": "nums = [4,5,6,7,0,1,2], target = 0  →  4",
        "approach": [
            "At each step, at least one half of [left, mid] or [mid, right] is normally sorted — figure out which.",
            "If the left half is sorted, check whether target falls within its range to decide which half to search.",
            "Otherwise the right half is sorted — apply the same range check there.",
            "Narrow left/right accordingly each step, same as standard binary search.",
        ],
        "code": '''from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1''',
    },

    # ---------------------------------------------------------------- Linked List
    {
        "slug": "reverse-linked-list",
        "number": 206,
        "title": "Reverse Linked List",
        "category": "linked-list",
        "difficulty": "Easy",
        "tags": ["Linked List"],
        "summary": "Reverse a singly linked list in place.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "1 → 2 → 3 → 4  becomes  4 → 3 → 2 → 1",
        "approach": [
            "Walk the list with two pointers: prev (starts None) and curr (starts head).",
            "At each node, save curr.next before overwriting it, then point curr.next back to prev.",
            "Advance prev to curr and curr to the saved next node.",
            "When curr is None, prev is the new head.",
        ],
        "code": '''from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev''',
    },
    {
        "slug": "merge-two-sorted-lists",
        "number": 21,
        "title": "Merge Two Sorted Lists",
        "category": "linked-list",
        "difficulty": "Easy",
        "tags": ["Linked List"],
        "summary": "Merge two sorted linked lists into one sorted list.",
        "time": "O(n + m)",
        "space": "O(1)",
        "example": "l1 = 1→2→4, l2 = 1→3→4  →  1→1→2→3→4→4",
        "approach": [
            "Use a dummy head node so the merged list always has a starting point to return.",
            "Compare the heads of both lists, attach the smaller one to the tail, and advance that list.",
            "Repeat until one list is exhausted.",
            "Attach whatever remains of the other list — it's already sorted.",
        ],
        "code": '''from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next''',
    },
    {
        "slug": "linked-list-cycle",
        "number": 141,
        "title": "Linked List Cycle",
        "category": "linked-list",
        "difficulty": "Easy",
        "tags": ["Linked List", "Two Pointers"],
        "summary": "Detect whether a linked list has a cycle, using O(1) space.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "3 → 2 → 0 → -4 → (back to 2)  →  True",
        "approach": [
            "Use Floyd's tortoise and hare: a slow pointer moves 1 step, a fast pointer moves 2 steps.",
            "If there's no cycle, fast (or fast.next) reaches None and we return False.",
            "If there is a cycle, the fast pointer eventually laps the slow pointer and they meet.",
            "A meeting (slow is fast) proves a cycle exists.",
        ],
        "code": '''from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False''',
    },
    {
        "slug": "reorder-list",
        "number": 143,
        "title": "Reorder List",
        "category": "linked-list",
        "difficulty": "Medium",
        "tags": ["Linked List", "Two Pointers"],
        "summary": "Reorder L0→L1→…→Ln to L0→Ln→L1→Ln-1→… in place.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "1→2→3→4  becomes  1→4→2→3",
        "approach": [
            "Find the middle of the list with slow/fast pointers.",
            "Reverse the second half of the list in place.",
            "Merge the first half and reversed second half by alternating nodes.",
            "Stop once the second (shorter or equal) half is exhausted.",
        ],
        "code": '''from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        second = slow.next
        slow.next = None
        prev = None
        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt

        first, second = head, prev
        while second:
            first.next, first = second, first.next
            second.next, second = first, second.next''',
    },
    {
        "slug": "remove-nth-node-from-end-of-list",
        "number": 19,
        "title": "Remove Nth Node From End of List",
        "category": "linked-list",
        "difficulty": "Medium",
        "tags": ["Linked List", "Two Pointers"],
        "summary": "Remove the nth node from the end of the list in one pass.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "1→2→3→4→5, n = 2  →  1→2→3→5",
        "approach": [
            "Use a dummy node before head so removing the actual head is handled uniformly.",
            "Advance a fast pointer n steps ahead of a slow pointer.",
            "Move both pointers together until fast reaches the last node.",
            "slow is now just before the node to remove — unlink it with slow.next = slow.next.next.",
        ],
        "code": '''from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n):
            fast = fast.next
        while fast.next:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next''',
    },
    {
        "slug": "merge-k-sorted-lists",
        "number": 23,
        "title": "Merge k Sorted Lists",
        "category": "linked-list",
        "difficulty": "Hard",
        "tags": ["Linked List", "Heap", "Divide and Conquer"],
        "summary": "Merge k sorted linked lists into one sorted list.",
        "time": "O(n log k) — n total nodes, k lists",
        "space": "O(k)",
        "example": "lists = [[1,4,5],[1,3,4],[2,6]]  →  [1,1,2,3,4,4,5,6]",
        "approach": [
            "Push the head of each non-empty list into a min-heap, keyed by value.",
            "Repeatedly pop the smallest node, attach it to the result tail, and push its successor if it has one.",
            "A list index tiebreaker in the heap tuple avoids comparing ListNode objects directly.",
            "This is effectively a k-way merge in O(n log k).",
        ],
        "code": '''from typing import List, Optional
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))

        dummy = ListNode()
        tail = dummy
        while heap:
            val, i, node = heapq.heappop(heap)
            tail.next = node
            tail = tail.next
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next''',
    },

    # ---------------------------------------------------------------- Trees
    {
        "slug": "invert-binary-tree",
        "number": 226,
        "title": "Invert Binary Tree",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["Tree", "DFS", "BFS"],
        "summary": "Flip a binary tree into its mirror image.",
        "time": "O(n)",
        "space": "O(h)",
        "example": "root = [4,2,7,1,3,6,9]  →  [4,7,2,9,6,3,1]  (mirrored)",
        "approach": [
            "Recursively invert the left and right subtrees.",
            "Swap the (already-inverted) left and right children at each node.",
            "Base case: an empty subtree inverts to itself (None).",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root''',
    },
    {
        "slug": "maximum-depth-of-binary-tree",
        "number": 104,
        "title": "Maximum Depth of Binary Tree",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["Tree", "DFS", "BFS"],
        "summary": "Find the length of the longest root-to-leaf path.",
        "time": "O(n)",
        "space": "O(h)",
        "example": "[3,9,20,null,null,15,7]  →  3",
        "approach": [
            "An empty tree has depth 0.",
            "Otherwise, the depth is 1 plus the deeper of the two subtrees' depths.",
            "Recurse on left and right, then combine.",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))''',
    },
    {
        "slug": "same-tree",
        "number": 100,
        "title": "Same Tree",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["Tree", "DFS"],
        "summary": "Check whether two binary trees are structurally identical with the same values.",
        "time": "O(n)",
        "space": "O(h)",
        "example": "p = [1,2,3], q = [1,2,3]  →  True",
        "approach": [
            "If both nodes are None, they match at this position.",
            "If exactly one is None, or their values differ, the trees don't match.",
            "Otherwise recurse on both left subtrees and both right subtrees, requiring both to match.",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)''',
    },
    {
        "slug": "subtree-of-another-tree",
        "number": 572,
        "title": "Subtree of Another Tree",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["Tree", "DFS"],
        "summary": "Check whether subRoot appears as an exact subtree anywhere in root.",
        "time": "O(m · n) worst case",
        "space": "O(h)",
        "example": "root = [3,4,5,1,2], subRoot = [4,1,2]  →  True",
        "approach": [
            "At each node of root, check if the tree rooted there is identical to subRoot (reusing a same-tree check).",
            "If it matches, we're done.",
            "Otherwise recurse into root's left and right children and try again.",
            "An empty root only matches an empty subRoot.",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if not root:
            return subRoot is None
        if self.sameTree(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def sameTree(self, a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return self.sameTree(a.left, b.left) and self.sameTree(a.right, b.right)''',
    },
    {
        "slug": "binary-tree-level-order-traversal",
        "number": 102,
        "title": "Binary Tree Level Order Traversal",
        "category": "trees",
        "difficulty": "Medium",
        "tags": ["Tree", "BFS"],
        "summary": "Return node values grouped level by level, top to bottom.",
        "time": "O(n)",
        "space": "O(n)",
        "example": "[3,9,20,null,null,15,7]  →  [[3],[9,20],[15,7]]",
        "approach": [
            "BFS with a queue, but process one full level at a time.",
            "Before dequeuing, note the current queue size — that's exactly this level's node count.",
            "Pop that many nodes, collect their values, and enqueue their children for the next level.",
            "Append each level's collected values to the result.",
        ],
        "code": '''from typing import List, Optional
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        result = []
        queue = deque([root]) if root else deque()
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result''',
    },
    {
        "slug": "construct-binary-tree-from-preorder-and-inorder-traversal",
        "number": 105,
        "title": "Construct Binary Tree from Preorder and Inorder Traversal",
        "category": "trees",
        "difficulty": "Medium",
        "tags": ["Tree", "DFS", "Hash Map"],
        "summary": "Rebuild a binary tree from its preorder and inorder traversals.",
        "time": "O(n)",
        "space": "O(n)",
        "example": "preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]",
        "approach": [
            "Preorder's first element is always the current subtree's root.",
            "Find that value's position in inorder — everything left of it is the left subtree, everything right is the right subtree.",
            "A hash map from value → inorder index makes that lookup O(1).",
            "Advance a shared preorder index and recurse, building left before right (matching preorder's order).",
        ],
        "code": '''from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        inorder_index = {val: i for i, val in enumerate(inorder)}
        self.pre_idx = 0

        def build(left: int, right: int) -> Optional[TreeNode]:
            if left > right:
                return None
            val = preorder[self.pre_idx]
            self.pre_idx += 1
            root = TreeNode(val)
            mid = inorder_index[val]
            root.left = build(left, mid - 1)
            root.right = build(mid + 1, right)
            return root

        return build(0, len(inorder) - 1)''',
    },
    {
        "slug": "binary-tree-maximum-path-sum",
        "number": 124,
        "title": "Binary Tree Maximum Path Sum",
        "category": "trees",
        "difficulty": "Hard",
        "tags": ["Tree", "DFS"],
        "summary": "Find the maximum sum along any path (not necessarily through the root).",
        "time": "O(n)",
        "space": "O(h)",
        "example": "[-10,9,20,null,null,15,7]  →  42",
        "approach": [
            "For each node, compute the best 'downward' path sum starting at it (dfs's return value) — a path can only extend through one child upward.",
            "Negative subtree contributions are clamped to 0 (better to not include them).",
            "At each node, consider the path that goes through it using BOTH children (a 'peak') and update the global best.",
            "Return only node.val + max(left, right) upward, since a path passed to the parent can't branch both ways.",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        best = float("-inf")

        def dfs(node: Optional[TreeNode]) -> int:
            nonlocal best
            if not node:
                return 0
            left = max(dfs(node.left), 0)
            right = max(dfs(node.right), 0)
            best = max(best, node.val + left + right)
            return node.val + max(left, right)

        dfs(root)
        return best''',
    },
    {
        "slug": "serialize-and-deserialize-binary-tree",
        "number": 297,
        "title": "Serialize and Deserialize Binary Tree",
        "category": "trees",
        "difficulty": "Hard",
        "tags": ["Tree", "DFS", "Design"],
        "summary": "Convert a binary tree to a string and back, preserving structure exactly.",
        "time": "O(n) for each operation",
        "space": "O(n)",
        "example": '[1,2,3,null,null,4,5]  →  "1,2,#,#,3,4,#,#,5,#,#"  →  same tree',
        "approach": [
            "Serialize with preorder DFS, writing '#' for every None child so structure is unambiguous.",
            "Join values with a delimiter (comma) into one string.",
            "Deserialize by reading tokens in the same preorder sequence: a '#' means None, otherwise build a node and recurse for its left then right child.",
            "An iterator over the split tokens keeps the recursive rebuild in lockstep with the serialized order.",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        vals = []

        def dfs(node):
            if not node:
                vals.append("#")
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(vals)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        vals = iter(data.split(","))

        def build():
            val = next(vals)
            if val == "#":
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node

        return build()''',
    },
    {
        "slug": "lowest-common-ancestor-of-a-binary-search-tree",
        "number": 235,
        "title": "Lowest Common Ancestor of a Binary Search Tree",
        "category": "trees",
        "difficulty": "Medium",
        "tags": ["Tree", "BST"],
        "summary": "Find the lowest node that has both p and q as descendants, in a BST.",
        "time": "O(h)",
        "space": "O(1)",
        "example": "root = [6,2,8,0,4,7,9], p = 2, q = 8  →  6",
        "approach": [
            "Use the BST property instead of general tree search: at each node, compare both target values to node.val.",
            "If both p and q are smaller, the LCA must be in the left subtree — move there.",
            "If both are larger, move right.",
            "The first node where they diverge (or match) is the split point — the LCA.",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                return node
        return None''',
    },
    {
        "slug": "validate-binary-search-tree",
        "number": 98,
        "title": "Validate Binary Search Tree",
        "category": "trees",
        "difficulty": "Medium",
        "tags": ["Tree", "DFS", "BST"],
        "summary": "Check whether a binary tree satisfies the BST property everywhere.",
        "time": "O(n)",
        "space": "O(h)",
        "example": "[5,1,4,null,null,3,6]  →  False  (4 < 5 but is in right subtree)",
        "approach": [
            "It's not enough to compare a node only to its direct children — every node in a left subtree must be less than ALL of its ancestors, not just its parent.",
            "Carry a valid (low, high) range down through the recursion.",
            "At each node, check low < node.val < high; recurse left with high = node.val, recurse right with low = node.val.",
            "An empty subtree is always valid.",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def valid(node, low, high) -> bool:
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return valid(node.left, low, node.val) and valid(node.right, node.val, high)

        return valid(root, float("-inf"), float("inf"))''',
    },
    {
        "slug": "kth-smallest-element-in-a-bst",
        "number": 230,
        "title": "Kth Smallest Element in a BST",
        "category": "trees",
        "difficulty": "Medium",
        "tags": ["Tree", "DFS", "BST"],
        "summary": "Find the kth smallest value in a binary search tree.",
        "time": "O(h + k)",
        "space": "O(h)",
        "example": "root = [3,1,4,null,2], k = 1  →  1",
        "approach": [
            "An inorder traversal of a BST visits values in ascending order.",
            "Simulate that traversal iteratively with an explicit stack instead of recursion.",
            "Push left children until there are none, then pop, count it, and move to the right child.",
            "The kth node popped is the answer — no need to build the full sorted list.",
        ],
        "code": '''from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        node = root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val
            node = node.right''',
    },

    # ---------------------------------------------------------------- Tries
    {
        "slug": "implement-trie-prefix-tree",
        "number": 208,
        "title": "Implement Trie (Prefix Tree)",
        "category": "tries",
        "difficulty": "Medium",
        "tags": ["Trie", "Design", "Hash Map"],
        "summary": "Implement insert, search, and startsWith for a prefix tree.",
        "time": "O(m) per operation, m = word length",
        "space": "O(total characters inserted)",
        "example": 'insert("apple"); search("apple") → True; startsWith("app") → True',
        "approach": [
            "Each TrieNode holds a map of character → child node, plus an 'end of word' flag.",
            "insert: walk/create a child for each character, then mark the last node as end.",
            "search: walk the characters; if any is missing, fail — otherwise check the end flag.",
            "startsWith: same walk, but don't check the end flag — just that the path exists.",
        ],
        "code": '''class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.end

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, word: str):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node''',
    },
    {
        "slug": "design-add-and-search-words-data-structure",
        "number": 211,
        "title": "Design Add and Search Words Data Structure",
        "category": "tries",
        "difficulty": "Medium",
        "tags": ["Trie", "DFS", "Design"],
        "summary": "Support adding words and searching with '.' as a wildcard for any letter.",
        "time": "O(m) typical, O(26^m) worst case with many wildcards",
        "space": "O(total characters added)",
        "example": 'addWord("bad"); search("b.d") → True',
        "approach": [
            "Store words in a trie exactly like Implement Trie.",
            "Search with DFS instead of a straight walk, to handle backtracking.",
            "On a normal letter, follow that one child if it exists.",
            "On '.', try every child at that level — if any path leads to a match, return True.",
        ],
        "code": '''class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True

    def search(self, word: str) -> bool:
        def dfs(node: TrieNode, i: int) -> bool:
            if i == len(word):
                return node.end
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for child in node.children.values())
            if ch not in node.children:
                return False
            return dfs(node.children[ch], i + 1)

        return dfs(self.root, 0)''',
    },
    {
        "slug": "word-search-ii",
        "number": 212,
        "title": "Word Search II",
        "category": "tries",
        "difficulty": "Hard",
        "tags": ["Trie", "DFS", "Backtracking", "Matrix"],
        "summary": "Find all given words that can be traced out on a letter grid.",
        "time": "O(rows · cols · 4 · 3^L)",
        "space": "O(N) for the trie",
        "example": 'board of letters, words = ["oath","pea","eat","rain"]  →  ["eat","oath"]',
        "approach": [
            "Build one trie from all target words instead of searching for each word separately on the grid.",
            "DFS from every board cell, walking the trie alongside the grid path.",
            "Mark visited cells temporarily (e.g. '#') to avoid reusing a letter in the same path, then restore it.",
            "When a trie node marked as a word-end is reached, record that word and keep exploring (a word can be a prefix of another).",
        ],
        "code": '''from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = TrieNode()
        for word in words:
            node = root
            for ch in word:
                node = node.children.setdefault(ch, TrieNode())
            node.word = word

        rows, cols = len(board), len(board[0])
        result = set()

        def dfs(r: int, c: int, node: TrieNode) -> None:
            ch = board[r][c]
            if ch not in node.children:
                return
            nxt = node.children[ch]
            if nxt.word:
                result.add(nxt.word)

            board[r][c] = "#"
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    dfs(nr, nc, nxt)
            board[r][c] = ch

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)

        return list(result)''',
    },

    # ---------------------------------------------------------------- Heap / Priority Queue
    {
        "slug": "find-median-from-data-stream",
        "number": 295,
        "title": "Find Median from Data Stream",
        "category": "heap",
        "difficulty": "Hard",
        "tags": ["Heap", "Design"],
        "summary": "Support adding numbers one at a time and querying the running median.",
        "time": "O(log n) add, O(1) query",
        "space": "O(n)",
        "example": "addNum(1), addNum(2) → median 1.5; addNum(3) → median 2",
        "approach": [
            "Split numbers across two heaps: 'small' (max-heap, via negation) for the lower half, 'large' (min-heap) for the upper half.",
            "Always push into small first, then move its top into large to keep values properly partitioned.",
            "Rebalance so small never has more than one extra element compared to large.",
            "If small has one more element, it holds the median; otherwise average the two tops.",
        ],
        "code": '''import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (negated)
        self.large = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2''',
    },

    # ---------------------------------------------------------------- Backtracking
    {
        "slug": "word-search",
        "number": 79,
        "title": "Word Search",
        "category": "backtracking",
        "difficulty": "Medium",
        "tags": ["Backtracking", "DFS", "Matrix"],
        "summary": "Check if a word can be traced through adjacent cells on a grid, no cell reused.",
        "time": "O(rows · cols · 4^L)",
        "space": "O(L) recursion depth",
        "example": 'board = [["A","B","C"],["S","F","C"],["A","D","E"]], word = "ABCCED"  →  True',
        "approach": [
            "Try starting the DFS from every cell that matches the word's first letter.",
            "At each step, if the current cell matches word[i], mark it visited (e.g. overwrite temporarily) and explore all 4 neighbors for word[i+1].",
            "Restore the cell after exploring (backtrack) so other paths can use it.",
            "Success when the recursion reaches the end of the word.",
        ],
        "code": '''from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r: int, c: int, i: int) -> bool:
            if i == len(word):
                return True
            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[i]:
                return False

            temp = board[r][c]
            board[r][c] = "#"
            found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                     dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
            board[r][c] = temp
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False''',
    },
    {
        "slug": "combination-sum",
        "number": 39,
        "title": "Combination Sum",
        "category": "backtracking",
        "difficulty": "Medium",
        "tags": ["Backtracking", "Array"],
        "summary": "Find all unique combinations of candidates that sum to target (reuse allowed).",
        "time": "O(2^t) worst case, t = target",
        "space": "O(t) recursion depth",
        "example": "candidates = [2,3,6,7], target = 7  →  [[2,2,3], [7]]",
        "approach": [
            "Backtrack, tracking the current path and remaining target.",
            "At each step, try each candidate from the current start index onward (not from 0) — this allows reuse of the same number while preventing duplicate combinations in different orders.",
            "If remaining hits exactly 0, record the path; if it goes negative, prune that branch.",
            "Pass the same index (not index+1) when recursing to allow reusing a candidate.",
        ],
        "code": '''from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        path = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return
            if remaining < 0:
                return
            for i in range(start, len(candidates)):
                path.append(candidates[i])
                backtrack(i, remaining - candidates[i])
                path.pop()

        backtrack(0, target)
        return result''',
    },

    # ---------------------------------------------------------------- Graphs
    {
        "slug": "number-of-islands",
        "number": 200,
        "title": "Number of Islands",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["Graph", "BFS", "DFS", "Matrix"],
        "summary": "Count the number of connected groups of '1's in a grid.",
        "time": "O(rows · cols)",
        "space": "O(rows · cols)",
        "example": '[["1","1","0"],["0","1","0"],["0","0","1"]]  →  2',
        "approach": [
            "Scan every cell; whenever an unvisited '1' is found, that's a brand new island — increment the count.",
            "BFS (or DFS) outward from that cell across all connected '1's, marking each visited so it isn't recounted.",
            "Only explore the 4 orthogonal neighbors (up/down/left/right).",
            "Continue scanning after the flood-fill returns.",
        ],
        "code": '''from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])
        visited = set()
        count = 0

        def bfs(r: int, c: int) -> None:
            queue = [(r, c)]
            visited.add((r, c))
            while queue:
                row, col = queue.pop()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = row + dr, col + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                            grid[nr][nc] == "1" and (nr, nc) not in visited):
                        visited.add((nr, nc))
                        queue.append((nr, nc))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1" and (r, c) not in visited:
                    bfs(r, c)
                    count += 1
        return count''',
    },
    {
        "slug": "clone-graph",
        "number": 133,
        "title": "Clone Graph",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["Graph", "DFS", "Hash Map"],
        "summary": "Deep-copy a connected undirected graph given a reference node.",
        "time": "O(V + E)",
        "space": "O(V)",
        "example": "adjList = [[2,4],[1,3],[2,4],[1,3]]  →  identical structure, new nodes",
        "approach": [
            "Keep a map from original node → its clone, so each node is only cloned once (handles cycles).",
            "DFS from the given node: if already cloned, return the existing clone.",
            "Otherwise create a clone, register it in the map immediately (before recursing) to break cycles, then recursively clone and attach each neighbor.",
        ],
        "code": '''from typing import Optional

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors or []

class Solution:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return None
        clones = {}

        def dfs(n):
            if n in clones:
                return clones[n]
            copy = Node(n.val)
            clones[n] = copy
            for neighbor in n.neighbors:
                copy.neighbors.append(dfs(neighbor))
            return copy

        return dfs(node)''',
    },
    {
        "slug": "pacific-atlantic-water-flow",
        "number": 417,
        "title": "Pacific Atlantic Water Flow",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["Graph", "DFS", "Matrix"],
        "summary": "Find cells from which water can flow to both the Pacific and Atlantic oceans.",
        "time": "O(rows · cols)",
        "space": "O(rows · cols)",
        "example": "heights grid, oceans border top/left (Pacific) and bottom/right (Atlantic)",
        "approach": [
            "Instead of checking 'can this cell reach the ocean' (expensive per cell), reverse it: flow uphill from each ocean's border cells inward.",
            "DFS from every Pacific-adjacent border cell, moving to neighbors with height >= current (since water flows downhill, reversed means uphill-or-equal is reachable).",
            "Do the same from Atlantic-adjacent border cells into a separate visited set.",
            "A cell reachable from both oceans is part of the answer.",
        ],
        "code": '''from typing import List

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights:
            return []
        rows, cols = len(heights), len(heights[0])
        pacific, atlantic = set(), set()

        def dfs(r: int, c: int, visited: set, prev_height: int) -> None:
            if ((r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or
                    heights[r][c] < prev_height):
                return
            visited.add((r, c))
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                dfs(r + dr, c + dc, visited, heights[r][c])

        for c in range(cols):
            dfs(0, c, pacific, heights[0][c])
            dfs(rows - 1, c, atlantic, heights[rows - 1][c])
        for r in range(rows):
            dfs(r, 0, pacific, heights[r][0])
            dfs(r, cols - 1, atlantic, heights[r][cols - 1])

        return [[r, c] for r in range(rows) for c in range(cols) if (r, c) in pacific and (r, c) in atlantic]''',
    },
    {
        "slug": "course-schedule",
        "number": 207,
        "title": "Course Schedule",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["Graph", "DFS", "Topological Sort"],
        "summary": "Determine if all courses can be finished given prerequisite pairs (i.e. no cycle).",
        "time": "O(V + E)",
        "space": "O(V + E)",
        "example": "numCourses = 2, prerequisites = [[1,0]]  →  True",
        "approach": [
            "Model courses and prerequisites as a directed graph; finishing all courses is possible iff the graph has no cycle.",
            "DFS each course, tracking state: 0 = currently visiting (on the recursion stack), 1 = fully processed.",
            "If DFS revisits a node that's still 'visiting', that's a cycle — return False.",
            "Memoize fully processed nodes so each is only explored once overall.",
        ],
        "code": '''from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = {i: [] for i in range(numCourses)}
        for course, pre in prerequisites:
            graph[course].append(pre)

        state = {}  # 0 = visiting, 1 = done

        def dfs(course: int) -> bool:
            if course in state:
                return state[course] == 1
            state[course] = 0
            for pre in graph[course]:
                if not dfs(pre):
                    return False
            state[course] = 1
            return True

        return all(dfs(course) for course in range(numCourses))''',
    },
    {
        "slug": "number-of-connected-components-in-an-undirected-graph",
        "number": 323,
        "title": "Number of Connected Components in an Undirected Graph",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["Graph", "Union-Find"],
        "summary": "Count connected components given n nodes and a list of undirected edges.",
        "time": "O(E · α(n)) — near O(E)",
        "space": "O(n)",
        "example": "n = 5, edges = [[0,1],[1,2],[3,4]]  →  2",
        "approach": [
            "Union-Find (Disjoint Set Union): start with n separate components, one per node.",
            "For each edge, union its two endpoints; if they were already in the same set, no component count changes.",
            "Path compression (find) and union by rank keep operations nearly O(1) amortized.",
            "Each successful union merges two components into one, so decrement the running count.",
        ],
        "code": '''from typing import List

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        rank = [1] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> bool:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            rank[ra] += rank[rb]
            return True

        components = n
        for a, b in edges:
            if union(a, b):
                components -= 1
        return components''',
    },
    {
        "slug": "graph-valid-tree",
        "number": 261,
        "title": "Graph Valid Tree",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["Graph", "Union-Find"],
        "summary": "Check whether n nodes and a list of edges form a valid tree.",
        "time": "O(E · α(n))",
        "space": "O(n)",
        "example": "n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]  →  True",
        "approach": [
            "A valid tree on n nodes must have exactly n - 1 edges — check that first as a cheap filter.",
            "With exactly n - 1 edges, the graph is a tree iff it's fully connected with no cycles.",
            "Union-Find each edge: if two endpoints are already connected, adding this edge creates a cycle — not a tree.",
            "If every union succeeds (no cycle found) and the edge count matched, it's a valid tree.",
        ],
        "code": '''from typing import List

class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> bool:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
            return True

        return all(union(a, b) for a, b in edges)''',
    },
    {
        "slug": "alien-dictionary",
        "number": 269,
        "title": "Alien Dictionary",
        "category": "graphs",
        "difficulty": "Hard",
        "tags": ["Graph", "DFS", "Topological Sort"],
        "summary": "Derive a valid character ordering for an alien language from a sorted word list.",
        "time": "O(C) — total characters across all words",
        "space": "O(1) — bounded alphabet",
        "example": 'words = ["wrt","wrf","er","ett","rftt"]  →  "wertf"',
        "approach": [
            "Compare each pair of adjacent words: the first differing character tells you one letter comes before another — add that as a directed edge.",
            "If one word is a prefix of the next, that's fine; if the longer word comes first, the ordering is invalid.",
            "Topologically sort the resulting letter graph via DFS, marking nodes 'visiting' then 'done' to detect cycles (an invalid ordering).",
            "Append each letter to the order list as its DFS finishes, then reverse — that's standard post-order topological sort.",
        ],
        "code": '''from typing import List

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        graph = {ch: set() for word in words for ch in word}

        for w1, w2 in zip(words, words[1:]):
            min_len = min(len(w1), len(w2))
            if w1[:min_len] == w2[:min_len] and len(w1) > len(w2):
                return ""
            for c1, c2 in zip(w1, w2):
                if c1 != c2:
                    graph[c1].add(c2)
                    break

        state = {}  # False = visiting, True = done
        order = []

        def dfs(ch: str) -> bool:
            if ch in state:
                return state[ch]
            state[ch] = False
            for nxt in graph[ch]:
                if not dfs(nxt):
                    return False
            state[ch] = True
            order.append(ch)
            return True

        for ch in graph:
            if not dfs(ch):
                return ""

        order.reverse()
        return "".join(order)''',
    },

    # ---------------------------------------------------------------- 1-D Dynamic Programming
    {
        "slug": "climbing-stairs",
        "number": 70,
        "title": "Climbing Stairs",
        "category": "dp-1d",
        "difficulty": "Easy",
        "tags": ["DP"],
        "summary": "Count distinct ways to climb n stairs, taking 1 or 2 steps at a time.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "n = 5  →  8",
        "approach": [
            "The number of ways to reach step n is ways(n-1) + ways(n-2) — you arrive either from one step back or two steps back. This is Fibonacci.",
            "Base cases: 1 way to reach step 1, 2 ways to reach step 2.",
            "Iterate up from step 3, keeping only the last two values instead of a full array.",
        ],
        "code": '''class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        prev, curr = 1, 2
        for _ in range(3, n + 1):
            prev, curr = curr, prev + curr
        return curr''',
    },
    {
        "slug": "house-robber",
        "number": 198,
        "title": "House Robber",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP"],
        "summary": "Maximize loot from houses in a row, without robbing two adjacent houses.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "nums = [2,7,9,3,1]  →  12  (rob 2 + 9 + 1)",
        "approach": [
            "At each house, choose: skip it (keep the best total so far) or rob it (that house's value + best total from two houses back).",
            "Track only the last two running best values (prev, curr) instead of a full DP array.",
            "curr becomes max(curr, prev + num) — either the total unchanged, or rob this house.",
        ],
        "code": '''from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        prev, curr = 0, 0
        for num in nums:
            prev, curr = curr, max(curr, prev + num)
        return curr''',
    },
    {
        "slug": "house-robber-ii",
        "number": 213,
        "title": "House Robber II",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP"],
        "summary": "Same as House Robber, but houses are arranged in a circle.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "nums = [2,3,2]  →  3",
        "approach": [
            "Because the first and last houses are now adjacent, they can't both be robbed.",
            "Reduce to two separate House Robber runs: one excluding the first house, one excluding the last.",
            "The answer is the max of those two runs (this correctly handles the wrap-around).",
            "Special-case a single house, since slicing would otherwise produce empty ranges.",
        ],
        "code": '''from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def rob_line(houses: List[int]) -> int:
            prev, curr = 0, 0
            for num in houses:
                prev, curr = curr, max(curr, prev + num)
            return curr

        return max(rob_line(nums[1:]), rob_line(nums[:-1]))''',
    },
    {
        "slug": "decode-ways",
        "number": 91,
        "title": "Decode Ways",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "String"],
        "summary": "Count ways to decode a digit string where 'A'-'Z' map to 1-26.",
        "time": "O(n)",
        "space": "O(1)",
        "example": '"226"  →  3  ("BZ", "VF", "BBF")',
        "approach": [
            "dp[i] = number of ways to decode the first i characters.",
            "A single digit s[i-1] contributes dp[i-1] ways if it's not '0'.",
            "The two-digit combo s[i-2:i] contributes dp[i-2] ways if it's between 10 and 26.",
            "Sum both contributions; track only the last two dp values for O(1) space.",
        ],
        "code": '''class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == "0":
            return 0
        n = len(s)
        prev, curr = 1, 1
        for i in range(1, n):
            count = 0
            if s[i] != "0":
                count += curr
            two_digit = int(s[i - 1:i + 1])
            if 10 <= two_digit <= 26:
                count += prev
            prev, curr = curr, count
        return curr''',
    },
    {
        "slug": "coin-change",
        "number": 322,
        "title": "Coin Change",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP"],
        "summary": "Find the fewest coins needed to make up a given amount (or -1 if impossible).",
        "time": "O(amount · number of coin types)",
        "space": "O(amount)",
        "example": "coins = [1,2,5], amount = 11  →  3  (5+5+1)",
        "approach": [
            "Bottom-up DP: dp[a] = fewest coins to make amount a, with dp[0] = 0.",
            "For every amount from 1 up to the target, try every coin: if the coin fits, dp[a] = min(dp[a], dp[a - coin] + 1).",
            "Initialize all dp values (besides 0) to infinity so unreachable amounts stay unreachable.",
            "If dp[amount] is still infinity at the end, it's impossible — return -1.",
        ],
        "code": '''from typing import List

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [0] + [float("inf")] * amount
        for a in range(1, amount + 1):
            for coin in coins:
                if coin <= a:
                    dp[a] = min(dp[a], dp[a - coin] + 1)
        return dp[amount] if dp[amount] != float("inf") else -1''',
    },
    {
        "slug": "maximum-product-subarray",
        "number": 152,
        "title": "Maximum Product Subarray",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "Array"],
        "summary": "Find the contiguous subarray with the largest product.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "nums = [2,3,-2,4]  →  6  ([2,3])",
        "approach": [
            "Unlike max subarray sum, a large negative product can become the best positive product after multiplying by another negative — so track both a running max AND a running min.",
            "At each number, the new max/min are the best/worst of: the number alone, max*number, min*number.",
            "Update the global result with the running max after each step.",
        ],
        "code": '''from typing import List

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        result = nums[0]
        cur_min, cur_max = 1, 1
        for num in nums:
            candidates = (num, cur_max * num, cur_min * num)
            cur_max, cur_min = max(candidates), min(candidates)
            result = max(result, cur_max)
        return result''',
    },
    {
        "slug": "word-break",
        "number": 139,
        "title": "Word Break",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "String", "Hash Set"],
        "summary": "Check if a string can be segmented into words from a given dictionary.",
        "time": "O(n²)",
        "space": "O(n)",
        "example": 's = "leetcode", wordDict = ["leet","code"]  →  True',
        "approach": [
            "dp[i] = True if s[:i] can be fully segmented using dictionary words.",
            "dp[0] = True (empty prefix trivially segments).",
            "For each end position i, try every split point j < i: if dp[j] is True and s[j:i] is a dictionary word, then dp[i] is True.",
            "A set for the dictionary makes each substring check O(1) average.",
        ],
        "code": '''from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]''',
    },
    {
        "slug": "longest-increasing-subsequence",
        "number": 300,
        "title": "Longest Increasing Subsequence",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "Binary Search"],
        "summary": "Find the length of the longest strictly increasing subsequence.",
        "time": "O(n log n)",
        "space": "O(n)",
        "example": "nums = [10,9,2,5,3,7,101,18]  →  4  ([2,3,7,101] or [2,3,7,18])",
        "approach": [
            "Maintain 'tails': tails[k] is the smallest possible tail value of an increasing subsequence of length k+1.",
            "For each number, binary search tails for the leftmost position where it can replace an existing value (or extend the list).",
            "If it extends past the end, the LIS length grows by one; otherwise it just makes a future extension easier by lowering a tail.",
            "The final length of tails is the LIS length (the array itself may not be a real subsequence, but its length is correct).",
        ],
        "code": '''from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []
        for num in nums:
            i = bisect.bisect_left(tails, num)
            if i == len(tails):
                tails.append(num)
            else:
                tails[i] = num
        return len(tails)''',
    },
    {
        "slug": "unique-paths",
        "number": 62,
        "title": "Unique Paths",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "Matrix"],
        "summary": "Count paths from top-left to bottom-right of an m x n grid, moving only right or down.",
        "time": "O(m · n)",
        "space": "O(n)",
        "example": "m = 3, n = 7  →  28",
        "approach": [
            "The number of ways to reach a cell is the sum of ways to reach the cell above it and the cell to its left.",
            "Only one row needs to be kept in memory at a time — process row by row, updating in place left to right.",
            "The first row and first column each have exactly 1 way (straight line), which the initialization/update naturally preserves.",
        ],
        "code": '''class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        row = [1] * n
        for _ in range(m - 1):
            for c in range(1, n):
                row[c] += row[c - 1]
        return row[-1]''',
    },
    {
        "slug": "jump-game",
        "number": 55,
        "title": "Jump Game",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "Greedy", "Array"],
        "summary": "Determine if you can reach the last index, where nums[i] is the max jump length from i.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "nums = [2,3,1,1,4]  →  True",
        "approach": [
            "Work backward from the last index, tracking the leftmost index ('goal') known to be able to reach the end.",
            "For each index i (right to left), if i + nums[i] can reach the current goal, then i itself becomes the new, closer goal.",
            "If the goal is pulled all the way back to index 0, the start can reach the end.",
        ],
        "code": '''from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        goal = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0''',
    },
    {
        "slug": "combination-sum-iv",
        "number": 377,
        "title": "Combination Sum IV",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP"],
        "summary": "Count the number of ordered sequences from nums that sum to target (order matters).",
        "time": "O(target · len(nums))",
        "space": "O(target)",
        "example": "nums = [1,2,3], target = 4  →  7",
        "approach": [
            "Unlike Combination Sum, order matters here, so this is really a 'count ways to climb to target using steps of size nums[i]' problem.",
            "dp[t] = number of ways to reach exactly total t; dp[0] = 1 (one way: use nothing).",
            "For each target t from 1 upward, sum dp[t - num] over every num that fits.",
            "This naturally counts different orderings of the same numbers as distinct.",
        ],
        "code": '''from typing import List

class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        dp = [1] + [0] * target
        for t in range(1, target + 1):
            for num in nums:
                if num <= t:
                    dp[t] += dp[t - num]
        return dp[target]''',
    },
    {
        "slug": "maximum-subarray",
        "number": 53,
        "title": "Maximum Subarray",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "Array", "Greedy"],
        "summary": "Find the contiguous subarray with the largest sum (Kadane's algorithm).",
        "time": "O(n)",
        "space": "O(1)",
        "example": "nums = [-2,1,-3,4,-1,2,1,-5,4]  →  6  ([4,-1,2,1])",
        "approach": [
            "Track a running sum of the 'best subarray ending here'.",
            "If the running sum ever drops below 0, it can only hurt any future subarray — reset it to 0 before adding the next number.",
            "Update the global best after adding each number.",
        ],
        "code": '''from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        best = nums[0]
        curr = 0
        for num in nums:
            curr = max(curr, 0) + num
            best = max(best, curr)
        return best''',
    },
    {
        "slug": "longest-palindromic-substring",
        "number": 5,
        "title": "Longest Palindromic Substring",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "String", "Two Pointers"],
        "summary": "Find the longest substring of s that reads the same forward and backward.",
        "time": "O(n²)",
        "space": "O(1)",
        "example": 's = "babad"  →  "bab" (or "aba")',
        "approach": [
            "Every palindrome has a center — either one character (odd length) or between two characters (even length).",
            "For each possible center, expand outward while the characters on both sides match.",
            "Try both an odd-length expansion (center = i) and even-length expansion (center = i, i+1) for every index.",
            "Track the longest match found across all centers.",
        ],
        "code": '''class Solution:
    def longestPalindrome(self, s: str) -> str:
        best = ""

        def expand(l: int, r: int) -> str:
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1:r]

        for i in range(len(s)):
            odd = expand(i, i)
            even = expand(i, i + 1)
            best = max(best, odd, even, key=len)
        return best''',
    },
    {
        "slug": "palindromic-substrings",
        "number": 647,
        "title": "Palindromic Substrings",
        "category": "dp-1d",
        "difficulty": "Medium",
        "tags": ["DP", "String", "Two Pointers"],
        "summary": "Count how many substrings of s are palindromes.",
        "time": "O(n²)",
        "space": "O(1)",
        "example": 's = "aaa"  →  6  ("a","a","a","aa","aa","aaa")',
        "approach": [
            "Same center-expansion idea as Longest Palindromic Substring, but count every valid expansion instead of tracking only the longest.",
            "For each index, expand around it as an odd-length center and count each successful match.",
            "Also expand around it and the next index as an even-length center.",
            "Sum the counts from every center across the string.",
        ],
        "code": '''class Solution:
    def countSubstrings(self, s: str) -> int:
        count = 0

        def expand(l: int, r: int) -> int:
            c = 0
            while l >= 0 and r < len(s) and s[l] == s[r]:
                c += 1
                l -= 1
                r += 1
            return c

        for i in range(len(s)):
            count += expand(i, i)
            count += expand(i, i + 1)
        return count''',
    },

    # ---------------------------------------------------------------- Intervals
    {
        "slug": "insert-interval",
        "number": 57,
        "title": "Insert Interval",
        "category": "intervals",
        "difficulty": "Medium",
        "tags": ["Array", "Intervals"],
        "summary": "Insert a new interval into a sorted, non-overlapping list of intervals, merging as needed.",
        "time": "O(n)",
        "space": "O(n)",
        "example": "intervals = [[1,3],[6,9]], newInterval = [2,5]  →  [[1,5],[6,9]]",
        "approach": [
            "Since intervals are already sorted, copy over every interval that ends before the new one starts, unchanged.",
            "Then merge every interval that overlaps the new one, expanding newInterval's bounds to cover them all.",
            "Append the fully-merged interval once no more overlaps remain.",
            "Copy over the rest of the untouched intervals that start after the new one ends.",
        ],
        "code": '''from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        result = []
        i, n = 0, len(intervals)

        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        result.append(newInterval)

        while i < n:
            result.append(intervals[i])
            i += 1

        return result''',
    },
    {
        "slug": "merge-intervals",
        "number": 56,
        "title": "Merge Intervals",
        "category": "intervals",
        "difficulty": "Medium",
        "tags": ["Array", "Intervals", "Sorting"],
        "summary": "Merge all overlapping intervals in an unsorted list.",
        "time": "O(n log n)",
        "space": "O(n)",
        "example": "intervals = [[1,3],[2,6],[8,10],[15,18]]  →  [[1,6],[8,10],[15,18]]",
        "approach": [
            "Sort intervals by start time — this guarantees any overlap involves consecutive intervals.",
            "Walk through, keeping a 'current merged interval' (initially the first).",
            "If the next interval's start is <= the current merged interval's end, they overlap — extend the end to cover both.",
            "Otherwise, close off the current merged interval and start a new one.",
        ],
        "code": '''from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda pair: pair[0])
        result = [intervals[0]]
        for start, end in intervals[1:]:
            if start <= result[-1][1]:
                result[-1][1] = max(result[-1][1], end)
            else:
                result.append([start, end])
        return result''',
    },
    {
        "slug": "non-overlapping-intervals",
        "number": 435,
        "title": "Non-overlapping Intervals",
        "category": "intervals",
        "difficulty": "Medium",
        "tags": ["Array", "Intervals", "Greedy", "Sorting"],
        "summary": "Find the minimum number of intervals to remove so the rest don't overlap.",
        "time": "O(n log n)",
        "space": "O(1)",
        "example": "intervals = [[1,2],[2,3],[3,4],[1,3]]  →  1  (remove [1,3])",
        "approach": [
            "Sort intervals by END time — a classic greedy interval-scheduling trick.",
            "Greedily keep the interval that ends earliest, since it leaves the most room for future intervals.",
            "For each subsequent interval, if it starts before the last kept interval ends, it overlaps — remove it (increment the counter) and keep the earlier end.",
            "Otherwise keep it and update the 'last end' boundary.",
        ],
        "code": '''from typing import List

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda pair: pair[1])
        removed = 0
        prev_end = float("-inf")
        for start, end in intervals:
            if start >= prev_end:
                prev_end = end
            else:
                removed += 1
        return removed''',
    },
    {
        "slug": "meeting-rooms",
        "number": 252,
        "title": "Meeting Rooms",
        "category": "intervals",
        "difficulty": "Easy",
        "tags": ["Array", "Intervals", "Sorting"],
        "summary": "Determine if a person could attend every meeting (no time overlaps).",
        "time": "O(n log n)",
        "space": "O(1)",
        "example": "intervals = [[0,30],[5,10],[15,20]]  →  False",
        "approach": [
            "Sort meetings by start time.",
            "Walk through consecutive pairs: if a meeting starts before the previous one ends, they overlap.",
            "Any single overlap means the person can't attend all meetings.",
        ],
        "code": '''from typing import List

class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals.sort(key=lambda pair: pair[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True''',
    },
    {
        "slug": "meeting-rooms-ii",
        "number": 253,
        "title": "Meeting Rooms II",
        "category": "intervals",
        "difficulty": "Medium",
        "tags": ["Array", "Intervals", "Heap", "Sorting"],
        "summary": "Find the minimum number of meeting rooms required to host all meetings.",
        "time": "O(n log n)",
        "space": "O(n)",
        "example": "intervals = [[0,30],[5,10],[15,20]]  →  2",
        "approach": [
            "Sort meetings by start time, then simulate room usage with a min-heap of end times.",
            "For each meeting, if the earliest-ending room (heap top) is free by this meeting's start, reuse that room (replace its end time).",
            "Otherwise no existing room is free yet — allocate a new one by pushing this meeting's end time.",
            "The heap's final size is the number of rooms simultaneously in use at peak — the answer.",
        ],
        "code": '''from typing import List
import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda pair: pair[0])
        heap = []  # end times of rooms in use
        for start, end in intervals:
            if heap and heap[0] <= start:
                heapq.heapreplace(heap, end)
            else:
                heapq.heappush(heap, end)
        return len(heap)''',
    },

    # ---------------------------------------------------------------- Matrix
    {
        "slug": "rotate-image",
        "number": 48,
        "title": "Rotate Image",
        "category": "matrix",
        "difficulty": "Medium",
        "tags": ["Matrix", "Array"],
        "summary": "Rotate an n x n matrix 90 degrees clockwise, in place.",
        "time": "O(n²)",
        "space": "O(1)",
        "example": "[[1,2,3],[4,5,6],[7,8,9]]  →  [[7,4,1],[8,5,2],[9,6,3]]",
        "approach": [
            "A 90° clockwise rotation equals: transpose the matrix, then reverse each row.",
            "Transpose in place by swapping matrix[i][j] with matrix[j][i] for j > i.",
            "Then reverse every row — the combination produces the rotated result without extra space.",
        ],
        "code": '''from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            row.reverse()''',
    },
    {
        "slug": "spiral-matrix",
        "number": 54,
        "title": "Spiral Matrix",
        "category": "matrix",
        "difficulty": "Medium",
        "tags": ["Matrix", "Array"],
        "summary": "Return all elements of a matrix in spiral (clockwise, inward) order.",
        "time": "O(rows · cols)",
        "space": "O(1) extra",
        "example": "[[1,2,3],[4,5,6],[7,8,9]]  →  [1,2,3,6,9,8,7,4,5]",
        "approach": [
            "Track four shrinking boundaries: top, bottom, left, right.",
            "Walk the top row left→right, then the right column top→bottom, then (if rows remain) the bottom row right→left, then (if columns remain) the left column bottom→top.",
            "After each side, shrink the corresponding boundary inward.",
            "Repeat until the boundaries cross.",
        ],
        "code": '''from typing import List

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                result.append(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):
                result.append(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    result.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    result.append(matrix[r][left])
                left += 1

        return result''',
    },
    {
        "slug": "set-matrix-zeroes",
        "number": 73,
        "title": "Set Matrix Zeroes",
        "category": "matrix",
        "difficulty": "Medium",
        "tags": ["Matrix", "Array"],
        "summary": "If an element is 0, set its entire row and column to 0 — in place, O(1) extra space.",
        "time": "O(rows · cols)",
        "space": "O(1)",
        "example": "[[1,1,1],[1,0,1],[1,1,1]]  →  [[1,0,1],[0,0,0],[1,0,1]]",
        "approach": [
            "Use the matrix's own first row and first column as storage for 'this row/column needs zeroing' — but first remember separately whether the first row/column themselves originally contained a zero.",
            "Scan the rest of the matrix (from [1][1]): for any zero found, mark its row-flag (col 0) and column-flag (row 0).",
            "Second pass: zero out any cell whose row-flag or column-flag is set.",
            "Finally, zero the first row and/or first column if their own original flags indicated a zero.",
        ],
        "code": '''from typing import List

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        rows, cols = len(matrix), len(matrix[0])
        first_row_has_zero = any(matrix[0][c] == 0 for c in range(cols))
        first_col_has_zero = any(matrix[r][0] == 0 for r in range(rows))

        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][c] == 0:
                    matrix[r][0] = 0
                    matrix[0][c] = 0

        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][0] == 0 or matrix[0][c] == 0:
                    matrix[r][c] = 0

        if first_row_has_zero:
            for c in range(cols):
                matrix[0][c] = 0
        if first_col_has_zero:
            for r in range(rows):
                matrix[r][0] = 0''',
    },

    # ---------------------------------------------------------------- Bit Manipulation
    {
        "slug": "number-of-1-bits",
        "number": 191,
        "title": "Number of 1 Bits",
        "category": "bit-manipulation",
        "difficulty": "Easy",
        "tags": ["Bit Manipulation"],
        "summary": "Count the number of set bits (1s) in an integer's binary representation.",
        "time": "O(k) — k = number of set bits",
        "space": "O(1)",
        "example": "n = 11 (1011)  →  3",
        "approach": [
            "n & (n - 1) clears the lowest set bit of n (a well-known bit trick).",
            "Repeat that operation, counting each time, until n becomes 0.",
            "The number of iterations equals the number of set bits — faster than checking all 32 bit positions when few are set.",
        ],
        "code": '''class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1
            count += 1
        return count''',
    },
    {
        "slug": "counting-bits",
        "number": 338,
        "title": "Counting Bits",
        "category": "bit-manipulation",
        "difficulty": "Easy",
        "tags": ["Bit Manipulation", "DP"],
        "summary": "For every number 0..n, count its number of set bits.",
        "time": "O(n)",
        "space": "O(n)",
        "example": "n = 5  →  [0,1,1,2,1,2]",
        "approach": [
            "Reuse previously computed answers instead of counting bits from scratch each time.",
            "i >> 1 is i with its lowest bit dropped, and i & 1 is that dropped bit itself.",
            "So dp[i] = dp[i >> 1] + (i & 1) — the bit count of i is the bit count of i//2 plus whether i is odd.",
        ],
        "code": '''from typing import List

class Solution:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp''',
    },
    {
        "slug": "reverse-bits",
        "number": 190,
        "title": "Reverse Bits",
        "category": "bit-manipulation",
        "difficulty": "Easy",
        "tags": ["Bit Manipulation"],
        "summary": "Reverse the bits of a 32-bit unsigned integer.",
        "time": "O(1) — always 32 iterations",
        "space": "O(1)",
        "example": "n = 00000010100101000001111010011100  →  00111001011110000010100101000000",
        "approach": [
            "For each of the 32 bit positions, extract bit i of n with (n >> i) & 1.",
            "Place that bit into the mirrored position (31 - i) of the result using OR and a left shift.",
            "After all 32 positions are processed, the result is n with its bits reversed.",
        ],
        "code": '''class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        for i in range(32):
            bit = (n >> i) & 1
            result |= bit << (31 - i)
        return result''',
    },
    {
        "slug": "sum-of-two-integers",
        "number": 371,
        "title": "Sum of Two Integers",
        "category": "bit-manipulation",
        "difficulty": "Medium",
        "tags": ["Bit Manipulation"],
        "summary": "Add two integers without using the + or - operators.",
        "time": "O(1) — bounded by 32 bits",
        "space": "O(1)",
        "example": "a = 1, b = 2  →  3",
        "approach": [
            "XOR (a ^ b) adds bits without carrying; AND (a & b) shifted left by 1 gives exactly the carry bits.",
            "Repeat 'sum, carry = a^b, (a&b)<<1' until there's no carry left — this is how binary adders work.",
            "A mask limits everything to 32 bits, since Python integers don't naturally overflow like C integers.",
            "Convert back from the 32-bit unsigned representation to a signed Python int at the end.",
        ],
        "code": '''class Solution:
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        while b & mask:
            a, b = a ^ b, (a & b) << 1
        result = (a ^ b) & mask
        return result if result <= 0x7FFFFFFF else ~(result ^ mask)''',
    },
    {
        "slug": "missing-number",
        "number": 268,
        "title": "Missing Number",
        "category": "bit-manipulation",
        "difficulty": "Easy",
        "tags": ["Bit Manipulation", "Array", "Math"],
        "summary": "Find the one missing number from a range [0, n] given n distinct numbers.",
        "time": "O(n)",
        "space": "O(1)",
        "example": "nums = [3,0,1]  →  2",
        "approach": [
            "The sum of 0..n has a closed form: n * (n + 1) / 2.",
            "Subtract the actual sum of nums from the expected sum — whatever's left over is the missing number.",
            "(An XOR-based version works too: XOR every index and every value together; everything pairs off except the missing one — either approach is O(n)/O(1).)",
        ],
        "code": '''from typing import List

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        expected = n * (n + 1) // 2
        return expected - sum(nums)''',
    },
]
