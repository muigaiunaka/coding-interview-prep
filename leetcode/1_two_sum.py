"""
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]
Example 3:

Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
Only one valid answer exists.
 

Follow-up: Can you come up with an algorithm that is less than O(n2) time complexity?
"""

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Examples
        nums = [2,7,11,15], target = 9 --> [0,1]
        nums = [3,2,4], target = 6 --> [1,2]
        nums = [3,3], target = 6 --> [0,1]
        nums = [], target = 6 --> []
        nums = [1], target = 6 --> []
        nums = [1,7,-4, 13], target = 6 --> [2,3]
        nums = [-4,-5,-9,-13], target = 6 --> []
        nums = [0,0,0], target = 6 --> []
        nums = [3,3,3,3,3], target = 6 --> [0,1]
        nums = [-3,-4,-2], target = -6 --> [1, 2]

        Clarify
        - can there be negative integers values? (Yes)
        - can the integers in the array be duplicates? (Yes)
        - can the target be a negative integer? (Yes)
        - can we expect the input array to contain float values? (No)
        
        Approach
        Hash Map
        - Use a hash map to store the value in the array subtracted from the target
        - loop through array and store [target-nums[i]] = i
        - if key in map equals current value, return value from map and current index
        - else set [target-num] = i
        T: N for iterating through each number in worst case
        S: N filling up a dictionary for every num in worst case

        Trade-offs
        - utilizes extra space
        - linear time complexity scales up to input size of 10 million, if larger, the algo will be slow
        """
        diff = {}
        for i, num in enumerate(nums):
            if num in diff:
                return [diff[num], i]
            else:
                diff[target-num] = i # store complement : index
        return []
