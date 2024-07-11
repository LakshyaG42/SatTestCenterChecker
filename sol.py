import math
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        m = len(nums1)
        n = len(nums2)
        isEven = (m + n) % 2 == 0
        newarr = []
        pointer1 = 0
        pointer2 = 0
        index = 0
        print(math.ceil((m + n) / 2))
        print((ceil((m+n)/2)+1))
        print(isEven)
        if isEven:
            limit = math.ceil((m + n) / 2)
        else:
            limit = math.ceil((m + n) / 2) - 1
        print(limit)
        while (pointer1 < m or pointer2 < n) and index <= limit :
            print(f"Iteration: {index}")
            if (pointer1 < m and pointer2 < n):
                if nums1[pointer1] < nums2[pointer2]:
                    newarr.append(nums1[pointer1])
                    index += 1
                    pointer1 += 1
                else:
                    newarr.append(nums2[pointer2])
                    index += 1
                    pointer2 += 1
            else:
                if pointer1 < m:
                    newarr.append(nums1[pointer1])
                    index += 1
                    pointer1 += 1
                if pointer2 < n:
                    newarr.append(nums2[pointer2])
                    index += 1
                    pointer2 += 1

            
        print(newarr)
        if isEven == True:
            return ((newarr[len(newarr)-1]+newarr[len(newarr)-2])/2)
        else:
            return newarr[len(newarr)-1]