original_list = ['sdf', 'sdfsdf', 'sdfsdf', 'sdfsdf']
appended_list = [list(element).append('x') for element in original_list]

arrraguments_list = []
for x in original_list:
    arrraguments_list.append([x])

print(arrraguments_list)