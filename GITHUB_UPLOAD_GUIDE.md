# 🚀 GitHub 上传和部署指南

本指南将帮助你将项目上传到 GitHub 并部署到 Streamlit Cloud，让其他人通过网址直接访问。

## 📋 准备清单

- [x] 敏感数据已排除（`.gitignore` 已配置）
- [x] 部署文档已创建（`DEPLOYMENT.md`）
- [x] Requirements 文件已准备
- [x] Streamlit 配置文件已准备
- [x] Secrets 示例文件已创建

## 步骤 1️⃣：检查敏感数据

确保以下文件**不会**被上传到 GitHub：

```bash
# 检查 git 状态
cd "/Users/caddyzhang/Documents/X_Codes/Caddy's data"
git status

# 确认以下文件被忽略：
# .streamlit/secrets.toml
# data/raw/*
# data/processed/*
# *.pyc, __pycache__
```

### ⚠️ 重要提醒

如果 `.streamlit/secrets.toml` 出现在 git status 中：
```bash
# 立即从 git 追踪中移除
git rm --cached dashboards/coffee_import_export/.streamlit/secrets.toml
```

## 步骤 2️⃣：初始化 Git 仓库（如果还没有）

```bash
cd "/Users/caddyzhang/Documents/X_Codes/Caddy's data"

# 检查是否已经是 git 仓库
git status

# 如果不是，初始化
git init

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/Caddy336/Work-Data.git

# 或者如果已经设置过，检查
git remote -v
```

## 步骤 3️⃣：提交代码

```bash
# 添加所有文件（.gitignore 会自动排除敏感文件）
git add .

# 检查将要提交的文件
git status

# 确认没有敏感文件后，提交
git commit -m "feat: 添加咖啡进出口数据分析仪表盘

- 实现月度和累计九宫格可视化
- 支持坚果云实时数据同步
- 国家专属配色方案
- 历史数据对比分析
- 完整的部署文档"

# 推送到 GitHub
git push -u origin main

# 如果是第一次推送，可能需要：
# git branch -M main
# git push -u origin main
```

### 🔐 如果需要 GitHub 认证

**方法 1：Personal Access Token（推荐）**

1. 访问 GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. 勾选 `repo` 权限
4. 复制生成的 token
5. 推送时使用 token 作为密码

**方法 2：SSH Key**

```bash
# 生成 SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥
cat ~/.ssh/id_ed25519.pub

# 添加到 GitHub：Settings → SSH and GPG keys → New SSH key
# 然后修改远程 URL
git remote set-url origin git@github.com:Caddy336/Work-Data.git
```

## 步骤 4️⃣：部署到 Streamlit Cloud

### 4.1 注册 Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 点击 "Sign up with GitHub"
3. 授权 Streamlit 访问你的 GitHub 仓库

### 4.2 创建新应用

1. 点击 "New app"
2. 填写配置：
   - **Repository**: `Caddy336/Work-Data`
   - **Branch**: `main`
   - **Main file path**: `dashboards/coffee_import_export/app_enhanced.py`
   - **App URL**: 选择一个自定义域名（如 `coffee-trade-analysis`）

### 4.3 配置 Secrets

点击 "Advanced settings"，在 "Secrets" 中添加：

```toml
[nutstore]
email = "你的坚果云邮箱"
app_password = "你的坚果云应用密码"
```

