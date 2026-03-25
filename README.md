# 🎯 Persona Hub | 客户画像控制台

> **一站式 ICP（理想客户画像）与 Buyer Persona（买家角色）管理系统。**
> 
> 基于 Markdown 驱动，通过 Python 自动化生成极简、现代、零构建成本的交互式控制台。

---

## 🌟 核心特性

- **🚀 零构建部署**：无需 React/Vue 编译环境，主页通过 `build_manifest.py` 自动生成，完美适配 GitHub Pages。
- **📝 Markdown 驱动**：所有的画像数据均以标准 Markdown 存储在 `data/` 目录，支持版本控制与协作。
- **📊 属性矩阵 (Matrix)**：自动提取 Tags 字典，支持多维过滤、关联画像跳转。
- **🤖 AI 助手集成**：内置 Prompt 生成工具，支持从聊天记录一键提炼画像（使用 `/analyze-chat` 指令）。
- **📑 群像洞察**：支持选中多个画像批量打包，生成群像深度洞察报告 Prompt。

---

## 🛠️ 快速开始

### 1. 添加画像数据
将您的 Markdown 文件放入对应的目录：
- `data/icps/`: 存放理想客户画像
- `data/personas/`: 存放买家角色

文件格式示例（需包含 YAML Frontmatter）：
```markdown
---
title: "AI初创企业"
category: "ICP"
tags: ["AI", "B2C", "A轮"]
related_personas: ["CTO_老李"]
---
# 这里是详细内容...
```

### 2. 生成主页
运行 Python 脚本将 Markdown 转换为交互式 HTML：
```bash
python3 build_manifest.py
```
这会更新根目录下的 `index.html`。

### 3. 部署到 GitHub
1. 将此仓库推送至 GitHub。
2. 进入 `Settings` > `Pages`。
3. 在 `Build and deployment` > `Source` 保持 `Deploy from a branch`。
4. 确保分支选择的是 `main` (或根目录 `/root`)。
5. **自动化运行**：仓库已内置 GitHub Action，您推送 `data/` 目录的修改后，`index.html` 会自动重建并上线。

---

## 📁 项目结构

```text
├── .github/workflows/    # GitHub 自动化构建流
├── data/                 # 核心数据目录 (Markdown)
│   ├── icps/            # 理想客户画像
│   └── personas/        # 买家角色画像
├── build_manifest.py     # 主页自动构建脚本
└── index.html            # 最终生成的交互式控制台
```

---

## 🎨 视觉预览

*(这里可以放置您的控制台截图)*

---

## 💡 提示

本项目专为高增长团队和产品经理设计，用于将琐碎的客户聊天记录沉淀为可指导业务的结构化资产。
