# by dttttttt 2023/5
import sys
import time
from functools import partial

from PyQt5.QtCore import QThread, pyqtSignal, Qt, QMutex, QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Elevator_Window(QWidget):  # 主窗口

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        whole_layout = QHBoxLayout()  #  创建的是水平布局，该布局会将添加到其中的控件横向排列，可以使用 addWidget() 方法将控件添加到该布局中。
        grid_elevator_external = QGridLayout() #创建的是网格布局，该布局会将添加到其中的控件按照行和列的方式排列，可以使用 addWidget() 方法将控件添加到该布局中。使用该布局时，需要指定控件所在的行和列。
        grid_elevator_internal = QGridLayout()

        # grid_elevator_internal 是 左侧界面（电梯里） 的布局管理器
        # grid_elevator_external 是 右侧界面（电梯外） 的布局管理器

        grid_elevator_internal.setSpacing(1) # 设置布局中控件之间的间距
        grid_elevator_external.setSpacing(1) # 设置布局中控件之间的间距

        widget_left = QWidget()  # 创建空部件
        widget_right = QWidget()
        widget_left.setLayout(grid_elevator_internal)  # 将grid_elevator_internal部件设置局部布局
        widget_right.setLayout(grid_elevator_external)
        whole_layout.addWidget(widget_left)  # 使用 addWidget() 方法将部件添加到全局布局中，使它们按照水平布局管理器 whole_layout 的规则排列
        whole_layout.addWidget(widget_right)

        self.setLayout(whole_layout)  # 设置全局布局


        floor_name = [('%s' % i) for i in range(1, 21)]  # 电梯按钮编号
        floor_button_positions = [(10 - i, j) for j in range(2) for i in range(10)]  # 位置

        button_up = [('▲') for i in range(1, 21)]
        button_down = [('▼') for i in range(1, 21)]

        #下面是左边（电梯内部按钮）布局-------------------------------------------------------------------------------

        for i in range(5):
            self.label_floor = QLabel()  # 电梯内部显示楼层
            self.label_floor.setObjectName("Floor{0}".format(i + 1))
            grid_elevator_internal.addWidget(self.label_floor, 0, 4 * i, 2, 2)
            self.space = QLabel(self)  # 为了增加缝隙
            grid_elevator_internal.addWidget(self.space, 0, 4 * i + 2, 15, 1)
            self.label_floor.setStyleSheet("color: #FFE6E6; background-color: #9783AA")
            self.label_floor.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
            self.label_floor.setAlignment(Qt.AlignCenter)

        for i in range(5):
            j = 1
            for position, name in zip(floor_button_positions, floor_name):
                if name == '':
                    continue
                self.button = QPushButton(name) #通过QPushButton类创建一个按钮实例，名字为name。
                self.button.setFixedSize(60, 60)  # 设置按钮的宽度和高度相等
                self.button.setFont(QFont("Comic Sans MS", 11, QFont.Bold)) #使用setFont方法设置按钮的字体为“Microsoft YaHei”（微软雅黑），大小为12。
                self.button.setObjectName("{0}+{1}".format(i + 1, j)) #使用setObjectName方法设置按钮的对象名为“{0}+{1}”。其中，{0}表示第一个循环的当前迭代次数加1，{1}表示第二个循环的当前迭代次数加1。这里的对象名将在后续的事件处理中用到。
                self.button.setStyleSheet("background-color: #FACBCB")

                self.button.clicked.connect(partial(Set_Elevator_Goal_Internal, i + 1, j)) #使用clicked信号连接Set_Elevator_Goal_Internal函数，传递参数为第一个循环的当前迭代次数加1和第二个循环的当前迭代次数加1。这里使用了partial函数来创建一个函数对象，用于延迟调用Set_Elevator_Goal_Internal函数并传递参数。
                j = j + 1
                grid_elevator_internal.addWidget(self.button, position[0] + 2, position[1] + i * 4)

        for i in range(grid_elevator_internal.rowCount()):
            grid_elevator_internal.setRowMinimumHeight(i, 60)

        # 门显示在下面的label上
        for i in range(5):
            self.label = QLabel()
            self.label.setObjectName("open{0}".format(i + 1))
            self.label.setMinimumHeight(80)
            self.label.setStyleSheet("background-image: url(door_close.jpg);background-position: center")#;background-size: 50%")
            label_space = QLabel(self)
            grid_elevator_internal.addWidget(label_space, 13, 4 * i, 1, 2)
            grid_elevator_internal.addWidget(self.label, 13 + 1, 4 * i, 1, 2)

        # pause按钮
        for i in range(5):
            self.button = QPushButton("Pause")
            self.button.setFont(QFont("Comic Sans MS", 12))
            self.button.setStyleSheet("background-color: #FFF2CC")
            self.button.setObjectName("pause{0}".format(i + 1))
            self.button.setMinimumHeight(40)
            self.button.clicked.connect(partial(Elevator_Pause, i + 1))  # 将暂停按钮连接到pause函数
            label_space = QLabel(self)
            grid_elevator_internal.addWidget(label_space, 13 + 2, 0, 1, 2)
            grid_elevator_internal.addWidget(self.button, 13 + 3, 4 * i, 1, 2)

        #下面是右边布局（电梯外部按钮）----------------------------------------------------------------------------

        for i in range(1, 21):
            label = QLabel("F" + str(i)+"  ")
            label.setAlignment(Qt.AlignCenter)
            font = QFont("Comic Sans MS", 10)
            font.setBold(True)
            label.setFont(font)
            grid_elevator_external.addWidget(label, 21 - i, 0)

        num_i = 0
        for i in button_up:
            if num_i == 19:
                break
            self.button = QPushButton(i)
            self.button.setFont(QFont("Comic Sans MS",7))
            self.button.setObjectName("up{0}".format(num_i + 1))
            self.button.setMinimumHeight(42)
            self.button.setFixedWidth(42)
            self.button.setStyleSheet("background-color: #FACBCB")
            self.button.clicked.connect(partial(Set_Elevator_Goal_External_Up, num_i + 1))
            grid_elevator_external.addWidget(self.button, 20 - num_i, 3)   # 在这个循环中，按钮在第 20-num_i 行、第 0 列。
            num_i = num_i + 1

        num_i = 0
        for i in button_down:
            if num_i == 0:
                num_i = num_i + 1
                continue
            self.button = QPushButton(i)
            self.button.setFont(QFont("Comic Sans MS",9))
            self.button.setObjectName("down{0}".format(num_i + 1))
            self.button.setMinimumHeight(42)
            self.button.setFixedWidth(42)
            self.button.setStyleSheet("background-color: #FACBCB")
            self.button.clicked.connect(partial(Set_Elevator_Goal_External_Down, num_i + 1))
            grid_elevator_external.addWidget(self.button, 20 - num_i, 5)
            num_i = num_i + 1

        # ui其他设置------------------------------------------------------------------------------------------------------------------------
        self.setStyleSheet("background-color: #FFE6E6")
        self.setWindowTitle('Elevator-Dispatching Project by 2152402_段婷婷')
        self.move(100, 100)
        self.show()

