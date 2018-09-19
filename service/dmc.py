from django.urls import re_path
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.forms.models import ModelChoiceField

from dmc.utils.page import Pagination


class ShowList:
    def __init__(self, config, data_list, request):
        self.config = config  # ModelDmc()
        self.data_list = data_list
        self.request = request
        self.actions = self.config.new_actions()

        data_count = self.data_list.count()
        current_page = int(request.GET.get("page", 1))
        base_path = request.path
        self.pagination = Pagination(current_page, data_count, base_path, self.request.GET,
                                     per_page_num=10,
                                     pager_count=11)
        self.page_data = self.data_list[self.pagination.start:self.pagination.end]

    # 获取filter过滤信息
    def get_filter_linktags(self):
        link_dict = {}
        for filter_field in self.config.list_filter:
            import copy
            params = copy.deepcopy(self.request.GET)
            cid = self.request.GET.get(filter_field, 0)
            filter_field_obj = self.config.model._meta.get_field(filter_field)
            if isinstance(filter_field_obj, ManyToManyField) or isinstance(filter_field_obj, ForeignKey):
                data_list = filter_field_obj.related_model.objects.all()
            else:
                data_list = self.config.model.objects.all()
            temp = []
            # 处理全部标签
            if params.get(filter_field):
                del params[filter_field]
                temp.append("<a href='?%s'>全部</a>" % params.urlencode())
            else:
                temp.append("<a class='_active' href='#'>全部</a>")

            # 处理数据标签
            for obj in data_list:
                if isinstance(filter_field_obj, ManyToManyField) or isinstance(filter_field_obj, ForeignKey):
                    text = str(obj)
                    params[filter_field] = obj.pk
                else:
                    text = getattr(obj, filter_field)
                    params[filter_field] = text
                _url = params.urlencode()
                if cid == str(obj.pk) or cid == text:
                    link_tag = '<a class="_active" href="?%s">%s</a>' % (_url, text)
                else:
                    link_tag = '<a href="?%s">%s</a>' % (_url, text)
                if link_tag not in temp:
                    temp.append(link_tag)
            link_dict[filter_field] = temp
        return link_dict

    # 将actions里的函数信息格式化
    def get_action_list(self):
        temp = []
        for action in self.actions:
            temp.append({
                "name": action.__name__,
                "desc": action.short_description
            })
        return temp

    # 获取表头信息
    def get_header(self):
        # 构建表单数据
        header_list = []
        for field in self.config.new_list_display():
            if callable(field):
                val = field(self.config, header=True)
            else:
                if field == "__str__":
                    val = self.config.model._meta.model_name.upper()
                else:
                    val = self.config.model._meta.get_field(field).verbose_name
            header_list.append(val)
        return header_list

    # 获取表内容
    def get_body(self):
        # 构建表头数据
        new_data_list = []
        for obj in self.page_data:
            temp = []
            for field in self.config.new_list_display():
                if callable(field):
                    val = field(self.config, obj)
                else:
                    try:
                        field_obj = self.config.model._meta.get_field(field)
                        if isinstance(field_obj, ManyToManyField):
                            obj_list = getattr(obj, field).all()
                            t = []
                            for _obj in obj_list:
                                t.append(str(_obj))
                            val = ','.join(t)
                        else:
                            if field_obj.choices:
                                val = getattr(obj, 'get_' + field + '_display')()
                            else:
                                val = getattr(obj, field)
                            if field in self.config.list_display_link:
                                url = self.config.get_urls("change", obj)
                                val = mark_safe("<a href='%s'>%s</a>" % (url, val))
                    except Exception as e:
                        val = getattr(obj, field)
                temp.append(val)
            new_data_list.append(temp)
        return new_data_list


