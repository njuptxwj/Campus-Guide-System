# -*- coding: utf-8 -*-
"""生成课程设计报告用算法流程图"""

import os

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "report_images")


def _box(ax, x, y, w, h, text, shape="rect"):
    if shape == "ellipse":
        patch = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.3",
            linewidth=1.2, edgecolor="black", facecolor="#E8F4FC",
        )
    elif shape == "diamond":
        patch = plt.Polygon(
            [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
            closed=True, linewidth=1.2, edgecolor="black", facecolor="#FFF3CD",
        )
        ax.add_patch(patch)
        ax.text(x, y, text, ha="center", va="center", fontsize=9, wrap=True)
        return
    else:
        patch = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.2, edgecolor="black", facecolor="#E8F4FC",
        )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=9)


def _arrow(ax, x1, y1, x2, y2, label=""):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=12,
        linewidth=1.1, color="#333333",
        shrinkA=4, shrinkB=4,
    )
    ax.add_patch(arr)
    if label:
        ax.text((x1 + x2) / 2 + 0.15, (y1 + y2) / 2, label, fontsize=8, color="#555555")


def _save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def draw_system_flowchart():
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis("off")
    ax.set_title("图1  系统总体流程图", fontsize=13, pad=12)

    _box(ax, 5, 13, 3.6, 0.7, "开始", "ellipse")
    _box(ax, 5, 11.6, 4.2, 0.8, "启动 GUI，加载 SPOTS/EDGES\n调用 build_graph() 构建邻接表")
    _box(ax, 5, 10.2, 4.0, 0.8, "渲染初始校园地图\nrender_graph()")
    _box(ax, 5, 8.8, 3.6, 0.7, "等待用户操作", "ellipse")
    _box(ax, 5, 7.3, 3.8, 0.9, "用户选择景点？", "diamond")

    _box(ax, 2, 5.8, 3.2, 0.9, "查询景点简介\nget_spot_info()")
    _box(ax, 5, 5.8, 3.2, 0.9, "选择起终点\n点击「开始问路」", "rect")
    _box(ax, 8, 5.8, 3.0, 0.9, "点击「清除路线」\nhighlight_path=None")

    _box(ax, 5, 4.2, 3.6, 0.8, "起点=终点？", "diamond")
    _box(ax, 5, 2.8, 4.0, 0.9, "dijkstra(start,target)\n堆优化最短路径")
    _box(ax, 5, 1.4, 3.8, 0.9, "输出路线文字\n地图红色高亮路径")
    _box(ax, 8, 4.2, 3.0, 0.7, "提示后返回")
    _box(ax, 5, 0.3, 3.6, 0.7, "退出系统？", "diamond")
    _box(ax, 8.5, 0.3, 2.2, 0.6, "结束", "ellipse")

    _arrow(ax, 5, 12.65, 5, 12.0)
    _arrow(ax, 5, 11.2, 5, 10.6)
    _arrow(ax, 5, 9.8, 5, 9.15)
    _arrow(ax, 5, 8.45, 5, 7.75)
    _arrow(ax, 4.2, 7.3, 2, 6.25, "浏览简介")
    _arrow(ax, 5, 6.85, 5, 6.25)
    _arrow(ax, 5.8, 7.3, 8, 6.25, "清除")
    _arrow(ax, 2, 5.35, 2, 8.45)
    _arrow(ax, 2, 8.45, 4.0, 8.45)
    _arrow(ax, 8, 5.35, 8, 8.45)
    _arrow(ax, 8, 8.45, 6.0, 8.45)
    _arrow(ax, 5, 5.35, 5, 4.6)
    _arrow(ax, 4.2, 4.2, 8, 4.55, "是")
    _arrow(ax, 8, 4.2, 8, 8.45)
    _arrow(ax, 5, 3.75, 5, 3.25, "否")
    _arrow(ax, 5, 2.35, 5, 1.85)
    _arrow(ax, 5, 0.95, 5, 0.65)
    _arrow(ax, 5, 0.3, 8.5, 0.3, "是")
    _arrow(ax, 4.0, 0.3, 4.0, 8.45)
    _arrow(ax, 4.0, 8.45, 4.0, 9.15)

    return _save(fig, "flow_system.png")


