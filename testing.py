def my_lamb(data, left, right):
    ret = data[left]
    while left < right:
        while data[left] < ret:
            left += 1
        while data[right] > ret:
            right -= 1

        data[left], data[right] = data[right], data[left]

    data[left] = ret
    return left


def my_func(data, left, right):
    mid = my_lamb(data, left, right)
    my_lamb(data, left, mid - 1)
    my_lamb(data, mid + 1, right)


li = [3, 2, 8, 4, 6, 1, 9, 45, 194]
my_func(li, 0, len(li) - 1)

print(li)


