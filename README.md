### Data management component
##### 数据管理组件

---
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;项目中常常有大量的表需要做重复的增删改查功能。Django自带的admin组件虽然能够快速的完成功能，但是对于admin组件我们无法做源码级别的自定制。且admin功能繁多，我们只会用到其中的一部分，白白浪费资源。于是我仿照admin写下了这个数据管理组件。
### 使用

---
##### 一.下载：
git clone https://github.com/wangsiyu34567/dmc-.git<br>
##### 二.将组件放到项目下并在需要做数据管理的表所在的app下新建dmc.py文件
![添加dmc.py](http://m.qpic.cn/psb?/V148R1sD4Ykfli/qWcwnmL27G.UIPUWLuDVjdbi66*QNLuVE7mRKSsmhKQ!/b/dFMBAAAAAAAA&bo=vgDcAAAAAAADB0A!&rf=viewer_4)
##### 三.在urls.py内添加url
![url示意图](http://m.qpic.cn/psb?/V148R1sD4Ykfli/6QVEUv*RHUYewbrULxS0cEqoiqXvPzCiJHe4sYzTl.8!/b/dDQBAAAAAAAA&bo=vgHbAAAAAAADB0Y!&rf=viewer_4)<br>
##### 四.在dmc.py文件内注册需要做数据管理的表
![注册表示意图](http://m.qpic.cn/psb?/V148R1sD4Ykfli/.EOG..ctyda073vXHeH1wioUwNseRdj93nK1zGti.ls!/b/dDQBAAAAAAAA&bo=kgHGAAAAAAADB3c!&rf=viewer_4)
##### 五.定制数据管理页面
- 创建配置类
    ![定制配置类](http://m.qpic.cn/psb?/V148R1sD4Ykfli/kKn4gM6EqvnS1XCcm3t1Q8RJkTRn0aZmVlUp9ducLMo!/b/dFUAAAAAAAAA&bo=wQHJAAAAAAADBys!&rf=viewer_4)
- 配置变量说明
    ![配置变量说明](http://m.qpic.cn/psb?/V148R1sD4Ykfli/kjlc3Mor0vUDuoqOzuhnyS53iYeGV4RfrWDo8BtMNzo!/b/dDYBAAAAAAAA&bo=vAPRAQAAAAADB00!&rf=viewer_4)
- 效果图
    ![效果图](http://m.qpic.cn/psb?/V148R1sD4Ykfli/sEpRvJhxNtk1aONoa0f8Fe7ap4DfAzQMm7tRiBSs96M!/b/dDcBAAAAAAAA&bo=OQbGAwAAAAADB9g!&rf=viewer_4)
