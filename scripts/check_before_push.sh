#!/bin/bash

echo "🔍 检查敏感文件是否被 Git 追踪..."
echo ""

# 检查 secrets.toml
if git ls-files | grep -q "secrets.toml"; then
    echo "❌ 警告：发现 secrets.toml 在 Git 追踪中！"
    echo "   执行以下命令移除："
    echo "   git rm --cached **/secrets.toml"
    echo ""
else
    echo "✅ secrets.toml 未被追踪"
fi

# 检查数据文件
if git ls-files | grep -q "data/raw/.*\.csv\|data/raw/.*\.xlsx"; then
    echo "❌ 警告：发现原始数据文件在 Git 追踪中！"
    echo "   这些文件可能包含敏感数据"
    echo ""
else
    echo "✅ 原始数据文件未被追踪"
fi

# 检查日志文件
if git ls-files | grep -q "logs/.*\.log"; then
    echo "⚠️  警告：发现日志文件在 Git 追踪中"
    echo ""
else
    echo "✅ 日志文件未被追踪"
fi

# 检查配置文件
if git ls-files | grep -q "config/.*\.json\|config/.*\.yaml"; then
    echo "⚠️  警告：发现配置文件在 Git 追踪中"
    echo "   请检查是否包含密码或密钥"
    echo ""
fi

echo ""
echo "📋 将要提交的文件列表："
git ls-files | grep "dashboards/coffee_import_export" | head -20

echo ""
echo "💡 提示："
echo "   - 如果发现敏感文件，使用: git rm --cached <file>"
echo "   - 检查完成后，可以提交: git add . && git commit -m 'your message'"
echo "   - 推送到 GitHub: git push"
