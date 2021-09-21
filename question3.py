import copy
pascal_list = []

def generate_pascal(n):
    if n == 0:
        pascal_list.append([1])
        return pascal_list

    pascal_list.append([1])
    if n == 1:
        pascal_list.append([1,1])
        return pascal_list
    pascal_list.append([1,1])
    for i in range(2,n+1):
        #avoid alias
        layer_list = copy.deepcopy(pascal_list[-1])
        temp_list = [1,1]
        #generating next layer
        for t in range(len(layer_list)-1):
            temp_list.insert(-1,layer_list[t]+layer_list[t+1])
        pascal_list.append(temp_list)
    return pascal_list
print(generate_pascal(5))
#output
# [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]]
