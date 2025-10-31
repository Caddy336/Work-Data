#!/bin/bash

#!/bin/bash

# 咖啡进口数据可视化应用启动脚本

echo "☕ 启动咖啡进口数据分析应用..."

# 激活虚拟环境（如果存在）
if [ -d "../../../venv" ]; then
    source ../../../venv/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 启动 Streamlit 应用
streamlit run app_enhanced.py --server.port 8501

echo "🚀 应用正在运行: http://localhost:8501"
echo ""
echo "📊 功能特点："
echo "  ✅ 坚果云实时数据 + 本地 CSV"
echo "  ✅ 月度九宫格可视化"
echo "  ✅ 累计九宫格可视化"
echo "  ✅ 预测功能"
echo ""
echo "🌐 应用将在浏览器中打开: http://localhost:8504"
echo ""

# 进入应用目录
cd "$(dirname "$0")"

# 启动 Streamlit 应用
streamlit run app_enhanced.py --server.port 8504
