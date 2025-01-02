# Pandoc 文件转换器

一个基于 Flask 和 Pandoc 的 Web 应用，用于将 Word 和 HTML 文件批量转换为 Markdown 格式。

## 功能特点

- ✨ 支持 Word (.docx) 转 Markdown
- 🌐 支持 HTML 转 Markdown
- 📦 支持批量文件转换
- 🔄 实时转换状态反馈
- ⬇️ 转换完成后可直接下载

## 环境要求

- Python 3.x
- Flask
- Pandoc >= 3.1.6

## 快速开始

1. 克隆项目：
   bash
   git clone https://github.com/new-mars/pandoc-converter.git
   cd pandoc-converter
2. 安装依赖：
   bash
   pip install -r requirements.txt
3. 安装 Pandoc：

   - Windows: 从 [Pandoc Releases](https://github.com/jgm/pandoc/releases/latest) 下载安装包
   - macOS: `brew install pandoc`
   - Linux: `sudo apt-get install pandoc`
4. 运行应用：
   bash
   python app.py
5. 访问应用：
   在浏览器中打开 http://127.0.0.1:5000

## 使用说明

1. 选择要转换的文件（支持多选）
2. 点击对应的转换按钮
3. 等待转换完成
4. 点击下载链接获取转换后的文件

## 项目结构

pandoc-converter/
├── app.py # 主应用程序
├── requirements.txt # Python 依赖
├── README.md # 项目说明
├── use.txt # 使用和维护指南
├── templates/ # HTML 模板
│ └── index.html # 主页面模板
├── uploads/ # 上传文件临时目录
└── output/ # 转换后文件保存目录

## 维护说明

详细的维护说明请参考 [use.txt](use.txt)。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

[您的名字]

## 致谢

- [Pandoc](https://pandoc.org/)
- [Flask](https://flask.palletsprojects.com/)
