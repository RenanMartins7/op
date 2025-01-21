#selection sort implementation to the mocked services

def selection_sort(randomList):
   
    selection_list = list(randomList)
    n = len(selection_list)

    for i in range(n):
        smallest_index = i
        for j in range(i + 1, n):
            if selection_list[j] < selection_list[smallest_index]:
                smallest_index = j
        selection_list[i], selection_list[smallest_index] = (
            selection_list[smallest_index],
            selection_list[i],
        )

    return selection_list