**获取坚果云应用密码**：
1. 登录 [坚果云网页版](https://www.jianguoyun.com/)
2. 右上角账户名 → 账户信息
3. 安全选项 → 第三方应用管理
4. 添加应用，生成应用密码

### 4.4 部署

1. 点击 "Deploy!" 按钮
2. 等待构建（约 2-3 分钟）
3. 构建成功后，会自动打开应用

### 4.5 获取分享链接

部署成功后，你会得到一个链接，格式如：
```
https://coffee-trade-analysis.streamlit.app
```

## 步骤 5️⃣：测试和验证

### 检查清单

- [ ] 应用能正常打开
- [ ] 可以从坚果云加载数据
- [ ] 月度九宫格显示正常
- [ ] 累计九宫格显示正常
- [ ] 颜色和格式正确
- [ ] 交互功能正常（缩放、悬停等）

### 如果遇到问题

**问题 1：应用无法启动**
- 检查 `requirements.txt` 是否完整
- 查看 Streamlit Cloud 的日志（Manage app → Logs）

**问题 2：坚果云连接失败**
- 检查 Secrets 配置是否正确
- 确认应用密码没有过期
- 查看错误信息

**问题 3：数据显示错误**
- 检查数据文件格式
- 查看控制台错误信息
- 尝试本地运行调试

## 步骤 6️⃣：自动更新设置

配置完成后，每次推送代码到 GitHub：

```bash
# 修改代码后
git add .
git commit -m "描述你的修改"
git push

# Streamlit Cloud 会自动检测并重新部署
```

### 手动重启应用

在 Streamlit Cloud：
1. 找到你的应用
2. 点击 "⋮" → "Reboot app"

## 步骤 7️⃣：分享应用

现在你可以把链接分享给其他人了！

### 分享链接示例

```
🔗 应用链接：https://your-app-name.streamlit.app
📂 GitHub 仓库：https://github.com/Caddy336/Work-Data
📖 使用文档：查看 DEPLOYMENT.md
```

### 嵌入到网站

可以用 iframe 嵌入：
```html
<iframe 
  src="https://your-app-name.streamlit.app/?embed=true" 
  height="700" 
  style="width:100%;border:none;">
</iframe>
```

## 📊 监控和维护

### 查看使用统计

在 Streamlit Cloud 控制台：
- Analytics：查看访问量
- Logs：查看运行日志
- Settings：修改配置

### 更新 Secrets

1. Streamlit Cloud → 应用 → Settings
2. 修改 Secrets
3. 保存后会自动重启

### 设置自定义域名（可选）

Streamlit Cloud 免费版使用默认域名。如需自定义域名，需要：
1. 升级到付费计划
2. 配置 CNAME 记录

## 🔒 安全最佳实践

1. **永远不要**在代码中硬编码密码
2. 使用 `.gitignore` 排除敏感文件
3. 定期更换坚果云应用密码
4. 为 GitHub 启用两步验证
5. 限制 Secrets 的访问权限

## 📚 相关文档

- [Streamlit 部署文档](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [GitHub 快速入门](https://docs.github.com/cn/get-started/quickstart)
- [坚果云 WebDAV 指南](https://help.jianguoyun.com/?p=2064)

## ❓ 常见问题

**Q: 如果不小心把 secrets.toml 推送到 GitHub 怎么办？**

A: 立即采取行动：
```bash
# 1. 从 Git 历史中完全删除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch dashboards/coffee_import_export/.streamlit/secrets.toml" \
  --prune-empty --tag-name-filter cat -- --all

# 2. 强制推送
git push origin --force --all

# 3. 立即更改坚果云应用密码
# 4. 在 Streamlit Cloud 中更新 Secrets
```

**Q: 部署后如何更新代码？**

A: 直接 push 到 GitHub，Streamlit Cloud 会自动更新：
```bash
git add .
git commit -m "更新说明"
git push
```

**Q: 可以部署多个版本吗？**

A: 可以，为不同分支创建不同的应用：
- `main` 分支 → 生产环境
- `dev` 分支 → 测试环境

---

## ✅ 完成！

按照以上步骤，你的应用现在应该已经：
- ✅ 代码安全地上传到 GitHub
- ✅ 应用部署到 Streamlit Cloud
- ✅ 可以通过 URL 访问
- ✅ 自动更新机制已配置

🎉 恭喜！现在任何人都可以通过你的分享链接访问这个数据分析仪表盘了！
