import os

path = "res"

dir_list = os.listdir(path)

print("Files and directories in '", path, "' :")


# prints all files
print(dir_list)
for file in dir_list:
    f = open(path+'/'+file, 'r')
    print(file)
    for line in f.readlines():
        print(line)
    break
