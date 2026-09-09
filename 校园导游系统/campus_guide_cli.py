# -*- coding: utf-8 -*-
"""命令行版入口（可选）"""

import sys
import os

import matplotlib.pyplot as plt

import campus_guide as cg


def setup_console():
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stdin.reconfigure(encoding="utf-8")


def draw_graph_popup(highlight_path=None, title="校园导游地图"):
    cg.setup_matplotlib()
    fig, ax = plt.subplots(figsize=(14, 7))
    cg.render_graph(ax, highlight_path, title=title)
    fig.tight_layout()
    plt.show()


def main_cli():
    setup_console()
    graph = cg.build_graph()

    print("欢迎使用校园导游系统（命令行版）！")
    print(f"本校平面图共 {len(cg.SPOTS)} 个景点，南门为来访客人入口。")
    print("提示：运行 python campus_guide_gui.py 可打开图形界面。")

    while True:
        print("\n========== 校园导游系统 ==========")
        print("1. 查看所有景点列表")
        print("2. 查询景点简介")
        print("3. 图形化地图")
        print("4. 问路查询（南门 -> 指定景点）")
        print("0. 退出")
        print("==================================")

        try:
            choice = int(input("请选择：").strip())
        except ValueError:
            print("输入无效。")
            continue

        if choice == 0:
            print("感谢使用，再见！")
            break
        elif choice == 1:
            for i in sorted(cg.SPOTS):
                print(f"  [{i:2d}] {cg.spot_name(i)}")
        elif choice == 2:
            try:
                spot_id = int(input("请输入景点代号：").strip())
                info = cg.get_spot_info(spot_id)
                print(info if info else "代号无效。")
            except ValueError:
                print("输入无效。")
        elif choice == 3:
            draw_graph_popup()
        elif choice == 4:
            try:
                target = int(input("请输入目标景点代号：").strip())
                result = cg.dijkstra(graph, cg.ENTRANCE, target)
                if result is None:
                    print("无法从南门到达该景点！")
                else:
                    dist, path = result
                    print(cg.format_route(cg.ENTRANCE, target, dist, path))
                    if input("高亮显示路径？(y/n)：").strip().lower() == "y":
                        draw_graph_popup(path, "校园导游地图 - 最短路径")
            except ValueError:
                print("输入无效。")
        else:
            print("无效选项。")


if __name__ == "__main__":
    main_cli()
