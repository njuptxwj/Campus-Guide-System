# -*- coding: utf-8 -*-
"""根据模板生成课程设计报告"""

import os
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn

import draw_flowcharts


def set_run_font(run, name="宋体", size=12, bold=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.font.bold = bold


def add_title_paragraph(doc, text, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    return p


def add_heading(doc, text, level=1):
    sizes = {1: 14, 2: 12}
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_run_font(run, size=sizes.get(level, 12), bold=True)
    return p


def add_body(doc, text, first_line_indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if first_line_indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run(text)
    set_run_font(run, size=12)
    return p


def add_code(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    run.font.size = Pt(10.5)
    return p


def add_figure(doc, image_path, caption):
    if not os.path.exists(image_path):
        add_body(doc, f"（图片缺失：{caption}）")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(image_path, width=Inches(5.8))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cap.add_run(caption)
    set_run_font(run, size=10.5)
    doc.add_paragraph()


def build_report():
    img_dir = draw_flowcharts.generate_all()
    img = {os.path.basename(p): p for p in img_dir}

    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)

    # 封面
    add_title_paragraph(doc, "《数据结构与算法课程设计》", size=18)
    add_title_paragraph(doc, "课程设计报告", size=22)
    add_title_paragraph(doc, "（ 2025 / 2026 学年 第 2 学期）", size=14, bold=False)
    doc.add_paragraph()
    for label, value in [
        ("题    目：", "校园导游程序"),
        ("专    业：", "（请填写）"),
        ("班    级：", "（请填写）"),
        ("学    号：", "（请填写）"),
        ("姓    名：", "（请填写）"),
        ("指导教师：", "刘红霞"),
        ("指导单位：", "计算机学院"),
        ("日    期：", "2026年6月"),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f"{label}{value}")
        set_run_font(run, size=14)

    doc.add_page_break()

    # 一、设计题目
    add_heading(doc, "一、设计题目")
    add_body(doc, "校园导游程序")

    # 二、设计内容和要求
    add_heading(doc, "二、设计内容和要求")
    add_body(doc, "运用数据结构与算法知识设计一个校园导游程序，为来访的客人提供信息查询服务。基本要求如下：")
    add_body(doc, "（1）设计学校的校园平面图，所含景点不少于 10 个。以图中顶点表示校内各景点，存放景点名称、代号、简介等信息；以边表示路径，存放路径长度等相关信息。")
    add_body(doc, "（2）为来访客人提供图中任意景点相关信息的查询。")
    add_body(doc, "（3）为来访客人提供从任意景点到任意景点的问路查询，输出最短路径及路径长度。")
    add_body(doc, "扩展要求：采用堆优化的 Dijkstra 算法求最短路径；使用 NetworkX 与 Matplotlib 实现校园拓扑图的图形化展示；设计基于 Tkinter 的图形用户界面，提升交互体验。")

    # 三、功能模块设计
    add_heading(doc, "三、功能模块设计")
    add_body(doc, "本系统采用“核心逻辑层 + 图形界面层”的分层结构。核心算法与数据存储位于 campus_guide.py，图形界面位于 campus_guide_gui.py。系统主要包含以下功能模块：")
    add_heading(doc, "3.1 景点信息管理模块", level=2)
    add_body(doc, "维护 17 个景点的代号、名称和简介信息。用户通过下拉框或景点列表选择某一景点时，系统自动在简介区域显示该景点的详细信息。")
    add_heading(doc, "3.2 问路查询模块", level=2)
    add_body(doc, "用户选择起点和终点后，系统调用堆优化 Dijkstra 算法计算两点之间的最短路径，输出总路程和途经景点序列，并在地图上用红色高亮显示该路径。")
    add_heading(doc, "3.3 图形化地图展示模块", level=2)
    add_body(doc, "基于 NetworkX 构建无向带权图，利用 Matplotlib 在界面右侧嵌入绘制校园拓扑图。节点表示景点，边表示道路，边上标注距离（米）。问路成功后最短路径以红色粗线高亮。")
    add_heading(doc, "3.4 图形用户界面模块", level=2)
    add_body(doc, "使用 Tkinter 构建桌面交互界面。左侧为景点简介、问路操作和景点列表；右侧为内嵌的校园地图画布。用户无需命令行输入即可完成全部操作。")

    # 四、环境说明和概要设计
    add_heading(doc, "四、环境说明和概要设计")
    add_heading(doc, "4.1 环境说明", level=2)
    add_body(doc, "硬件环境：Intel/AMD 处理器，4GB 及以上内存，分辨率 1920×1080 及以上显示器。")
    add_body(doc, "软件环境：Windows 10/11 操作系统；Python 3.10 及以上；主要依赖库包括 networkx、matplotlib；图形界面使用 Python 标准库 tkinter。")
    add_heading(doc, "4.2 数据结构设计与存储结构", level=2)
    add_body(doc, "本系统以无向带权图 G=(V,E) 为逻辑结构，各功能模块使用的数据结构与存储结构如下表所示。")
    add_body(doc, "（1）景点表 SPOTS\n逻辑结构：集合（17 个景点顶点）。\n存储结构：Python 字典 dict[int, tuple]。键为景点代号，值为 (名称, 简介) 元组。\n用途：O(1) 查询景点名称与简介，供界面显示和路径输出。\n定义示例：SPOTS = {0: (\"南门\", \"学校南侧主入口……\"), …}")
    add_body(doc, "（2）边集 EDGES\n逻辑结构：线性表（22 条无向边）。\n存储结构：Python 列表 list[tuple]，每个元素为 (起点代号, 终点代号, 权值/米)。\n用途：图的原始数据来源，构建邻接表和 NetworkX 图均从 EDGES 读取，保证数据唯一、一致。")
    add_body(doc, "（3）邻接表 graph\n逻辑结构：图（邻接表表示）。\n存储结构：字典嵌套字典 dict[int, dict[int, int]]，graph[u][v]=w 表示 u 与 v 之间存在权值为 w 的边。\n用途：供 Dijkstra 算法遍历邻接点。相比邻接矩阵，在稀疏图（E 远小于 V²）中节省空间，遍历边的时间复杂度为 O(degree(u))。")
    add_body(doc, "（4）距离表 dist 与前驱表 prev\n逻辑结构：线性表。\n存储结构：Python 字典，dist[i] 表示起点到 i 的当前最短距离；prev[i] 记录最短路径中 i 的前驱节点。\n用途：Dijkstra 算法核心辅助结构，算法结束后通过 prev 回溯得到完整路径。")
    add_body(doc, "（5）最小堆 pq\n逻辑结构：优先队列（按距离从小到大）。\n存储结构：Python list 配合 heapq 模块实现二叉堆，元素为 (距离, 节点代号) 二元组。\n用途：每次 O(logV) 取出当前距离最小的未确定节点，实现堆优化 Dijkstra。")
    add_body(doc, "（6）节点坐标 NODE_POS\n逻辑结构：集合。\n存储结构：Python 字典 dict[int, tuple(float, float)]，存储各景点在画布上的 (x, y) 坐标。\n用途：NetworkX 固定布局绘图，使图形化地图与校园实际布局一致。")
    add_body(doc, "（7）NetworkX 图对象 G\n逻辑结构：图。\n存储结构：networkx.Graph 对象，节点带 label 属性，边带 weight 属性。\n用途：render_graph() 中调用 nx.draw_networkx_* 系列函数完成可视化。")

    add_heading(doc, "4.3 各模块算法与流程图概述", level=2)
    add_body(doc, "系统各功能模块均对应明确的算法流程，以下在概要设计阶段给出总体说明，详细流程图见第五章。")
    add_body(doc, "（1）系统总体流程：启动时加载数据、构建邻接表、渲染地图，进入事件循环；根据用户操作分支至简介查询、问路查询或清除路线。")
    add_body(doc, "（2）邻接表构建：顺序扫描 EDGES，对每条边 (a,b,w) 双向写入 graph[a][b] 和 graph[b][a]。")
    add_body(doc, "（3）问路查询（Dijkstra）：以起点为源，用最小堆按距离递增扩展，松弛邻接边，直到找到终点或堆为空。")
    add_body(doc, "（4）地图渲染：由 EDGES 构建 NetworkX 图，按 NODE_POS 绘制节点和边，若有问路结果则将路径边红色高亮。")
    add_figure(doc, img["flow_system.png"], "图1  系统总体流程图")

    # 五、详细设计
    add_heading(doc, "五、详细设计")
    add_heading(doc, "5.1 系统结构与文件组织", level=2)
    add_body(doc, "campus_guide.py：核心模块，包含 SPOTS、EDGES 数据定义，build_graph() 构建邻接表，dijkstra() 堆优化最短路径，render_graph() 地图渲染，get_spot_info() 和 format_route() 等辅助函数。")
    add_body(doc, "campus_guide_gui.py：界面模块，CampusGuideApp 类负责窗口布局、事件响应和地图画布刷新。")
    add_body(doc, "campus_guide_cli.py：命令行版本（备用）。")

    add_heading(doc, "5.2 邻接表构建模块", level=2)
    add_body(doc, "算法描述：build_graph() 首先为 SPOTS 中每个景点代号创建空的邻接字典，然后遍历 EDGES 列表，对每条道路 (a, b, w) 执行 graph[a][b]=w 和 graph[b][a]=w，形成无向图邻接表。算法时间复杂度 O(V+E)，空间复杂度 O(V+E)。")
    add_body(doc, "数据结构：输入为 list 类型的 EDGES；输出为 dict 类型的邻接表 graph。选择邻接表而非邻接矩阵，是因为本图仅有 22 条边，属于稀疏图，邻接表更节省空间且便于 Dijkstra 遍历。")
    add_figure(doc, img["flow_build_graph.png"], "图3  邻接表构建算法流程图")
    add_code(doc, """def build_graph():
    graph = {i: {} for i in SPOTS}
    for a, b, w in EDGES:
        graph[a][b] = w
        graph[b][a] = w
    return graph""")

    add_heading(doc, "5.3 景点信息查询模块", level=2)
    add_body(doc, "算法描述：用户在下拉框或列表中选择景点后，界面调用 parse_spot_label() 解析出景点代号 spot_id，再通过 get_spot_info(spot_id) 在 SPOTS 字典中以 O(1) 时间取出 (名称, 简介) 并格式化显示。该模块不涉及图遍历，属于直接查表操作。")
    add_body(doc, "数据结构：SPOTS 字典为唯一数据源；界面层使用 tk.StringVar 绑定下拉框选项，Text 控件只读显示查询结果。")
    add_code(doc, """def get_spot_info(spot_id):
    name, desc = SPOTS[spot_id]
    return f"代号：{spot_id}\\n名称：{name}\\n简介：{desc}" """)

    add_heading(doc, "5.4 问路查询模块（堆优化 Dijkstra）", level=2)
    add_body(doc, "算法描述：本模块是系统核心。给定邻接表 graph、起点 start 和终点 target，采用堆优化 Dijkstra 算法求单源最短路径。算法维护 dist（最短距离）、prev（前驱节点）和最小堆 pq。每次从 pq 弹出距离最小的节点 u 进行扩展；对 u 的每个邻接点 v，若 dist[u]+w(u,v) 小于 dist[v]，则更新 dist[v]、prev[v] 并将 (新距离, v) 入堆。当 u 等于 target 时提前终止；若堆空仍未到达 target，则判定不可达。")
    add_body(doc, "路径回溯：算法结束后，从 target 出发沿 prev 指针逆向追踪至 start，再反转得到正序路径。")
    add_body(doc, "数据结构：graph 为邻接表；dist、prev 为字典；pq 为 heapq 最小堆（list 实现）。时间复杂度 O((V+E)logV)，空间复杂度 O(V+E)。")
    add_figure(doc, img["flow_dijkstra.png"], "图2  堆优化 Dijkstra 算法流程图")
    add_code(doc, """def dijkstra(graph, start, target):
    dist = {i: float("inf") for i in SPOTS}
    prev = {i: None for i in SPOTS}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == target:
            break
        for v, w in graph[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    # 回溯路径并返回 (dist, path)""")

    add_heading(doc, "5.5 地图渲染模块", level=2)
    add_body(doc, "算法描述：render_graph(ax, highlight_path) 在 Matplotlib 的 Axes 对象上绘制校园拓扑图。首先调用 build_networkx_graph() 由 EDGES 构建 NetworkX 图；然后按 NODE_POS 坐标绘制节点和标签；遍历所有边，若 highlight_path 不为空，则将路径上的边用红色粗线绘制，其余边用灰色绘制；最后标注边权并刷新画布。")
    add_body(doc, "数据结构：NetworkX Graph 存储拓扑；NODE_POS 提供布局坐标；highlight_path 为 list[int] 类型的节点序列，通过 path_edges() 转换为边集合用于高亮判断。")
    add_figure(doc, img["flow_render.png"], "图4  地图渲染算法流程图")

    add_heading(doc, "5.6 图形界面交互模块", level=2)
    add_body(doc, "算法描述：CampusGuideApp 类在初始化时调用 build_graph() 构建邻接表并渲染初始地图，随后进入 Tkinter 事件循环。用户触发不同控件事件时：选择景点则调用 get_spot_info() 更新简介区；点击「开始问路」则调用 dijkstra() 并将结果写入问路区、更新 highlight_path 后重绘地图；点击「清除路线」则将 highlight_path 置空并重绘。")
    add_body(doc, "数据结构：界面层持有 graph（邻接表）、highlight_path（当前高亮路径）、spot_options（下拉选项列表）等实例变量；地图区使用 FigureCanvasTkAgg 将 Matplotlib 画布嵌入 Tkinter 窗口。总体流程见图1。")

    add_heading(doc, "5.7 校园平面图", level=2)
    add_body(doc, "本系统校园平面图包含 17 个景点、22 条道路，拓扑关系如下：")
    add_body(doc, "南门(0)—教学楼1(1)—教学楼4(2)—图书馆(3)；南门(0)—梅苑(6)—南一食堂(7)；南门(0)—校史馆(4)；南门(0)—实验楼(14)；教学楼1(1)—实验楼(14)—校史馆(4)；图书馆(3)—南二食堂(5)；南一食堂(7)—南二食堂(5)；南二食堂(5)—南操场(8)—桃苑(10)—北荷(12)；桃苑(10)—东门(9)；桃苑(10)—医务室(11)—学科楼(15)—北门(16)；学科楼(15)—体育馆(13)；北荷(12)—体育馆(13)；南操场(8)—东门(9)。各边权值见 EDGES 数据。")

    # 六、测试内容及测试结果
    add_heading(doc, "六、测试内容及测试结果")
    add_heading(doc, "6.1 使用方法", level=2)
    add_body(doc, "安装依赖：pip install -r requirements.txt")
    add_body(doc, "启动程序：python campus_guide_gui.py")
    add_body(doc, "操作说明：在左侧下拉框或景点列表中选择景点可查看简介；在问路区域选择起点和终点，点击“开始问路”即可查询最短路径；点击“清除路线”取消高亮；右侧地图实时显示拓扑结构和问路结果。")
    add_heading(doc, "6.2 测试数据与结果", level=2)
    tests = [
        ("景点简介查询", "选择代号 3（图书馆）", "正确显示名称“图书馆”及简介内容"),
        ("同点问路", "起点=终点=南门(0)", "弹出提示“起点与终点相同，无需问路”"),
        ("南门→北门", "起点=0，终点=16", "最短路径 980 米：南门→校史馆→南一食堂→南二食堂→南操场→桃苑→医务室→学科楼→北门"),
        ("南门→图书馆", "起点=0，终点=3", "最短路径 370 米：南门→教学楼1→教学楼4→图书馆"),
        ("实验楼→东门", "起点=14，终点=9", "正确输出最短路径并在地图红色高亮"),
        ("图形化地图", "点击问路后查看右侧地图", "全部道路灰色显示，最短路径红色粗线高亮，边权标注正确"),
    ]
    for name, data, result in tests:
        add_body(doc, f"测试项：{name}。输入：{data}。预期/结果：{result}。")
    add_heading(doc, "6.3 算法时间复杂度分析", level=2)
    add_body(doc, "设 V=17 为景点数，E=22 为道路数。堆优化 Dijkstra 算法中，每个节点最多入堆一次，每条边最多松弛一次，堆操作复杂度 O(logV)，总时间复杂度 O((V+E)logV)。在本项目规模下运行时间为毫秒级，满足实时交互需求。相比朴素 O(V²) 实现，在稀疏图中效率更优，且易于扩展到更大规模的校园地图。")

    # 七、设计调试过程中的问题
    add_heading(doc, "七、设计调试过程中的问题")
    add_body(doc, "（1）控制台中文乱码：Windows 控制台默认 GBK 编码，与 UTF-8 源码不一致导致乱码。早期命令行版本通过 SetConsoleOutputCP(65001) 和 /utf-8 编译选项解决；最终采用 Tkinter 图形界面后该问题自然消除。")
    add_body(doc, "（2）C++ 与 Python 选型：初期使用 C++ 实现，因编码和语法兼容问题调试成本较高。后改用 Python，配合 networkx、matplotlib 快速实现图算法和可视化，开发效率显著提升。")
    add_body(doc, "（3）地图与数据不同步：曾使用手写 ASCII 图展示道路，修改 EDGES 后易与真实数据不一致。最终改为 EDGES 为唯一数据源，NetworkX 图形化展示真实拓扑。")
    add_body(doc, "（4）Matplotlib 嵌入 Tkinter：由 plt.show() 弹窗改为 FigureCanvasTkAgg 嵌入主窗口，需在每次问路后调用 canvas.draw() 刷新画布。")
    add_body(doc, "（5）算法优化：将朴素 Dijkstra 改为 heapq 堆优化，并增加目标节点提前终止，减少不必要的节点扩展。")

    # 八、课程学习总结
    add_heading(doc, "八、课程学习总结")
    add_body(doc, "通过本次校园导游程序的课程设计，我将课堂所学的图、邻接表、最短路径等理论知识应用于实际项目，完成了从需求分析、数据结构设计、算法实现到图形界面开发的全流程。")
    add_body(doc, "在数据结构方面，用邻接表存储稀疏无向带权图，用字典管理景点属性，结构清晰且便于维护。在算法方面，理解并实现了堆优化 Dijkstra 算法，掌握了优先队列在图算法中的作用。在工程实践方面，学会了模块分层、GUI 与算法解耦、以及 NetworkX 与 Matplotlib 的可视化集成。")
    add_body(doc, "设计过程中也认识到：数据结构设计应服务于算法需求，可视化应以 EDGES 等原始数据为准，避免多处维护导致不一致。")
    add_body(doc, "关于 AI 工具的使用：本次设计过程中使用了 Cursor IDE 中的 AI 编程助手。主要用途包括：理解课程设计要求并规划图的数据结构；在 C++ 版本出现编码和语法问题时排查修复；将控制台程序重构为 Python 版本并实现 NetworkX 图形化；设计 Tkinter 图形界面并实现堆优化 Dijkstra。AI 工具在代码生成、错误定位和方案对比方面提高了效率，但核心算法思路、校园地图拓扑设计、测试用例验证和报告撰写仍由本人理解和完成。通过合理使用 AI 辅助工具，我能将更多精力集中在算法正确性和系统设计思路上，同时也意识到必须对 AI 生成的代码进行审查和测试，不能盲目依赖。")
    add_body(doc, "总体而言，本次课程设计加深了我对图论算法和数据结构应用的理解，提升了 Python 编程和软件界面开发能力，为后续学习更复杂的算法和系统开发打下了基础。")

    out_path = os.path.join(os.path.dirname(__file__), "程序设计报告_含流程图.docx")
    doc.save(out_path)
    print(f"报告已生成：{out_path}")


if __name__ == "__main__":
    build_report()
