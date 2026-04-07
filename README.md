# ☕ 中国咖啡进出口数据分析

中国咖啡豆进出口数据的可视化分析工具。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python main.py
```

其他命令：
```bash
python main.py --check   # 检查配置
python main.py --test    # 测试坚果云连接
```

## 项目结构

```
.
├── main.py              # 主入口
├── dashboards/          # Streamlit 仪表盘
│   └── coffee_import_export/
├── src/                 # 核心模块
│   ├── visualization/   # 坚果云加载器
│   └── data_processing/ # PostgreSQL 加载器
├── scripts/             # 工具脚本
└── archive/             # 历史数据
```

## 主要功能

- 📊 月度/累计九宫格可视化
- ☁️ 坚果云实时数据同步
- 🔮 趋势预测分析

详细文档见 [dashboards/coffee_import_export/DEPLOYMENT.md](dashboards/coffee_import_export/DEPLOYMENT.md)