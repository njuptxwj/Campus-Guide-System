# 校园导游系统 (Campus Guide System)

基于图论的校园景点导游与最短路径查询系统。以无向加权图建模校园拓扑，采用 **Dijkstra** 算法求解任意两点间最短路径，并提供图形界面（Tkinter + Matplotlib）与命令行两种交互方式。

本仓库面向课程设计 / 算法实验复现：克隆后即可运行；通过修改少量数据即可替换为任意校园地图。

---

## 目录

- [功能特性](#功能特性)
- [项目结构](#项目结构)
- [环境依赖](#环境依赖)
- [安装与复现](#安装与复现)
- [快速开始](#快速开始)
- [使用说明](#使用说明)
- [自定义校园地图](#自定义校园地图)
- [算法说明](#算法说明)
- [可选：生成课程报告](#可选生成课程报告)
- [常见问题](#常见问题)
- [许可证](#许可证)

---

## 功能特性

| 功能 | 说明 |
|------|------|
| 景点查询 | 按代号 / 名称查看景点简介 |
| 问路查询 | 任选起点、终点，计算最短路径与总距离（米） |
| 路径可视化 | 在校园拓扑图上高亮显示最短路线 |
| 双入口 | GUI 图形界面 / CLI 命令行 |
| 可扩展 | 景点、边权、节点坐标均集中配置，便于替换为本校地图 |

---

## 项目结构

```text
校园导游系统/
├── campus_guide.py          # 核心：景点数据、图构建、Dijkstra、地图绘制
├── campus_guide_gui.py      # 图形界面入口（推荐）
├── campus_guide_cli.py      # 命令行入口（可选）
├── draw_flowcharts.py       # （可选）生成报告用流程图
├── generate_report.py       # （可选）生成课程设计 Word 报告
├── requirements.txt         # Python 依赖
└── README.md
```

核心逻辑与界面分离：修改地图数据只需编辑 `campus_guide.py` 中的配置常量，无需改动 GUI/CLI。

---

## 环境依赖

### 系统要求

- **Python** ≥ 3.8（建议 3.9+）
- **操作系统**：Windows / macOS / Linux
- GUI 模式需要可用的桌面环境（Tkinter 一般为 Python 自带）
- 中文显示：Windows 通常自带「微软雅黑 / 黑体」；Linux / macOS 若缺中文字体，请安装对应字体，否则图标签可能乱码

### Python 包

主程序依赖（见 `requirements.txt`）：

```text
networkx>=3.0
matplotlib>=3.7
```

可选（仅生成 Word 报告时需要）：

```text
python-docx
```

标准库使用：`tkinter`、`heapq` 等，无需额外安装。

---

## 安装与复现

以下步骤可完整复现本项目运行环境。

### 1. 克隆仓库

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

> 上传后请将上方 URL 替换为你的实际仓库地址。

### 2. 创建虚拟环境（推荐）

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证安装

```bash
python -c "import networkx, matplotlib; print('OK')"
```

---

## 快速开始

### 图形界面（推荐）

```bash
python campus_guide_gui.py
```

启动后将打开「校园导游系统」窗口：左侧查询景点与问路，右侧显示校园拓扑图；点击「开始问路」后路径以红色高亮。

### 命令行

```bash
python campus_guide_cli.py
```

按菜单提示操作（景点列表、简介查询、弹窗地图、最短路径查询等）。

---

## 使用说明

### GUI

1. **景点简介**：下拉框或左侧列表选择景点，查看代号、名称与简介。
2. **问路查询**：选择起点、终点 →「开始问路」→ 文本区显示路径与距离，地图高亮路线。
3. **清除路线**：恢复未高亮的完整校园图。

### CLI

| 选项 | 功能 |
|------|------|
| 1 | 查看所有景点列表 |
| 2 | 按代号查询简介 |
| 3 | 弹出图形化地图 |
| 4 | 从南门（默认入口）到指定景点的最短路径 |
| 0 | 退出 |

---

## 自定义校园地图

地图数据全部集中在 `campus_guide.py` 顶部，修改下列四处即可替换为**任意学校 / 园区**的拓扑图，无需改算法与界面代码。

### 1. 景点字典 `SPOTS`

格式：`代号: (名称, 简介)`

```python
SPOTS = {
    0: ("南门", "学校南侧主入口，来访客人登记处。"),
    1: ("教学楼1", "主要公共课教学区，设施完善。"),
    # ... 按本校实际情况增删
}
```

### 2. 边与权重 `EDGES`

无向边列表：`(点A, 点B, 距离米)`。边会自动建成双向。

```python
EDGES = [
    (0, 1, 120),   # 南门 ↔ 教学楼1，120 米
    (0, 6, 250),
    # ...
]
```

### 3. 默认入口 `ENTRANCE`

CLI 问路默认起点（GUI 可任选起终点）：

```python
ENTRANCE = 0  # 改为你的校门 / 入口代号
```

### 4. 可视化坐标 `NODE_POS`

用于 Matplotlib / NetworkX 布局，**不必是真实经纬度**，保持相对位置合理即可：

```python
NODE_POS = {
    0: (0.0, 0.0),
    1: (1.5, 0.0),
    # 每个 SPOTS 中的代号都应有对应坐标
}
```

### 自定义检查清单

- [ ] `SPOTS` 中每个代号在 `NODE_POS` 中都有坐标
- [ ] `EDGES` 中的端点代号均存在于 `SPOTS`
- [ ] 图连通（或接受部分点对不可达；算法会提示无法到达）
- [ ] 边权为正数（Dijkstra 前提）
- [ ] 修改后重新运行 `python campus_guide_gui.py` 验证

### 最小示例（示意）

若只需演示三节点一线：

```python
SPOTS = {
    0: ("校门", "入口"),
    1: ("图书馆", "阅览"),
    2: ("食堂", "就餐"),
}
EDGES = [(0, 1, 100), (1, 2, 80)]
ENTRANCE = 0
NODE_POS = {0: (0, 0), 1: (1, 0), 2: (2, 0)}
```

---

## 算法说明

### 图模型

- 景点 → 顶点  
- 道路 → 无向边  
- 步行距离（米）→ 非负边权  

### 最短路径：Dijkstra

实现位于 `campus_guide.dijkstra`：

- 优先队列（`heapq`）维护候选距离  
- 松弛更新邻接边  
- 回溯 `prev` 还原完整路径  

时间复杂度约为 \(O((V + E)\log V)\)（堆实现）。

### 可视化

- `networkx` 构建图结构  
- `matplotlib` 绘制节点、边权与高亮路径  
- GUI 通过 `FigureCanvasTkAgg` 嵌入 Tkinter  

---

## 可选：生成课程报告

若需自动生成流程图与 Word 报告：

```bash
pip install python-docx
python draw_flowcharts.py    # 生成 report_images/ 下流程图
python generate_report.py    # 生成课程设计报告 .docx
```

报告脚本依赖本仓库示例数据与流程说明，自定义地图后如需写入报告，请同步修改 `generate_report.py` 中的文字描述。

---

## 常见问题

**Q: GUI 启动报错找不到 tkinter？**  
A: Linux 需单独安装，例如 `sudo apt install python3-tk`。

**Q: 地图中文显示为方框？**  
A: 安装中文字体，或在 `setup_matplotlib()` 中把 `font.sans-serif` 改为本机已有字体名。

**Q: 修改了 SPOTS 但界面没变？**  
A: 确认保存的是 `campus_guide.py`，并重新启动程序（勿只重启部分模块缓存）。

**Q: 上传 GitHub 时要忽略哪些文件？**  
A: 建议忽略虚拟环境与缓存，例如：

```gitignore
.venv/
__pycache__/
*.pyc
.idea/
report_images/
*.docx
```

---

## 许可证

本项目可用于学习、课程设计与二次开发。若公开仓库，可自行补充 `LICENSE`（如 MIT）。

---

## 致谢 / 说明

本系统为数据结构与算法相关课程实践项目：用图结构表示校园道路网，并用经典最短路径算法完成导游问路。欢迎 Fork 后替换 `SPOTS` / `EDGES` / `NODE_POS`，适配你自己的校园地图。
