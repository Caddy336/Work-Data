# Caddy's Data Analysis Project

这是一个数据分析项目工作区，包含完整的数据分析和可视化环境。

## 项目结构

```
.
├── config/          # 配置文件
├── dashboards/      # 数据可视化面板
├── data/           # 数据文件
│   ├── raw/        # 原始数据
│   ├── interim/    # 中间数据
│   └── processed/  # 处理后的数据
├── logs/           # 日志文件
├── notebooks/      # Jupyter notebooks
├── src/           # Python 源代码
├── templates/      # 模板文件
├── requirements.txt # 项目依赖
└── README.md
```

## 环境设置

1. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 快速开始

1. 运行环境设置notebook：
```bash
jupyter notebook notebooks/workspace_setup.ipynb
```

2. 按照notebook中的步骤完成工作区配置

## 目录说明

- `/config`: 存放配置文件，包括日志配置和数据路径配置
- `/dashboards`: 存放数据可视化面板
- `/data`: 数据文件存储
  - `/raw`: 原始数据
  - `/interim`: 数据处理中间文件
  - `/processed`: 处理后的数据
- `/logs`: 应用日志文件
- `/notebooks`: Jupyter notebooks用于交互式分析
- `/src`: Python源代码
- `/templates`: 模板文件