from collections import defaultdict
from queue import Queue
import bisect

class FileSystem:
    
    DIR_MAX_ELEMS: int
    MAX_BUF_FILE_SIZE: int

    def __init__(self, max_elems: int, max_buf_file_size: int):
        self.DIR_MAX_ELEMS = max_elems
        self.MAX_BUF_FILE_SIZE = max_buf_file_size
        
        self.paths = defaultdict(list)
        self.binfiles = defaultdict(str)
        self.logfiles = defaultdict(str)
        self.buffiles = defaultdict(Queue)
    
    def ls(self, path: str) -> list[str]: 
        if path.endswith(".bin") or path.endswith(".log") or path.endswith(".buf"):
            return [path.split("/")[-1]]
        else:
            return self.paths[path]

    def mkdir(self, path: str) -> bool:
        if ".bin" in path or ".log" in path or ".buf" in path:
            print("Incorrect path")
            return False
        if self.check_ancestor_dir(path):
            self.paths[path]
            return True
        else:
            return False

    def check_ancestor_dir(self, path: str) -> bool:
        if ".bin" in path or ".log" in path or ".buf" in path:
            print("Incorrect path")
            return False
        directories = path.split("/")

        for i in range(1, len(directories)):
            cur = "/".join(directories[:i]) or "/"

            if cur not in self.paths or directories[i] not in self.paths[cur]:
                if len(self.paths[cur]) < self.DIR_MAX_ELEMS:
                    bisect.insort(self.paths[cur], directories[i])
                else:
                    print("Directory is full")
                    return False
        return True
    
    def delete_directory(self, path: str) -> bool:
        if path in self.paths:
            l = self.ls(path)
            if len(l) == 0:
                dirs = path.split("/")
                parent_dir = "/".join(dirs[:-1])
                
                self.paths[parent_dir].remove(dirs[len(dirs) - 1])
                self.paths.pop(path)
                return True
            else:
                print("Cannot delete non-empty directory")
                return False
        else:
            print("There is no such directory")
            return False

    def move_directory(self, path: str, pathTo: str) -> bool:
        if (path in self.paths):
            dirs = path.split("/")
            name = dirs[len(dirs) - 1]

            if name not in self.paths[pathTo]:
                if len(self.paths[pathTo]) < self.DIR_MAX_ELEMS:
                    self.delete_directory(path)
                    pathTo_name = pathTo + "/" + name
                    self.mkdir(pathTo_name)
                    return True
                else:
                    print("Directory is full")
                    return False
            else:
                print("Directory with such name already exists")
                return False
        else:
            print("Directory doesn't exist")
            return False

    
    def create_binary_file(self, path: str, fileName: str) -> bool:
        if (fileName.endswith(".bin")):
            if path != "/":
                if self.check_ancestor_dir(path):
                    if fileName not in self.paths[path]:
                        #self.binfiles.pop(path)
                        if len(self.paths[path]) < self.DIR_MAX_ELEMS:
                            filePath = path + "/" + fileName
                            bisect.insort(self.paths[path], fileName)
                            self.binfiles[filePath] = "Just a bin file."
                            return True
                        else:
                            print("Directory is full")
                            return False
                    else:
                        print("File already exists")
                        return False
                else:
                    return False
            else:
                print("Create a directory first")
                return False
        else: 
            print("Incorrect file name")
            return False

    def delete_binary_file(self, filePath: str) -> bool:
        if (filePath in self.binfiles):
            directories = filePath.split("/")
        
            dirpath = "/".join(directories[:-1])
            self.paths[dirpath].remove(directories[len(directories)-1])
            self.binfiles.pop(filePath)
            return True
        else:
            print("File doesn't exist")
            return False

    def read_binary_file(self, filePath: str) -> str:
        if filePath in self.binfiles:
            return self.binfiles[filePath]
        else:
            print("File doesn't exist")
            return None
        

    def move_binary_file(self, filePath: str, pathTo: str) -> bool:
        if (filePath in self.binfiles):
            dirs = filePath.split("/")
            fileName = dirs[len(dirs) - 1]

            if fileName not in self.paths[pathTo]:
                #self.binfiles.pop(pathTo)
                if len(self.paths[pathTo]) < self.DIR_MAX_ELEMS:
                    self.delete_binary_file(filePath)
                    self.create_binary_file(pathTo, fileName)
                    return True
                else:
                    print("Directory is full")
                    return False
            else:
                print("File with such name already exists")
                return False
        else:
            print("File doesn't exist")
            return False


    def create_log_file(self, path: str, fileName: str) -> bool:
        if (fileName.endswith(".log")):
            if path != "/":
                if self.check_ancestor_dir(path):
                    if fileName not in self.paths[path]:
                        #self.logfiles.pop(path)
                        if len(self.paths[path]) < self.DIR_MAX_ELEMS:
                            filePath = path + "/" + fileName
                            bisect.insort(self.paths[path], fileName)
                            self.logfiles[filePath] = ""
                            return True
                        else:
                            print("Directory is full")
                            return False
                    else:
                        print("File already exists")
                        return False
                else:
                    return False
            else:
                print("Create a directory first")
                return False
        else: 
            print("Incorrect file name")
            return False

    def delete_log_file(self, filePath: str) -> bool:
        if (filePath in self.logfiles):
            directories = filePath.split("/")
        
            dirpath = "/".join(directories[:-1])
            self.paths[dirpath].remove(directories[len(directories)-1])
            self.logfiles.pop(filePath)
            return True
        else:
            print("File doesn't exist")
            return False

    def append_text(self, filePath: str, text: str) -> bool:
        if filePath not in self.logfiles:
            dirs = filePath.split("/")
            fileName = dirs[len(dirs) - 1]
            dirpath = "/".join(dirs[:-1])
            b = self.create_log_file(dirpath, fileName)
            if b == False:
                return False
        
        if self.logfiles[filePath] != "":
            self.logfiles[filePath] += "\n\r"
        self.logfiles[filePath] += text
        if text in self.logfiles[filePath]:
            return True
        else:
            print("Something went wrong")
            return False

    def read_log_file(self, filePath: str) -> str:
        if filePath in self.logfiles:
            return self.logfiles[filePath]
        else:
            print("File doesn't exist")
            return None

    def move_log_file(self, filePath: str, pathTo: str) -> bool:
        if (filePath in self.logfiles):
            dirs = filePath.split("/")
            fileName = dirs[len(dirs) - 1]

            if fileName not in self.logfiles[pathTo]:
                #self.logfiles.pop(pathTo)
                text = self.logfiles[filePath]

                if len(self.paths[pathTo]) < self.DIR_MAX_ELEMS:
                    self.delete_log_file(filePath)
                    self.create_log_file(pathTo, fileName)

                    newFilePath = pathTo + "/" + fileName
                    self.append_text(newFilePath, text)
                    return True
                else:
                    return False
            else:
                print("File with such name already exists")
                return False
        else:
            print("File doesn't exist")
            return False


    
    def create_buf_file(self, path: str, fileName: str) -> bool:
        if (fileName.endswith(".buf")):
            if path != "/":
                if self.check_ancestor_dir(path):
                    if fileName not in self.paths[path]:
                        #self.buffiles.pop(path)
                        if len(self.paths[path]) < self.DIR_MAX_ELEMS:
                            filePath = path + "/" + fileName
                            bisect.insort(self.paths[path], fileName)
                            self.buffiles[filePath] = Queue(maxsize = self.MAX_BUF_FILE_SIZE)
                            return True
                        else:
                            print("Directory is full")
                            return False
                    else:
                        print("File already exists")
                        return False
                else:
                    return False
            else:
                print("Create a directory first")
                return False
        else: 
            print("Incorrect file name")
            return False

    def delete_buf_file(self, filePath: str) -> bool:
        if (filePath in self.buffiles):
            directories = filePath.split("/")
        
            dirpath = "/".join(directories[:-1])
            self.paths[dirpath].remove(directories[len(directories)-1])
            self.buffiles.pop(filePath)
            return True
        else:
            print("File doesn't exist")
            return False

    def push_to_buf_file(self, filePath: str, elem) -> bool:
        if filePath not in self.buffiles:
            dirs = filePath.split("/")
            fileName = dirs[len(dirs) - 1]
            dirpath = "/".join(dirs[:-1])
            b = self.create_buf_file(dirpath, fileName)
            if b == False:
                return False
        if self.buffiles[filePath].full() == False:
            self.buffiles[filePath].put(elem)
            return True
        else:
            print("Queue is full")
            return False


    def consume_from_buf_file(self, filePath: str):
        if filePath not in self.buffiles:
            print("File doesn't exist")
            return False
        elif self.buffiles[filePath].empty() == True:
            print("Queue is empty")
            return False
        else:
            return self.buffiles[filePath].get()
    
    def move_buf_file(self, filePath: str, pathTo: str) -> bool:
        if (filePath in self.buffiles):
            dirs = filePath.split("/")
            fileName = dirs[len(dirs) - 1]

            if fileName not in self.paths[pathTo]:
                if len(self.paths[pathTo]) < self.DIR_MAX_ELEMS:
                    self.delete_buf_file(filePath)
                    self.create_buf_file(pathTo, fileName)
                    return True
                else:
                    print("Directory is full")
                    return False
            else:
                print("File with such name already exists")
                return False
        else:
            print("File doesn't exist")
            return False