class Elevator_Thread(QThread):

    update_signal = pyqtSignal(int) # 信号
    open_signal = pyqtSignal(int, int)

    def __init__(self, elevator_num):
        super(Elevator_Thread, self).__init__()
        self.int = elevator_num
        self.update_signal.connect(Elevator_Update)
        self.open_signal.connect(Open_Door)

    def run(self):
        while (1):

            self.update_signal.emit(self.int)

            time.sleep(1)#每一秒更新一次电梯状态

            if open_door[self.int - 1] == 1:

                #下面是开门动画
                self.open_signal.emit(0, self.int) #不能直接在此处修改样式表，会闪烁，需要用信号处理
                time.sleep(0.2)
                self.open_signal.emit(1, self.int)
                time.sleep(0.5)
                self.open_signal.emit(0, self.int)
                time.sleep(0.2)
                self.open_signal.emit(2, self.int)
                time.sleep(0.5)

                open_door[self.int - 1] = 0

def Open_Door(type, elevator_num):
    if type == 0:
        My_Elevator_Window.findChild(QLabel, "open{0}".format(elevator_num)).setStyleSheet(
            "QLabel{background-image: url(door_half.jpg);background-position: center}")
    elif type == 1:
        My_Elevator_Window.findChild(QLabel, "open{0}".format(elevator_num)).setStyleSheet(
            "QLabel{background-image: url(door_open.jpg);background-position: center}")
    elif type == 2:
        My_Elevator_Window.findChild(QLabel, "open{0}".format(elevator_num)).setStyleSheet(
            "QLabel{background-image: url(door_close.jpg);background-position: center}")

