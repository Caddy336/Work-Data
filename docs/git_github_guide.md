# Git & GitHub 使用指南

本文档提供了在数据分析项目中使用Git和GitHub的最佳实践指南。

## 1. 基本工作流程

### 日常工作流程
```bash
# 1. 查看工作区状态
git status

# 2. 查看修改内容
git diff

# 3. 暂存修改
git add .  # 添加所有修改
# 或者选择性添加
git add notebooks/specific_notebook.ipynb
git add src/specific_file.py

# 4. 提交修改
git commit -m "描述性的提交信息"

# 5. 推送到GitHub
git push origin main
```

### 提交信息规范
使用清晰的提交信息前缀：
- `[DATA]` - 数据相关更改
- `[NOTEBOOK]` - Jupyter notebook更新
- `[SRC]` - 源代码更改
- `[CONFIG]` - 配置文件更改
- `[DOC]` - 文档更新

示例：
```bash
git commit -m "[NOTEBOOK] 添加客户分析可视化"
git commit -m "[DATA] 更新2025年Q3销售数据"
```

## 2. 分支管理策略

### 主要分支
- `main`: 主分支，保持稳定
- `develop`: 开发分支，用于集成新功能
- `feature/*`: 特性分支，用于开发新功能
- `analysis/*`: 分析分支，用于特定的数据分析任务

### 分支操作
```bash
# 创建新分支
git checkout -b analysis/customer-segmentation

# 切换分支
git checkout main

# 合并分支
git merge analysis/customer-segmentation

# 删除分支（完成后）
git branch -d analysis/customer-segmentation
```

## 3. 数据文件管理

### 大文件处理
对于大型数据文件：
1. 使用 `.gitignore` 排除原始数据
2. 保留数据样本用于测试
3. 使用外部存储或数据库存储完整数据集

### 敏感信息保护
1. 使用 `.env` 文件存储敏感配置
2. 确保 `.env` 文件在 `.gitignore` 中
3. 提供 `.env.example` 作为模板

## 4. Jupyter Notebook版本控制

### 最佳实践
1. 提交前清理输出：
   ```bash
   jupyter nbconvert --clear-output --inplace notebook.ipynb
   ```
2. 使用nbstripout自动清理：
   ```bash
   pip install nbstripout
   nbstripout --install
   ```

### 冲突解决
处理notebook冲突：
1. 使用nbdime进行diff和merge：
   ```bash
   pip install nbdime
   nbdime config-git --enable
   ```

## 5. GitHub协作

### Pull Request流程
1. 从main分支创建新分支
2. 在新分支上进行开发
3. 创建Pull Request
4. 代码审查
5. 合并到main分支

### Issue管理
使用Issue跟踪：
- 数据分析任务
- Bug修复
- 功能请求
- 文档更新

### 项目板
使用GitHub项目板组织任务：
- To Do
- In Progress
- Review
- Done

## 6. 备份策略

### 本地备份
1. 定期创建标签：
   ```bash
   git tag -a v1.0.0 -m "第一个稳定版本"
   git push origin v1.0.0
   ```

2. 导出项目快照：
   ```bash
   git archive --format=zip HEAD > project-backup.zip
   ```

### 远程备份
1. 添加多个远程仓库：
   ```bash
   # 添加GitHub备份
   git remote add github https://github.com/username/repo.git
   
   # 添加其他备份位置
   git remote add backup https://other-git-service.com/username/repo.git
   ```

2. 同步到所有远程：
   ```bash
   git push --all github
   git push --all backup
   ```

## 7. 恢复操作

### 撤销修改
```bash
# 撤销工作区修改
git checkout -- filename

# 撤销暂存区修改
git reset HEAD filename

# 撤销提交
git revert commit-hash
```

### 版本回退
```bash
# 回到指定版本
git checkout v1.0.0

# 强制回退
git reset --hard commit-hash
```

## 8. 定期维护

### 仓库清理
```bash
# 清理无用文件
git clean -fd

# 压缩仓库
git gc --aggressive
```

### 日志查看
```bash
# 查看提交历史
git log --pretty=format:"%h - %an, %ar : %s"

# 查看文件历史
git log --follow -p filename
```

## 9. GitHub Pages部署

如果需要展示数据分析结果：
1. 创建 `docs` 目录
2. 在GitHub设置中启用Pages
3. 选择发布分支和目录