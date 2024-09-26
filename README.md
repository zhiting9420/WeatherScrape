### 简介
气象数据分析与可视化项目使用Django写的 需要python环境和创建python虚拟环境 创建数据库存放天气数据 开发环境是Pycharm 
### 步骤

1. 打开pycharm终端创建虚拟环境 `python -m venv .venv` 激活虚拟环境 `.venv\Scripts\activate.bat`  安装需要的依赖 `pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple` 

2. Pycharm能自动识别虚拟环境最好 不行就手动选择虚拟环境 pycharm中设置-项目-Python解释器-选择刚刚创建的.venv中的python.exe 记得勾上旁边的"将此虚拟环境与当前项目关联

3. 创建一个数据库 名字下面的配置需要用到 字符类型utf8mb4

4. 修改项目中的settings文件 找到DATABASES 修改成对应的数据库名和账号密码主机号和端口

5. 终端运行命令 创建数据库迁移文件 `python manage.py makemigrations`  执行数据库迁移 `python manage.py migrate` 也就是应用models文件里创建的类

6. 运行项目 输入要爬取的年份 pycharm如果错误可以用终端运行 `python manage.py runserver`

7. 终端运行命令 执行导入CSV文件到数据库命令 `python manage.py import_data weather_data` 其中import_data是存放在management/commands下的自定义导入文件程序 weather_data是CSV文件存放的文件夹路径  显示导入成功可以去数据库weather_weatherrecord表查看数据是否导入成功

8. 复制控制台输出的链接 `http://localhost:8000/` 浏览器粘贴

9. 后面跟上`http://localhost:8000/dashboard/`是展示面板 右上角可以切换显示的月份 `http://localhost:8000/update/`是更新数据的面板 提示成功后要回到终端执行第6点了数据导入命令 再次回到面板页面`http://localhost:8000/dashboard/` 刷新就是新的年份的天气数据了

今天我做了一个测试 发现一个月只能爬取十天的数据 去网站上看发现已经被限制了 提示“获取更多历史天气信息，请联系kf@tianqi.com 网站人工做了限制 所以限制爬虫只能爬取一个月前十天的数据了