def Elevator_Update(elevator_num_1):

    elevator_num = elevator_num_1 - 1

    if pause[elevator_num] == 0:  #电梯被暂停了，不需要更新状态
        return

    if state[elevator_num] == -1:  #电梯要向下运行
        floor[elevator_num] -= 1
    elif state[elevator_num] == 1:  #电梯是向上运行的
        floor[elevator_num] += 1

    # 下面讨论当前需要开门的情况--------------------------------------------------------------------------------------------------------------------------------------------
    if floor[elevator_num] in elevator_goal_internal[elevator_num]:  #现在电梯到达了一个内部按下的目标层
        open_door[elevator_num] = 1
        My_Elevator_Window.findChild(QPushButton, "{0}+{1}".format(elevator_num_1, floor[elevator_num])).setStyleSheet(
            "QPushButton{background-color: #FACBCB}") #移除电梯内部的标识
        elevator_goal_internal[elevator_num].discard(floor[elevator_num])

    if elevator_goal_total[elevator_num]: # 如果有目标层才可能需要开门
    #若电梯到达一个外部按下的目标层，而且方向一致(向上)
        if (state[elevator_num] == 1 or min(elevator_goal_total[elevator_num]) >= floor[elevator_num]) \
                and floor[elevator_num] in elevator_goal_external_up[elevator_num] :
            open_door[elevator_num] = 1
            My_Elevator_Window.findChild(QPushButton, "up{0}".format(floor[elevator_num])).setStyleSheet(
                "QPushButton{background-color: #FACBCB}")
            elevator_goal_external_up[elevator_num].discard(floor[elevator_num])
            external_up.discard(floor[elevator_num])
        # 若电梯到达一个外部按下的目标层，而且方向一致(向下)
        if (state[elevator_num] == -1 or max(elevator_goal_total[elevator_num]) <= floor[elevator_num]) \
                and floor[elevator_num] in elevator_goal_external_down[elevator_num] :
            open_door[elevator_num] = 1
            My_Elevator_Window.findChild(QPushButton, "down{0}".format(floor[elevator_num])).setStyleSheet(
                "QPushButton{background-color: #FACBCB}")
            elevator_goal_external_down[elevator_num].discard(floor[elevator_num])
            external_down.discard(floor[elevator_num])
        # 若电梯是静止的，但是外部按下了该楼层，也是要开门的
        if state[elevator_num] == 0:
            if floor[elevator_num] in elevator_goal_external_up[elevator_num]:
                open_door[elevator_num] = 1
                My_Elevator_Window.findChild(QPushButton, "up{0}".format(floor[elevator_num])).setStyleSheet(
                    "QPushButton{background-color: #FACBCB}")
                elevator_goal_external_up[elevator_num].discard(floor[elevator_num])
                external_up.discard(floor[elevator_num])
            elif floor[elevator_num] in elevator_goal_external_down[elevator_num]:
                open_door[elevator_num] = 1
                My_Elevator_Window.findChild(QPushButton, "down{0}".format(floor[elevator_num])).setStyleSheet(
                    "QPushButton{background-color: #FACBCB}")
                elevator_goal_external_down[elevator_num].discard(floor[elevator_num])
                external_down.discard(floor[elevator_num])

        elevator_goal_total[elevator_num] = elevator_goal_internal[elevator_num].union(elevator_goal_external_up[elevator_num]).union(elevator_goal_external_down [elevator_num])

    goal_internal_list = list(elevator_goal_internal[elevator_num])
    goal_list = list(elevator_goal_internal[elevator_num].union(elevator_goal_external_up[elevator_num]).union(elevator_goal_external_down [elevator_num]))

    # 下面更新电梯的状态state-----------------------------------------------------------------------------------------------
    if len(goal_list) == 0: #没有目标楼层了
        state[elevator_num] = 0
    elif state[elevator_num] == 0: #当前是不动的，随便选一个目标楼层的方向移动，优先去内部按的
        to_floor = 1
        if len(goal_internal_list) != 0:
            to_floor = goal_internal_list[0]
        else:
            to_floor = goal_list[0]
        if to_floor > floor[elevator_num]:
            state[elevator_num] = 1
        else:
            state[elevator_num] = -1
    elif state[elevator_num] == 1: # 目前是往上走，那么看看上面有没有楼层需要
        tag = 0
        for to_floor in goal_list :
            if to_floor > floor[elevator_num]:
                tag = 1
                break
        if tag == 0:
            state[elevator_num] = -1
    else:
        tag = 0
        for to_floor in goal_list:
            if to_floor < floor[elevator_num]:
                tag = 1
                break
        if tag == 0:
            state[elevator_num] = 1

    label_floor = My_Elevator_Window.findChild(QLabel, "Floor{0}".format(elevator_num_1))

    if state[elevator_num] == -1:  # 电梯要向下运行
        label_floor.setText("↓" + str(floor[elevator_num]))
    elif state[elevator_num] == 1:  # 电梯是向上运行的
        label_floor.setText("↑" + str(floor[elevator_num]))
    else:
        label_floor.setText(str(floor[elevator_num]))