def draw_dijkstra_flowchart():
    fig, ax = plt.subplots(figsize=(7, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis("off")
    ax.set_title("图2  堆优化 Dijkstra 算法流程图", fontsize=13, pad=12)

    steps = [
        (5, 15, "开始", "ellipse", 3.0, 0.7),
        (5, 13.6, "输入：邻接表 graph，起点 start，终点 target", "rect", 5.5, 0.8),
        (5, 12.2, "初始化 dist[start]=0，其余 dist=∞\nprev 全部置空，pq={(0,start)}", "rect", 5.2, 1.0),
        (5, 10.6, "pq 为空？", "diamond", 3.4, 0.9),
        (5, 9.1, "弹出堆顶 (d, u)", "rect", 3.8, 0.7),
        (5, 7.7, "d > dist[u]？", "diamond", 3.6, 0.9),
        (5, 6.2, "u == target？", "diamond", 3.6, 0.9),
        (5, 4.7, "遍历 u 的每个邻接点 v\nnd = d + w(u,v)", "rect", 5.0, 0.9),
        (5, 3.2, "nd < dist[v]？", "diamond", 3.6, 0.9),
        (5, 1.8, "更新 dist[v]、prev[v]\n将 (nd,v) 入堆", "rect", 4.6, 0.9),
        (5, 0.4, "继续循环", "rect", 3.0, 0.6),
    ]
    for x, y, t, s, w, h in steps:
        _box(ax, x, y, w, h, t, s)

    _box(ax, 8.2, 10.6, 3.0, 0.9, "dist[target]=∞？\n返回 None", "diamond")
    _box(ax, 8.2, 8.8, 3.2, 0.9, "沿 prev 回溯\n构造路径 path", "rect")
    _box(ax, 8.2, 7.2, 3.0, 0.7, "返回 (dist, path)", "rect")
    _box(ax, 8.2, 5.8, 2.4, 0.7, "结束", "ellipse")

    _arrow(ax, 5, 14.65, 5, 14.0)
    _arrow(ax, 5, 13.2, 5, 12.7)
    _arrow(ax, 5, 11.7, 5, 11.05)
    _arrow(ax, 5, 10.15, 5, 9.45)
    _arrow(ax, 6.0, 10.6, 7.0, 10.6, "是")
    _arrow(ax, 8.2, 10.15, 8.2, 9.25)
    _arrow(ax, 5, 8.75, 5, 8.05)
    _arrow(ax, 6.0, 7.7, 7.5, 7.7, "否")
    _arrow(ax, 7.5, 7.7, 7.5, 0.4)
    _arrow(ax, 7.5, 0.4, 6.5, 0.4)
    _arrow(ax, 5.5, 7.7, 6.8, 6.2, "是")
    _arrow(ax, 6.8, 6.2, 7.2, 7.2)
    _arrow(ax, 5, 7.25, 5, 6.55)
    _arrow(ax, 5, 5.75, 5, 5.15)
    _arrow(ax, 5, 4.25, 5, 3.65)
    _arrow(ax, 5, 2.75, 5, 2.25)
    _arrow(ax, 6.0, 3.2, 7.0, 3.2, "否")
    _arrow(ax, 7.0, 3.2, 7.0, 0.4)
    _arrow(ax, 5, 2.25, 5, 1.35, "是")
    _arrow(ax, 5, 0.7, 5, 0.4)
    _arrow(ax, 3.5, 0.4, 3.5, 9.1)
    _arrow(ax, 3.5, 9.1, 3.1, 9.1)
    _arrow(ax, 3.3, 7.7, 2.5, 7.7, "是")
    _arrow(ax, 2.5, 7.7, 2.5, 9.1)
    _arrow(ax, 8.2, 8.35, 8.2, 7.55)
    _arrow(ax, 8.2, 6.85, 8.2, 6.15)

    return _save(fig, "flow_dijkstra.png")


def draw_build_graph_flowchart():
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_title("图3  邻接表构建算法流程图", fontsize=13, pad=12)

    _box(ax, 5, 10, 2.8, 0.7, "开始", "ellipse")
    _box(ax, 5, 8.7, 4.8, 0.8, "创建空邻接表 graph\n对每个景点 i 令 graph[i]={}")
    _box(ax, 5, 7.3, 4.2, 0.8, "遍历 EDGES 中每条边 (a,b,w)", "rect")
    _box(ax, 5, 5.8, 4.4, 0.9, "graph[a][b]=w\ngraph[b][a]=w\n（无向图双向存储）", "rect")
    _box(ax, 5, 4.3, 3.6, 0.8, "还有未处理边？", "diamond")
    _box(ax, 5, 2.8, 3.6, 0.7, "返回 graph", "rect")
    _box(ax, 5, 1.4, 2.4, 0.7, "结束", "ellipse")

    _arrow(ax, 5, 9.65, 5, 9.1)
    _arrow(ax, 5, 8.3, 5, 7.7)
    _arrow(ax, 5, 6.9, 5, 6.25)
    _arrow(ax, 5, 5.35, 5, 4.7)
    _arrow(ax, 4.0, 4.3, 3.0, 4.3)
    _arrow(ax, 3.0, 4.3, 3.0, 7.3)
    _arrow(ax, 3.0, 7.3, 3.5, 7.3, "是")
    _arrow(ax, 5, 3.9, 5, 3.15, "否")
    _arrow(ax, 5, 2.45, 5, 1.75)

    return _save(fig, "flow_build_graph.png")


def draw_render_flowchart():
    fig, ax = plt.subplots(figsize=(6, 9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.set_title("图4  地图渲染算法流程图", fontsize=13, pad=12)

    _box(ax, 5, 11, 2.8, 0.7, "开始", "ellipse")
    _box(ax, 5, 9.6, 4.6, 0.8, "build_networkx_graph()\n由 EDGES 构建 NetworkX 图")
    _box(ax, 5, 8.2, 4.2, 0.8, "按 NODE_POS 绘制节点与标签", "rect")
    _box(ax, 5, 6.8, 4.4, 0.9, "highlight_path 为空？", "diamond")
    _box(ax, 5, 5.3, 4.6, 0.9, "全部边灰色绘制\n标注边权 weight", "rect")
    _box(ax, 8.2, 6.8, 3.4, 0.9, "最短路径边红色高亮\n其余边灰色绘制", "rect")
    _box(ax, 5, 3.7, 4.0, 0.8, "canvas.draw() 刷新界面", "rect")
    _box(ax, 5, 2.2, 2.4, 0.7, "结束", "ellipse")

    _arrow(ax, 5, 10.65, 5, 10.0)
    _arrow(ax, 5, 9.2, 5, 8.6)
    _arrow(ax, 5, 7.8, 5, 7.25)
    _arrow(ax, 5, 6.35, 5, 5.75)
    _arrow(ax, 6.2, 6.8, 8.2, 6.8, "否")
    _arrow(ax, 8.2, 6.35, 8.2, 4.15)
    _arrow(ax, 8.2, 4.15, 7.0, 4.15)
    _arrow(ax, 5, 4.85, 5, 4.1)
    _arrow(ax, 5, 3.3, 5, 2.55)

    return _save(fig, "flow_render.png")


def generate_all():
    paths = [
        draw_system_flowchart(),
        draw_dijkstra_flowchart(),
        draw_build_graph_flowchart(),
        draw_render_flowchart(),
    ]
    for p in paths:
        print("已生成:", p)
    return paths


if __name__ == "__main__":
    generate_all()
