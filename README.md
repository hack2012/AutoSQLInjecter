#SQL-Hacker
---

####项目介绍 :  
  
基于Python的SQL盲注利用脚本 , 实现地很简陋  
  
最近几乎刷完了Sqli-labs的题目 , 但是其实感觉好多知识点自己都没有学习到  
写这个工具只是为了学习SQL注入的原理 , 虽然说已经有SQLMAP这样的如此强大的工具了  
自己还是不想当脚本小子 , 而且觉得还是自己写的东西用着爽  
那就先自己写 , 看看自己能写到什么样的程度 , 然后再去阅读SQLMAP的源码  
  
---

####运行截图 :  
  
![图片.png](http://upload-images.jianshu.io/upload_images/2355077-d7cb0cac4319424a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
![图片.png](http://upload-images.jianshu.io/upload_images/2355077-3ed9f5c8d92f2f90.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
![图片.png](http://upload-images.jianshu.io/upload_images/2355077-aec6678f81dc95ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
---

####使用说明 :  
```
python sqlhacker.py http://www.xxx.com/index.php?id=1
```
只需要一个参数 , 程序会自动判断是否存在注入点  
如果存在会显示出Payload并自动脱裤  
会自动忽略系统库 , 例如` information_schema/mysql `等  

---

####TODO :  
1. 目前只可以利用Bool盲注 , 以后需要添加时间盲注等等功能  
2. 增加灵活性和可扩展性  
3. 增加帮助文档  
4. 对URL参数进行分离 , 目前只支持一个参数  
5. 对除了mysql以外的数据库进行支持  
6. 目前只支持GET方式 , 以后要对与POST/HTTP头等方式进行支持
7. 关于Bool盲注自动化脚本一直有一个问题 , 就是不知道应该怎么判断是否注入成功 , 感觉根据返回页面的长度来判断不是很靠谱啊
8. 有时候会出现可以找到注入点 , 但是注入的时候出错的情况 , 这个还是因为是通过长度判断的
9. 检测URL是否存在时间盲注漏洞
