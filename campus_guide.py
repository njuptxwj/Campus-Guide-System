# -*- coding: utf-8 -*-
"""校园导游系统 - 核心数据结构与算法"""

import heapq

import matplotlib.pyplot as plt
import networkx as nx

# 景点代号 -> (名称, 简介)
SPOTS = {
    0: ("南门", "学校南侧主入口，来访客人登记处。"),
    1: ("教学楼1", "主要公共课教学区，设施完善。"),
    2: ("教学楼4", "理工科专业课程教学区。"),
    3: ("图书馆", "藏书丰富，提供自习与阅览服务。"),
    4: ("校史馆", "展示学校发展历程与荣誉成果。"),
    5: ("南二食堂", "第二食堂，菜品多样。"),
    6: ("梅苑", "学生宿舍区，环境安静。"),
    7: ("南一食堂", "第一食堂，靠近梅苑。"),
    8: ("南操场", "田径场与球类活动场地。"),
    9: ("东门", "学校东侧出入口。"),
    10: ("桃苑", "学生宿舍区，生活便利。"),
    11: ("医务室", "提供日常医疗与急救服务。"),
    12: ("北荷", "北区宿舍区."),
    13: ("体育馆", "室内球馆与健身设施。"),
    14: ("实验楼", "理工科实验与科研场所。"),
    15: ("学科楼", "学科竞赛与科研办公区。"),
    16: ("北门", "学校北侧出入口。"),
}

EDGES = [
    (0, 1, 120), (0, 6, 250), (0, 4, 80), (1, 2, 300), (2, 3, 150), (1, 14, 180),
    (1, 4, 90), (0, 14, 150), (4, 7, 190), (6, 7, 100), (5, 8, 130), (3, 5, 110),
    (7, 5, 200), (8, 9, 190), (8, 10, 120), (10, 12, 370), (10, 9, 90), (10, 11, 110),
    (11, 15, 140), (12, 13, 80), (15, 16, 200), (15, 13, 190),
]

ENTRANCE = 0

NODE_POS = {
    0: (0.0, 0.0), 1: (1.5, 0.0), 2: (3.0, 0.0), 3: (4.5, 0.0),
    4: (1.5, -1.2), 6: (1.5, -2.4), 7: (3.0, -2.4), 5: (4.5, -1.2),
    8: (6.0, -1.2), 10: (7.5, -1.2), 12: (9.0, -1.2), 9: (7.5, -2.4),
    11: (6.0, 0.8), 13: (8.2, 0.8), 14: (2.2, 1.2), 15: (9.0, 1.2), 16: (10.5, 1.2),
}

def setup_matplotlib():
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

def spot_name(spot_id):
    return SPOTS[spot_id][0]

def spot_label(spot_id):
    return f"{spot_id} - {spot_name(spot_id)}"

def parse_spot_label(label):
    return int(label.split(" - ", 1)[0])

def build_graph():
    graph = {i: {} for i in SPOTS}
    for a, b, w in EDGES:
        graph[a][b] = w
        graph[b][a] = w
    return graph

def build_networkx_graph():
    g = nx.Graph()
    for spot_id in SPOTS:
        g.add_node(spot_id, label=f"{spot_name(spot_id)}\n({spot_id})")
    for a, b, w in EDGES:
        g.add_edge(a, b, weight=w)
    return g

def dijkstra(graph, start, target):
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

    if dist[target] == float("inf"):
        return None

    path = []
    v = target
    while v is not None:
        path.append(v)
        v = prev[v]
    path.reverse()
    return int(dist[target]), path

def path_edges(path):
    return {(path[i], path[i + 1]) for i in range(len(path) - 1)}

def get_spot_info(spot_id):
    if spot_id not in SPOTS:
        return None
    name, desc = SPOTS[spot_id]
    return f"代号：{spot_id}\n名称：{name}\n简介：{desc}"

def format_route(start, target, dist, path):
    lines = [
        f"起点：{spot_name(start)}",
        f"终点：{spot_name(target)}",
        f"最短路径长度：{dist} 米",
        "路线：" + " -> ".join(spot_name(i) for i in path),
    ]
    return "\n".join(lines)

def render_graph(ax, highlight_path=None, title="校园导游地图"):
    """在指定 Axes 上绘制校园拓扑图"""
    g = build_networkx_graph()
    labels = {n: g.nodes[n]["label"] for n in g.nodes}
    ax.clear()

    nx.draw_networkx_nodes(
        g, NODE_POS, nodelist=list(SPOTS.keys()),
        node_color="#A8D8EA", node_size=2400, ax=ax,
    )
    nx.draw_networkx_labels(g, NODE_POS, labels=labels, font_size=11, font_family="Microsoft YaHei", ax=ax)

    all_edges = list(g.edges())
    highlight = path_edges(highlight_path) if highlight_path else set()
    highlight_undirected = highlight | {(b, a) for a, b in highlight}

    normal = [
        e for e in all_edges
        if e not in highlight_undirected and (e[1], e[0]) not in highlight_undirected
    ]
    hi = [
        e for e in all_edges
        if e in highlight_undirected or (e[1], e[0]) in highlight_undirected
    ]

    nx.draw_networkx_edges(g, NODE_POS, edgelist=normal, edge_color="#888888", width=2, ax=ax)
    if hi:
        nx.draw_networkx_edges(g, NODE_POS, edgelist=hi, edge_color="#E74C3C", width=4, ax=ax)

    edge_labels = nx.get_edge_attributes(g, "weight")
    nx.draw_networkx_edge_labels(g, NODE_POS, edge_labels=edge_labels, font_size=10, font_family="Microsoft YaHei", ax=ax)

    if highlight_path:
        route = " -> ".join(spot_name(i) for i in highlight_path)
        ax.set_title(f"{title}\n最短路径：{route}", fontsize=14)
    else:
        ax.set_title(title, fontsize=15)

    ax.axis("off")
