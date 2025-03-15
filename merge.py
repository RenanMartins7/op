#Merge Sort implementation for mocked services in api
def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

def merge_sort(randomList):
    mergeList = list(randomList)
    n = len(mergeList)

    if len(mergeList) <= 1:
        return mergeList

    middle = int(len(mergeList) / 2)
    left = merge_sort(mergeList[:middle])
    right = merge_sort(mergeList[middle:])

    return merge(left, right) 

