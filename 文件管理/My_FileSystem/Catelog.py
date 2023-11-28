#  此文件定义多级目录结点（CatalogNode）

from FCB import *

class CatalogNode: # 多级目录结点
    def __init__(self,name,isFile,fat,disk,createTime,parent=None,data=""):
        self.name=name # 路径名，用于标识目录结点的名称。
        self.isFile=isFile # 是否为文件类型的标志，如果为True，则表示该目录结点为文件；如果为False，则表示该目录结点为文件夹。
        self.parent=parent # 父结点，表示该目录结点的父级目录结点。
        self.createTime=createTime # 创建时间
        self.updateTime=self.createTime # 更新时间


        if not self.isFile: # 文件类型
            self.children=[]
        else: # 文件夹类型
            self.data=FCB(name, createTime, data, fat, disk)
    
        