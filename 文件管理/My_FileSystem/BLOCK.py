#  此文件定义磁盘的物理块

BLOCKSIZE=512 # 单个物理块大小
BLOCKNUM=512 # 磁盘中物理块个数

class Block:
    def __init__(self,blockIndex:int,data=""):
        self.blockIndex=blockIndex # 物理块的编号
        self.data=data # 存储的数据

    def read(self): # 从物理块中读取数据
        return self.data

    def write(self,newData:str): # 向物理块写入新的数据，返回无法写入的内容
        self.data=newData[:BLOCKSIZE]
        return newData[BLOCKSIZE:]

    def append(self,newData:str)->str: # 向物理块追加新的内容，返回无法写入的内容
        remainSpace=BLOCKSIZE-len(self.data)
        if remainSpace>=newData:
            return ""
        else:
            self.data+=newData[:remainSpace]
            return newData[remainSpace:]

    def isFull(self): # 检查物理块是否已满
        return len(self.data)==BLOCKSIZE

    def clear(self):
        self.data=""
