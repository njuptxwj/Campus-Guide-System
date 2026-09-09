# -*- coding: utf-8 -*-
"""校园导游系统 - 图形界面"""

import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import campus_guide as cg

# 界面字体配置
FONT_FAMILY = "Microsoft YaHei"
FONT_TITLE = (FONT_FAMILY, 20, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 16)
FONT_NORMAL = (FONT_FAMILY, 14)
FONT_BUTTON = (FONT_FAMILY, 14)
FONT_LIST = (FONT_FAMILY, 14)
FONT_TEXT = (FONT_FAMILY, 14)
FONT_LF = (FONT_FAMILY, 14, "bold")


class CampusGuideApp:
    def __init__(self, root):
        self.root = root
        self.graph = cg.build_graph()
        self.spot_options = [cg.spot_label(i) for i in sorted(cg.SPOTS)]
        self.highlight_path = None

        cg.setup_matplotlib()
        self._setup_style()
        self._setup_window()
        self._build_ui()
        self._draw_map()

    def _setup_style(self):
        """统一 ttk 控件字体（ttk 默认字体偏小）"""
        style = ttk.Style()
        style.configure(".", font=FONT_NORMAL)
        style.configure("TLabel", font=FONT_NORMAL)
        style.configure("TButton", font=FONT_BUTTON, padding=6)
        style.configure("TCombobox", font=FONT_NORMAL, padding=4)
        style.configure("TLabelframe.Label", font=FONT_LF)
        self.root.option_add("*TCombobox*Listbox*Font", FONT_LIST)
        self.root.option_add("*Font", FONT_NORMAL)

    def _setup_window(self):
        self.root.title("校园导游系统")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 600)

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        left = ttk.Frame(main, width=380)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        left.grid_propagate(False)

        ttk.Label(left, text="校园导游系统", font=FONT_TITLE).pack(anchor="w", pady=(0, 4))
        ttk.Label(
            left,
            text=f"共 {len(cg.SPOTS)} 个景点",
            font=FONT_SUBTITLE,
            foreground="#666",
        ).pack(anchor="w", pady=(0, 16))

        intro_frame = ttk.LabelFrame(left, text="景点简介", padding=10)
        intro_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(intro_frame, text="选择景点：", font=FONT_NORMAL).pack(anchor="w")
        self.spot_var = tk.StringVar(value=self.spot_options[0])
        spot_combo = ttk.Combobox(
            intro_frame, textvariable=self.spot_var,
            values=self.spot_options, state="readonly",
        )
        spot_combo.pack(fill=tk.X, pady=(4, 0))
        spot_combo.bind("<<ComboboxSelected>>", lambda _: self._on_query_intro())

        self.intro_text = tk.Text(intro_frame, height=5, wrap=tk.WORD, font=FONT_TEXT)
        self.intro_text.pack(fill=tk.X, pady=(8, 0))
        self.intro_text.config(state=tk.DISABLED)

        route_frame = ttk.LabelFrame(left, text="问路查询", padding=10)
        route_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(route_frame, text="起点：", font=FONT_NORMAL).pack(anchor="w")
        self.start_var = tk.StringVar(value=self.spot_options[0])
        ttk.Combobox(
            route_frame, textvariable=self.start_var,
            values=self.spot_options, state="readonly",
        ).pack(fill=tk.X, pady=(4, 8))

        ttk.Label(route_frame, text="终点：", font=FONT_NORMAL).pack(anchor="w")
        self.target_var = tk.StringVar(value=self.spot_options[-1])
        ttk.Combobox(
            route_frame, textvariable=self.target_var,
            values=self.spot_options, state="readonly",
        ).pack(fill=tk.X, pady=(4, 8))

        btn_row = ttk.Frame(route_frame)
        btn_row.pack(fill=tk.X)
        ttk.Button(btn_row, text="开始问路", command=self._on_route).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))
        ttk.Button(btn_row, text="清除路线", command=self._on_clear_route).pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.route_text = tk.Text(route_frame, height=5, wrap=tk.WORD, font=FONT_TEXT)
        self.route_text.pack(fill=tk.X, pady=(8, 0))
        self.route_text.config(state=tk.DISABLED)

        list_frame = ttk.LabelFrame(left, text="景点列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)

        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.spot_list = tk.Listbox(
            list_frame, font=FONT_LIST,
            yscrollcommand=list_scroll.set, activestyle="none",
        )
        self.spot_list.pack(fill=tk.BOTH, expand=True)
        list_scroll.config(command=self.spot_list.yview)

        for opt in self.spot_options:
            self.spot_list.insert(tk.END, opt)
        self.spot_list.bind("<<ListboxSelect>>", self._on_list_select)

        right = ttk.LabelFrame(main, text="校园地图", padding=10)
        right.grid(row=0, column=1, sticky="nsew")

        self.fig, self.ax = plt.subplots(figsize=(8, 5), dpi=100)
        self.fig.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.02)

        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self._on_query_intro()

    def _set_text(self, widget, content):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, content)
        widget.config(state=tk.DISABLED)

    def _on_list_select(self, _event=None):
        sel = self.spot_list.curselection()
        if not sel:
            return
        label = self.spot_list.get(sel[0])
        self.spot_var.set(label)
        self._on_query_intro()

    def _on_query_intro(self):
        spot_id = cg.parse_spot_label(self.spot_var.get())
        info = cg.get_spot_info(spot_id)
        self._set_text(self.intro_text, info or "未找到该景点。")

    def _on_route(self):
        start = cg.parse_spot_label(self.start_var.get())
        target = cg.parse_spot_label(self.target_var.get())
        if start == target:
            messagebox.showinfo("提示", "起点与终点相同，无需问路。")
            return

        result = cg.dijkstra(self.graph, start, target)
        if result is None:
            messagebox.showwarning(
                "无法到达",
                f"无法从{cg.spot_name(start)}到达{cg.spot_name(target)}！",
            )
            return

        dist, path = result
        self.highlight_path = path
        self._set_text(self.route_text, cg.format_route(start, target, dist, path))
        self._draw_map()

    def _on_clear_route(self):
        self.highlight_path = None
        self._set_text(self.route_text, "")
        self._draw_map()

    def _draw_map(self):
        title = "校园导游地图 - 最短路径" if self.highlight_path else "校园导游地图"
        cg.render_graph(self.ax, self.highlight_path, title=title)
        self.canvas.draw()


def main():
    root = tk.Tk()
    CampusGuideApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
