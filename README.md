这是一个上海闻泰通讯软件内部工作台。当前只适用在linux主机下，后面会兼容windows系统。


软件版本：
  V1.0.0

开发环境：
  Ubuntu 12.04
  Python 2.7
  wxpython 2.8

开发者：
  周沿江
  zhouyanjiang@wingtech.com
  15000032998

角色介绍： 
  Administartor 工作台管理员，最高权限
  SCM           配置管理员，可处理Engineer提交的各种表单，同时拥有Engineer的权限
  Engineer      软件工程师，可填写表单和使用通用工具

功能介绍：
  1. 申请权限： Engineer填写表单申请gerrit svn相应权限
  2. 申请GIT：  Engineer填写表单申请base分支下的git库
  3. 申请分支： Engineer填写表单申请基于base分支创建新分支
  4. 申请构建： Engineer填写表单申请项目的dailybuild
  5. 申请编译： Engineer填写表单申请定时编译版本
  6. 查询分支： 根据条件查询相应分支名
  7. 拉取代码： 根据分支名拉去整体或部分代码
  8. 工具集合： 字串工具/APN工具/图片处理工具集等等

  
