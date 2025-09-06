"""
Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.
"""

def maxProfit(prices):
    if len(prices) == 0:
        return 0
    
    num = prices[0]
    max_dif = 0

    for i in range(len(prices) - 1):
        if prices[i+1] < num:
            num = prices[i+1]
        else:
            if prices[i+1] - num > max_dif:
                max_dif = prices[i+1] - num
    
    return max_dif

"""Example 1:

Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:

Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.
"""
    

def merge(intervals):
    arr = []
    cur_starting = intervals[0][0]

    for i in range(len(intervals)-1):
        if intervals[i][1] >= intervals[i+1][0]:
            cur_ending = intervals[i+1][1]
            cur_interval = [cur_starting, cur_ending]
            if i == len(intervals)-2:
                arr.append([cur_starting, cur_ending])

        if intervals[i][1] < intervals[i+1][0]:
            cur_ending = intervals[i][1]
            cur_interval = [cur_starting, cur_ending]
            cur_starting = intervals[i+1][0]
            arr.append(cur_interval)
            if i == len(intervals)-2:
                arr.append(intervals[-1])

    return arr

"""print(merge([[1,3],[1,4],[1,4],[2,6],[6,7],[8,10],[11,12],[15,18],[17,20],[19,23],[24,25]]))
print(merge([[1,3],[2,6],[8,10],[15,18]]))
print(merge([[1,4],[4,5]]))
"""

def productExceptSelf(og_arr):
    def helper(index_to_skip):
        prod_so_far = 1
        for i in range(len(og_arr)):
            if i != index_to_skip:
                prod_so_far *= og_arr[i]
        return prod_so_far

    new_arr = []
    for i in range(len(og_arr)):
        new_arr.append(helper(i))

    return new_arr

"""print(productExceptSelf([1,2,3,4]))
print(productExceptSelf([-1,1,0,-3,3]))"""



def Track_Stock(prices):
    # Initialize an array to store the result, with all values set to 0
    result = [0] * len(prices)
    
    # Initialize an empty stack to store indices of the prices
    stack = []
    
    # Iterate through each day's price
    for i in range(len(prices)):
        # While the stack is not empty and the current price is greater than the price at the index on top of the stack
        while stack and prices[i] > prices[stack[-1]]:
            prev_index = stack.pop()
            # Calculate the number of days waited and store it in the result array
            result[prev_index] = i - prev_index
        
        # Push the current index onto the stack
        stack.append(i)
    
    # Return the result array
    return result

# Example usage
#prices = [100, 180, 120, 130, 150, 200, 118]
prices = [90, 120, 50, 70, 20, 80, 20]
output = Track_Stock(prices)
print(output)  # Output: [1, 0, 1, 2, 1, 0, 0]
