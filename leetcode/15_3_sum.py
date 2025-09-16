"""
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

 

Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.
Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.
Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.
 

Constraints:

3 <= nums.length <= 3000
-105 <= nums[i] <= 105
"""
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Examples
        nums = [-1,0,1,2,-1,-4] --> [[-1,-1,2],[-1,0,1]]
        nums = [0,1,1] --> []
        nums = [0,0,0] --> [[0,0,0]]
        nums = [] --> []
        
        Clarify
        - can there be negative values in array? (yes)
        - can we expect float values in array? (no)

        Approach
        1. Triple Nested Loop - Brute Force
        - triple nested loop
        - set output equal to set
        - compare each index to ensure not equal, if combination equals 0, add to output
        - sort array before adding and compare against each sorted array inside of output already? can't use set with array

        2. Intuitive with Combinations (doesn't work)
        - create each combination of size 3
        - check if sum of combination is 0, if so, add to output array
        - return output
        T: O(r * n/r) with n being the nums array size and r being the constant 3
        S: O(1)

        Tradeoffs
        - This handles most cases well but fails for duplicates in the input array

        - use set for no duplicates, iterate through set to create array output
        [-4,-1,-1,-0,1,2]

        3. Two Pointers
        - sort array (if you sort and smallest number is 1, nothing can sum to zero)
        - iterate through array
        - if current value > 0, break from loop (remaining values cannot sum to zero)
        - if current value is same as one before, skip it
        - else call TwoSumII for current position i

        - create helper function (TwoSumII) that sets lo to i+1, hi to last index
        - while lo is smaller than hi:
            - if sum nums[i] + nums[lo] + nums[hi] < 0, increment lo
            - if greater than 0, decrement hi
            - else, add to result decrement hi, increment lo and increment lo while next value is same as before to avoid dupes
        """
        # import itertools
        # output = []
        # combos = itertools.combinations(nums, 3)
        # for i, combo in enumerate(combos):
        #     if sum(combo) == 0:
        #         output.append(combo)
        # return output
        output = []
        nums.sort()
        for i in range(len(nums)):
            if nums[i] > 0:
                break
            if i == 0 or nums[i-1] != nums[i]:
                self.twoSumII(nums, i, output)
        return output

    def twoSumII(self, nums: list[int], i: int, output: list[list[int]]):
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            sum = nums[i] + nums[lo] + nums[hi]
            if sum < 0:
                lo += 1
            elif sum > 0:
                hi -= 1
            else:
                output.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo +=1
        
