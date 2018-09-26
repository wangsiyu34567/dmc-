### Data management component
##### 数据管理组件

---
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;项目中常常有大量的表需要做重复的增删改查功能。Django自带的admin组件虽然能够快速的完成功能，但是对于admin组件我们无法做源码级别的自定制。且admin功能繁多，我们只会用到其中的一部分，白白浪费资源。于是我仿照admin写下了这个数据管理组件。
### 快速使用

---
##### 一.下载：
git clone https://github.com/wangsiyu34567/dmc-.git<br>
##### 二.将组件放到项目下并在需要做数据管理的表所在的app下新建dmc.py文件
![添加dmc.py](http://m.qpic.cn/psb?/V148R1sD4Ykfli/qWcwnmL27G.UIPUWLuDVjdbi66*QNLuVE7mRKSsmhKQ!/b/dFMBAAAAAAAA&bo=vgDcAAAAAAADB0A!&rf=viewer_4)
##### 三.在urls.py内添加url

```py
from dmc.service import dmc

urlpatterns = [
    path('dmc/', dmc.site.urls),
]
```

##### 四.在dmc.py文件内注册需要做数据管理的表

```py
from dmc.service.dmc import site


site.register(Publish)
site.register(Book, BookConfig)
site.register(Author, AuthorConfig)
```

##### 五.定制数据管理页面
- 创建配置类和配置说明

```py
from dmc.service.dmc import site, ModelDmc


class BookConfig(ModelDmc):
    list_display = ["title", "price", "publish", "authers"]  # 要显示的字段
    list_display_link = ["title"]  # 将该字段变为编辑页面的入口
    search_fields = ["title", "price"]  # 可对列表中字段进行查询
    list_filter = ["title", "publish", "authers"]  # 筛选字段

    def patch_init(self, request, queryset):
        queryset.update(price=F("price") - 1)

    patch_init.short_description = "批量初始化"  # 批量处理功能名称
    actions = [patch_init]  # 批量处理函数


site.register(Book, BookConfig)
```
- 效果图
    ![效果图](http://m.qpic.cn/psb?/V148R1sD4Ykfli/sEpRvJhxNtk1aONoa0f8Fe7ap4DfAzQMm7tRiBSs96M!/b/dDcBAAAAAAAA&bo=OQbGAwAAAAADB9g!&rf=viewer_4)
