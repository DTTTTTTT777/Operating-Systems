#  此文件定义 FCB
#  FCB: File Control Block，是用于管理文件的原数据和文件操作的数据结构，每个文件在文件系统中都对应唯一的FCB。

from FAT import *

class FCB:
    def __init__(self,name,createTime,data,fat,disk):
        self.name=name # 文件名
        self.createTime=createTime # 创建时间
        self.updateTime=self.createTime # 最后修改时间
        self.start=-1 # 起始位置
    
    def update(self,newData,fat,disk): # 更新文件的内容
        self.start=fat.update(self.start,newData,disk) # 调用文件分配表（FAT）对象的update方法来更新文件的存储空间。
    
    def delete(self,fat,disk): # 删除文件
        fat.delete(self.start,disk) # 调用文件分配表（FAT）对象的delete方法来释放文件占用的物理块空间
    
    def read(self,fat,disk): # 读取文件的内容
        if self.start==-1:
            return ""
        else:
            return fat.read(self.start,disk) # 调用文件分配表（FAT）对象的read方法，从磁盘中读取文件的

