# 基于分词和关键词提取技术的海事船舶管理系统

## 1 功能描述

+ 上传船舶文档：用户上传海事船舶相关文档（word，pdf，txt）
+ NLP处理：系统读取文档内容，自动进行文档分词、关键词提取以及关键词权重划分。
+ 文档信息检索：用户对已上传文档可以根据关键词、文档标题进行检索。
+ 文档信息修改：用户对已上传的文档可以修改其关键词。
+ 文档信息查看：用户可以查看文档的分词信息、关键词信息以及关键字权重信息。
+ 用户身份验证：对用户密码进行散列值处理、注册用户时支持电子邮件确认。
+ 用户角色划分：用户分为管理员、普通用户、游客。管理员具有上传文档权限，普通用户具有查看文档权限，不具备上传文档权限。游客只具备查看文档关键词权限。

## 2 技术简介

+ 系统：window
+ 环境：python3.7
+ IDE环境：pycharm
+ web技术：Flask
+ NLP技术：jieba
+ 依赖包：详见主目录下的requirements.txt文件

## 3 技术详解

### 3.1 jieba分词

#### 3.1.1 jieba介绍
Jieba 是一款Python 中文分词组件。

#### 3.1.2 jieba原理
+ 基于前缀词典实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图 (DAG)
+ 采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合
+ 对于未登录词，采用了基于汉字成词能力的 HMM 模型，使用了 Viterbi 算法
+ 关键词提取：基于TF-IDF关键词抽取算法和基于TextRank关键词抽取算法，两类算法均是无监督学习的算法。

### 3.2 Flask技术
本节分别从Flask的介绍、原理以及优缺点，展示Flask框架。
#### 3.2.1 Flask定义
**Flask**是一个基于Python开发并且依赖jinja2模板和Werkzeug WSGI服务的一个微型框架。
Flask 旨在保持核心简单而易于扩展。Flask不会为开发人员制定过多约束，比如用户登陆状态记录，开发人员可以使用传统的session与cookie，同时也可以选择Flask已经封装好的Flask-login接口。这些接口只需要引入，没有太多约束，同时不实用也不会有任何影响。并且Flask 所选择的固有约束，如Flask默认使用的模板引擎Jinja2，则很容易兼容、替换。除此之外的一切都可由开发人员掌握。

#### 3.2.2 Flask原理
Flask使用**werkzeug**（一个WSGI实用程序库）来做路由分发。使用**Jinja2**（Python的一个完整的特性模板引擎。它有完整的unicode支持，拥有可选的集成沙箱执行环境，并且广泛使用和BSD许可）来做模板渲染
从web的一般流程来分析，当客户端希望获取某种资源时，向指定的url发送一个HTTP请求，通过网络的路由转发，此时Web应用程序就会在服务器后台进行相应的业务处理，服务器后台根据HTTP协议的解析，获取用户传送数据，并返回用户需要数据，同样以HTTP协议传送给客户端。

#### 3.2.3 Flask优缺点
+ 优点：
1. 简单，Flask的路由以及路由函数由修饰器设定，开发人员不需要借助其他文件匹配；
2. 配置灵活，有多种方法配置，不同环境的配置也非常方便；环境部署简单，Flask运行不需要借助其他任何软件，只需要安装了Python的IDE，在命令行运行即可。只需要在Python中导入相应包即可满足所有需求；
3. 入门简单，通过官方指南便可以清楚的了解Flask的运行流程；
4. 低耦合，Flask可以兼容多种数据库、模板。

+ 缺点：
1. 对于大型网站开发，需要设计路由映射的规则，否则导致代码混乱。

### 4 软件说明

#### 4.1 结构说明

/app:主要功能实现  
&nbsp;&nbsp;&nbsp;&nbsp;/auth: 登陆注册功能，包括：表单功能、报错功能、路由功能  
&nbsp;&nbsp;&nbsp;&nbsp;/main: 软件功能，包括：表单功能、报错功能、路由功能  
&nbsp;&nbsp;&nbsp;&nbsp;/static:辅助文件，包括css、ico、js  
&nbsp;&nbsp;&nbsp;&nbsp;/template:前端文件，包括html  
&nbsp;&nbsp;&nbsp;&nbsp;models.py:数据库表，包括用户、角色、文件等数据库表  
/files:用户上传的文件路径  
/migrations:迁移仓库相关  
/nlp:自然语言处理相关  
&nbsp;&nbsp;&nbsp;&nbsp;loader.py:读取文件  
&nbsp;&nbsp;&nbsp;&nbsp;process.py:对文件内容进行分词、关键词提取、关键词权重度量  
/tests:软件测试相关  
/venv:pyhton虚拟环境  
config.py:Flask配置环境  
flasky.py:启动程序  
requirements.txt:相关依赖包   

#### 4.2 环境配置
python3.7、pycharmIDE


#### 临时-查看改变
https://github.com/yongqiangyang/flask_Ship-Knowledge-Management-System/compare/v1.0...v3.0
