"""
You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

 

Example 1:


Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
Example 2:

Input: height = [1,1]
Output: 1
"""
class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        Examples
        height = [1,8,6,2,5,4,8,3,7] --> 49
        height = [1,1] --> 1

        Clarify
        - can there be negative vertical lines? (assume no)
        max water = (Bx - Ax) * min(By, Ay) if A and B are the highest points that are also furthest apart
        
        Approach
        Two Pointer
        - instantiate two pointers, left and right to 0 and len(arr) - 1
        - instantiate output to really small number
        - calculate new output if current container size is bigger
        - if value at right index of array is less than value at left, increment left, else decrement right
        T: O(N)
        S: O(1)
        
        """
        left, right = 0, len(height) - 1
        output = float('-inf')
        while left <= right:
            max_container = (right - left) * min(height[right], height[left])
            if output < max_container:
                output = max_container
            elif height[right] > height[left]:
                left += 1
            else:
                right -= 1
        return output


        
        