def Elevator_Pause(elevator_num):
    if pause[elevator_num - 1] == 0:
        pause[elevator_num - 1] = 1
        My_Elevator_Window.findChild(QPushButton, "pause{0}".format(elevator_num)).setText("Pause")
    else:
        pause[elevator_num - 1] = 0
        My_Elevator_Window.findChild(QPushButton, "pause{0}".format(elevator_num)).setText("Start")


def Set_Elevator_Goal_Internal(elevator_num, to_floor):  # 设定电梯内部的目标楼层

    My_Elevator_Window.findChild(QPushButton, "{0}+{1}".format(elevator_num, to_floor)).setStyleSheet(
        "QPushButton{background-image: url(background.png)}")
    elevator_goal_internal[elevator_num - 1].add(to_floor)
    elevator_goal_total[elevator_num - 1].add(to_floor)


def Set_Elevator_Goal_External_Up(to_floor):  # 设定电梯外上楼请求所在的楼层

    if to_floor in external_up:
        return

    external_up.add(to_floor)

    My_Elevator_Window.findChild(QPushButton, "up{0}".format(to_floor)).setStyleSheet("QPushButton{background-image: url(background.png)}")

    # 下面是选择哪个电梯来响应这个请求的关键代码！
    # 先看有没有空闲的电梯，有的话直接加上，然后return
    for i in range(5):
        if state[i] == 0:
            elevator_goal_external_up[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return
    # 看看有没有现在在 to_floor 以下的楼层，而且是向上走的电梯
    for i in range(5):
        if state[i] == 1 and floor[i] <= to_floor:  #这里我是找到一个就加入了，没有再选择
            elevator_goal_external_up[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return
    # 最后的话就直接选个在 to_floor 以下的楼层（那肯定是向下走的，显然选to_floor以下向下走的电梯比选to_floor以上向下走的电梯更优）
    min_floor = min(floor)
    lowest_elevator = floor.index(min_floor)

    if min_floor <= to_floor:
        elevator_goal_external_up[lowest_elevator].add(to_floor)
        elevator_goal_total[lowest_elevator].add(to_floor)
        return

    # 到这，说明所有的电梯都在to_floor上面，优先选往下走的；
    for i in range(5):
        if(state[i] == -1):
            elevator_goal_external_up[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    # 否则选楼层最高的
    max_floor = max(floor)
    highest_elevator = floor.index(max_floor)
    elevator_goal_external_up[highest_elevator].add(to_floor)
    elevator_goal_total[highest_elevator].add(to_floor)


def Set_Elevator_Goal_External_Down(to_floor):  # 设定电梯外下楼请求所在的楼层
    if to_floor in external_down:
        return

    external_down.add(to_floor)

    My_Elevator_Window.findChild(QPushButton, "down{0}".format(to_floor)).setStyleSheet("QPushButton{background-image: url(background.png)}")

    # 先看有没有空闲的电梯，有的话直接加上，然后return
    for i in range(5):
        if state[i] == 0:
            elevator_goal_external_down[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return
    # 看看有没有现在在 to_floor 以上的楼层，而且是向下走的电梯
    for i in range(5):
        if state[i] == -1 and floor[i] >= to_floor:  # 这里我是找到一个就加入了，没有再选择
            elevator_goal_external_down[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    # 最后的话就直接选个在 to_floor 以上的楼层（那肯定是向上走的，显然选to_floor以上向上走的电梯比选to_floor以下向上走的电梯更优）
    max_floor = max(floor)
    highest_elevator = floor.index(max_floor)

    if max_floor >= to_floor:
        elevator_goal_external_down[highest_elevator].add(to_floor)
        elevator_goal_total[highest_elevator].add(to_floor)
        return

    # 到这，说明所有的电梯都在to_floor下面，优先选往上走的；
    for i in range(5):
        if (state[i] == 1):
            elevator_goal_external_down[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    # 否则选楼层最低的
    min_floor = min(floor)
    lowest_elevator = floor.index(min_floor)
    elevator_goal_external_down[lowest_elevator].add(to_floor)
    elevator_goal_total[lowest_elevator].add(to_floor)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    My_Elevator_Window = Elevator_Window() # 图形化页面的实例

    elevator_goal_internal = [] # 电梯内部按下的目标楼层
    elevator_goal_external_up = [] # 分配给该电梯的外部按下的向上的目标楼层
    elevator_goal_external_down = [] # 分配给该电梯的外部按下的向下的目标楼层
    elevator_goal_total = [] # 分配给该电梯的所有目标楼层
    external_up = set([]) # 记录外面按下的所有向上电梯，这是为了避免重复按键导致某楼层被加入多个电梯的目标楼层
    external_down = set([]) # 记录外面按下的所有向下电梯，这是为了避免重复按键导致某楼层被加入多个电梯的目标楼层

    for i in range(5):
        elevator_goal_internal.append(set([]))
        elevator_goal_external_up.append(set([]))
        elevator_goal_external_down.append(set([]))
        elevator_goal_total.append(set([]))

    state = [] # 电梯状态 0表示停止 1表示向上运行 -1表示向下运行
    pause = [] # 电梯是否暂停运行
    floor = [] # 当前楼层
    open_door = [] # 电梯是否需要开门

    for i in range(5):
        state.append(0)
        pause.append(1)
        floor.append(1)
        open_door.append(0)

    My_Elevator_Thread = [] # 电梯的线程
    for i in range(1,6):
        My_Elevator_Thread.append(Elevator_Thread(i))

    for i in range(5):
        My_Elevator_Thread[i].start()

    sys.exit(app.exec_())  # 应用程序主循环