class ModelDmc:
    list_display = ("__str__",)
    list_display_link = []
    search_fields = []
    actions = []
    list_filter = []

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def batch_delete(self, request, queryset):
        queryset.delete()

    batch_delete.short_description = "批量删除"

    def get_urls(self, action, obj=None):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        if obj:
            _url = reverse("%s_%s_%s" % (app_label, model_name, action), args=(obj.pk,))
        else:
            _url = reverse("%s_%s_%s" % (app_label, model_name, action))
        return _url

    def edit(self, obj=None, header=False):
        if header:
            return "操作"
        url = self.get_urls("change", obj)
        return mark_safe("<a href='%s'>编辑</a>" % url)

    def deletes(self, obj=None, header=False):
        if header:
            return "操作"
        url = self.get_urls("delete", obj)
        return mark_safe("<a href='%s'>删除</a>" % url)

    def checkbox(self, obj=None, header=False):
        if header:
            return mark_safe("<input id='choice' type='checkbox'>")
        return mark_safe("<input class='choice_item' type='checkbox' name='selected_pk' value='%s'>" % obj.pk)

    def get_modelform_class(self):
        class ModelFormsDemo(ModelForm):
            class Meta:
                model = self.model
                fields = "__all__"

        return ModelFormsDemo

    def add_view(self, request):
        ModelFormsDemo = self.get_modelform_class()
        form = ModelFormsDemo()
        pop_field = request.GET.get('pop_field')
        if request.method == "POST":
            form = ModelFormsDemo(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save()
                if pop_field:
                    return render(request, "../templates/pop_mode.html",
                                  {"pk": obj.pk, "text": str(obj), "pop_field": pop_field})
                return redirect(self.get_urls("list"))
        for bfield in form:
            if isinstance(bfield.field, ModelChoiceField):
                bfield.is_pop = True
                releted_model_name = bfield.field.queryset.model._meta.model_name
                releted_app_label = bfield.field.queryset.model._meta.app_label
                _url = reverse("%s_%s_add" % (releted_app_label, releted_model_name))
                bfield.url = _url + "?pop_field=id_%s" % bfield.name
        if pop_field:
            return render(request, "../templates/form.html", {"form": form})
        return render(request, "../templates/add_view.html", {"form": form})

    def delete_view(self, request, id):
        url = self.get_urls("list")
        if request.method == "POST":
            self.model.objects.filter(pk=id).delete()
            return redirect(url)
        return render(request, "../templates/delete_view.html", locals())

    def change_view(self, request, id):
        ModelFormsDemo = self.get_modelform_class()
        edit_obj = self.model.objects.filter(pk=id).first()
        form = ModelFormsDemo(instance=edit_obj)
        if request.method == "POST":
            form = ModelFormsDemo(request.POST, request.FILES, instance=edit_obj)
            if form.is_valid():
                obj = form.save()
                pop_field = request.GET.get('pop_field')
                if pop_field:
                    return render(request, "../templates/pop_mode.html",
                                  {"pk": obj.pk, "text": str(obj), "pop_field": pop_field})
                return redirect(self.get_urls("list"))
        for bfield in form:
            if isinstance(bfield.field, ModelChoiceField):
                bfield.is_pop = True
                releted_model_name = bfield.field.queryset.model._meta.model_name
                releted_app_label = bfield.field.queryset.model._meta.app_label
                _url = reverse("%s_%s_add" % (releted_app_label, releted_model_name))
                bfield.url = _url + "?pop_field=id_%s" % bfield.name
        return render(request, "../templates/change_view.html", locals())

    def new_list_display(self):
        new_list = []
        new_list.append(ModelDmc.checkbox)
        new_list.extend(self.list_display)
        if not self.list_display_link:
            new_list.append(ModelDmc.edit)
        new_list.append(ModelDmc.deletes)
        return new_list

    def new_actions(self):
        temp = []
        temp.append(ModelDmc.batch_delete)
        temp.extend(self.actions)
        return temp

    # 获取搜索框过滤信息
    def get_search_condition(self, request):
        self.key_words = request.GET.get("q", "")
        search_connection = Q()
        if self.key_words:
            search_connection.connector = "or"
            for search_field in self.search_fields:
                search_connection.children.append((search_field + "__contains", self.key_words))
        return search_connection

    def get_filter_condition(self, request):
        filter_condition = Q()
        for filter_filed, val in request.GET.items():
            if filter_filed != "page":
                filter_condition.children.append((filter_filed, val))
        return filter_condition

    def list_view(self, request):
        if request.method == "POST":
            action = request.POST.get("action")
            if action:
                selected_pk = request.POST.getlist("selected_pk")
                action_func = getattr(self, action)
                queryset = self.model.objects.filter(pk__in=selected_pk)
                action_func(request, queryset)

        search_connection = self.get_search_condition(request)

        filter_condition = self.get_filter_condition(request)

        data_list = self.model.objects.filter(search_connection).filter(filter_condition)
        showlist = ShowList(self, data_list, request)

        add_url = self.get_urls("add")
        return render(request, "../templates/list_view.html", {"showlist": showlist, "add_url": add_url})

    def extra_url(self):
        return []

    def get_urls2(self):
        temp = []
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        temp.append(re_path(r"^add/$", self.add_view, name="%s_%s_add" % (app_label, model_name)))
        temp.append(re_path(r"^(\d+)/delete/$", self.delete_view, name="%s_%s_delete" % (app_label, model_name)))
        temp.append(re_path(r"^(\d+)/change/$", self.change_view, name="%s_%s_change" % (app_label, model_name)))
        temp.append(re_path(r"^$", self.list_view, name="%s_%s_list" % (app_label, model_name)))

        # 扩展url
        temp.extend(self.extra_url())
        return temp

    @property
    def urls2(self):
        return self.get_urls2(), None, None


class Dmcsite:
    def __init__(self, ):
        self._register = {}

    def register(self, model, dmc_class=None):
        if not dmc_class:
            dmc_class = ModelDmc

        self._register[model] = dmc_class(model, self)

    def get_urls(self):
        temp = []
        for model, dmc_class_obj in self._register.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            temp.append(re_path(r"^%s/%s/" % (app_label, model_name), dmc_class_obj.urls2))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


site = Dmcsite()
