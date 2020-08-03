#### baidu-zhidao-spiders
### 运行项目

##### 下载代码:

* git clone

```bash
git clone git@github.com:xsxs89757/zhidao.git
```

##### 安装依赖:

```bash
pip install -r requirements.txt
```

```python
# config.json 为项目配置文件

# 配置API服务

MYSQL_*     # mysql数据库相关
QUESTION_*  # 问题相关mysql配置资料  # 暂时未实现相关api
```

#### 启动项目:

```bash    
scrapy run [question_name] [bind_id] -p [start_page end_page] 
例如:scrapy run 成人高考怎么报名？ 1 -p 1 30 
```   

### 使用
```bash
baidu.middlewares #中可更改使用随机代理的方式  由于zhidao.baidu.com大部分的免费代理都被黑名单了，如果需要使用请购买收费分代理ip进行对接
git clone git@github.com:jhao104/proxy_pool.git #获取随机代理方式
```
