(function (window) {
    var document = window.document;

    // 获取“开始模拟”按钮
    var Start_Simulation = document.getElementById("Start_Simulation");
    var Clear_Button = document.getElementById("Clear")

    //获取参数信息
    var Memory_Blocks_Count = parseInt(document.getElementById("Memory_Blocks_Count").textContent); // 4
    var Instructions_Count = parseInt(document.getElementById("Instructions_Count").textContent); // 320
    var Instructions_Count_Per_Page = parseInt(document.getElementById("Instructions_Count_Per_Page").textContent); // 10

    //获取需要改变的标签元素
    var Page_Fault_CountSpan = document.getElementById("Page_Fault_Count");
    var Page_Fault_RateSpan = document.getElementById("Page_Fault_Rate");

    //定义变量
    var memory = [];// 内存块
    var instructions = [];// 记录指令访问次序
    var page_fault_count = 0;// 缺页个数

    function init() {

        //清空表格
        var table = document.getElementById("simulation-information");
        while (table.rows.length > 2) {
            table.deleteRow(table.rows.length - 1);
        }

        //初始化变量
        memory = new Array(Memory_Blocks_Count);
        instructions = new Array(Instructions_Count);

        page_fault_count = 0;

        Page_Fault_CountSpan.textContent = page_fault_count;
        Page_Fault_RateSpan.textContent = page_fault_count / Instructions_Count;

    };

    function generate_instructions() {
        var cur_ins = Math.floor(Math.random() * Instructions_Count); //随机生成起始指令 current_instruction
        var pre_ins = -1;

        //按照顺序执行、跳转到后地址、顺序执行、跳转到前地址的顺序生成指令
        //所以可以根据 idx 来确定当前指令应当如何生成

        var idx = 0;
        instructions[0] = cur_ins;

        while (idx < Instructions_Count - 1) {
            pre_ins = cur_ins;

            if (idx % 2 === 0 && cur_ins < Instructions_Count - 1) //顺序执行
                ++cur_ins;

            else if (idx % 4 === 1 && cur_ins < Instructions_Count - 2) //跳转到后地址
                cur_ins = Math.floor(Math.random() * (Instructions_Count - (cur_ins + 2))) + cur_ins + 2;

            else if (idx % 4 === 3 && cur_ins > 0) //跳转到前地址
                cur_ins = Math.floor(Math.random() * cur_ins);

            else {
                while (cur_ins === pre_ins) //如果指令没变，说明前述的跳转规则不适用，直接随机一条新指令
                    cur_ins = Math.floor(Math.random() * Instructions_Count);
            }
            instructions[++idx] = cur_ins;

        }
    }

    function update_table(idx, instruction_available, block) {

        var cur_ins = instructions[idx]; //current_instruction
        var next_ins = instructions[idx + 1]; //next_instruction

        var new_row = document.getElementById("simulation-information").insertRow()
        new_row.insertCell(0).innerHTML = idx + 1;
        new_row.insertCell(1).innerHTML = "NO. " + cur_ins;

        if (next_ins == cur_ins + 1)
            new_row.insertCell(2).innerHTML = "→Sequence"
        else if (next_ins < cur_ins)
            new_row.insertCell(2).innerHTML = "↑Preceding"
        else if (next_ins > cur_ins)
            new_row.insertCell(2).innerHTML = "↓Succeeding"
        else
            new_row.insertCell(2).innerHTML = "NULL"

        for (var i = 0; i < 4; ++i)
            new_row.insertCell(i + 3).innerHTML =
                memory[i] == undefined ? "Empty" : memory[i];

        if (!instruction_available) 
            new_row.insertCell(7).innerHTML = "⚠ Page fault &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + "<br>🔗Loaded into memory block " + block;
        else 
            new_row.insertCell(7).innerHTML = "✔ Already in memory block " + block;
    }

    function is_Available(number) {
        for (var i = 0; i < memory.length; i++) 
            if (Math.floor(number / Instructions_Count_Per_Page) === memory[i]) 
                return true; // 已经存在，没有发生缺页
        return false;// 缺页
    };

    function execute_simulation() {
        var page_replacement_algorithm = document.querySelector("input:checked").value; //获取对换页算法的选择

        var vis_seq = [0, 1, 2, 3];// visit_sequence 访问顺序，靠近末尾的为最近访问的
        var FIFO_block = 0;

        for (var idx = 0; idx < instructions.length; ++idx) {

            cur_ins = instructions[idx];
            var cur_page = Math.floor(cur_ins / Instructions_Count_Per_Page); //current_page

            // 判断选中指令是否在内存中
            var instruction_available = is_Available(cur_ins);
            if (!instruction_available) { // 不在内存中，缺页
                 
                page_fault_count++; //跟新缺页数目
                
                // 更新相应html标签
                Page_Fault_CountSpan.textContent = page_fault_count;
                Page_Fault_RateSpan.textContent = page_fault_count / Instructions_Count;

                // 替换
                if (page_replacement_algorithm === "FIFO") 
                    memory[(FIFO_block++) % 4] = cur_page;

                else if (page_replacement_algorithm === "LRU")
                    memory[vis_seq[0]] = cur_page;

            };

            if (page_replacement_algorithm === "FIFO")
                update_table(idx, instruction_available, (FIFO_block - 1) % 4 + 1);

            else if (page_replacement_algorithm === "LRU") {
                // 更新访问顺序
                var LRU_block = memory.indexOf(cur_page);

                // 将当前块在访问顺序数组中挪到最后一位
                vis_seq.splice(vis_seq.indexOf(LRU_block), 1);
                vis_seq.push(LRU_block);

                update_table(idx, instruction_available, LRU_block + 1);
            }

        };
    }

    function start() {
        // 禁用“Start”和"Clear"按钮
        Start_Simulation.disabled = true;
        Clear_Button.disabled = true;

        init(); // 初始化表格和变量
        generate_instructions(); //生成指令序列
        execute_simulation(); //开始模拟

        // 启用“Start”和"Clear"按钮
        Start_Simulation.disabled = false;
        Clear_Button.disabled = false;
    }

    // 添加点击按钮关联的函数
    Start_Simulation.addEventListener('click', start);
    Clear_Button.addEventListener('click', init);

})(window)


