# owod
开放世界目标检测

# 注意
需要使用Vue2，不能使用Vue3，否则d3.lasso组件会报错

```shell
//安装2版本的vue-cli
npm install -g vue-cli
//vue2创建工程专用语法
vue init webpack project_name
```

### 环境搭建 ###

#### 前端环境

首先要保证node和npm版本一致
- node版本：v16.19.0
- npm版本: 8.19.3

之后在owod文件夹内执行命令行

```shell
//安装组件
npm install
//运行程序
npm run dev
```

#### 后端环境

在 python_script 文件夹中，运行 app.py 文件，如果 import 报错，就 pip 下载，比如：

```shell
pip install Flask
```

