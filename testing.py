# def my_lamb(data, left, right):
#     ret = data[left]
#     while left < right:
#         while data[left] < ret:
#             left += 1
#         while data[right] > ret:
#             right -= 1
#
#         data[left], data[right] = data[right], data[left]
#
#     data[left] = ret
#     return left
#
#
# def my_func(data, left, right):
#     mid = my_lamb(data, left, right)
#     my_lamb(data, left, mid - 1)
#     my_lamb(data, mid + 1, right)

#
# li = [3, 2, 8, 4, 6, 1, 9, 45, 194]
# my_func(li, 0, len(li) - 1)
#
# print(li)


# def binary_serach(data, val):
#     left = 0
#     right = len(data)-1
#
#     while left <= right:
#         mid = (left + right) // 2
#         if data[mid] == val:
#             return mid
#         elif data[mid] > val:
#             right = mid - 1
#         elif data[mid] < val:
#             left = mid + 1
#
# li = [1,2,3,4,5,6,7,8,9]
#
# print(binary_serach(li, 9))

def top_serach(data):
    for i in range(len(data)-1):  # i表示每一趟
        for j in range(len(data)-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]  # 相邻的互换

