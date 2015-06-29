# nobot

一个小说抓取项目，先支持贴吧小说抓取

## 功能列表

- 创建新的小说
- 抓取获取章节列表，显示Process
- 抓取章节内容，生成TXT文件，显示Process
- 获取章节列表，在线阅读
- 定期同步


## 结构

- 基于Flask的API
- 基于celery的任务调度，使用Redis作为Broker 和 Backend
- 基于SQLAlchemy的ORM
- 前端框架待定