fs = FileSystem(5, 5)
fs.mkdir("/maindir")
fs.mkdir("/maindir/projects")
fs.mkdir("/maindir/university")

fs.create_binary_file("/maindir/projects", "just_a_binfile.bin")
fs.create_log_file("/maindir/projects", "my_qa_lab.log")

fs.append_text("/maindir/projects/my_qa_lab.log", "Artem\n\rKononenko")
fs.append_text("/maindir/projects/my_qa_lab.log", "KP-03")
fs.append_text("/maindir/projects/my_qa_lab.log", "lab is done")

fs.create_buf_file("/maindir/university", "buffile.buf")
fs.push_to_buf_file("maindir/university/buffile.buf", 1)
fs.push_to_buf_file("maindir/university/buffile.buf", "some string")
fs.push_to_buf_file("maindir/university/buffile.buf", False)

print("Text in this file:\n\r" + fs.read_log_file("/maindir/projects/my_qa_lab.log"))

print()
print(fs.consume_from_buf_file("maindir/university/buffile.buf"))
print(fs.consume_from_buf_file("maindir/university/buffile.buf"))
print(fs.consume_from_buf_file("maindir/university/buffile.buf"))

fs.mkdir("/maindir/emptydir")
print(fs.ls("/maindir"))
fs.delete_directory("/maindir/emptydir")
print(fs.ls("/maindir"))

fs.mkdir("/maindir/dirtomove")
print(fs.ls("/maindir"))
fs.move_directory("/maindir/dirtomove", "/maindir/projects")
print(fs.ls("/maindir"))
print(fs.ls("/maindir/projects"))

fs.mkdir("/maindir")
