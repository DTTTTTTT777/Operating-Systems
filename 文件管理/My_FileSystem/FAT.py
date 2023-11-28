#  此文件定义FAT表
#  FAT（File Allocation Table）是一种文件分配表，是文件系统中用于管理文件存储和检索的数据结构。

from BLOCK import *

class FAT:
    def __init__(self):
        self.fat=[]
        for i in range(BLOCKNUM):
            self.fat.append(-2) # -2为空闲

    def findBlank(self): # 寻找空闲的物理块
        for i in range(BLOCKNUM):
            if self.fat[i]==-2:
                return i
        return -1
    
    def write(self,data,disk): # 将数据写入磁盘
        start=-1
        cur=-1

        while data!="":
            loca=self.findBlank()
            if loca==-1:
                raise Exception(print('磁盘空间不足'))
                return
            if cur!=-1:
                self.fat[cur]=loca
            else:
                start=loca
            cur=loca
            data=disk[cur].write(data)
            self.fat[cur]=-1

        return start # 返回起始物理块的索引
        
    
    def delete(self,start,disk): # 删除文件在磁盘上的存储
        if start==-1:
            return

        while self.fat[start]!=-1:
            disk[start].clear()
            lst=self.fat[start]
            self.fat[start]=-2
            start=lst

        self.fat[start]=-2
        disk[start].clear()
    
    def update(self,start,data,disk): # 更新文件的内容
        self.delete(start, disk) # 先调用 delete 方法清空原来的文件内容和 fat 表中的链接关系
        return self.write(data, disk) # 然后调用 write 方法将新数据写入磁盘

    def read(self,start,disk): # 读取文件的内容
        data=""
        while self.fat[start]!=-1:
            data+=disk[start].read()
            start=self.fat[start]
        data+=disk[start].read()
        return data
