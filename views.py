from django.shortcuts import render

from dmc.utils.page import Pagination
from api.models import Order, OrderDetail
from osos import settings

def get_page(request, data_list):
    data_count = data_list.count()
    current_page = int(request.GET.get("page", 1))
    base_path = request.path
    pagination = Pagination(current_page, data_count, base_path, request.GET, per_page_num=settings.PER_PAGE_NUM,
                            pager_count=11)
    page_data = data_list[pagination.start:pagination.end]
    return pagination, page_data


def order(request):
    order_list = Order.objects.all()
    pagination, page_data = get_page(request, order_list)
    return render(request, "order.html", {"page_data": page_data, "pagination": pagination})


def orderdetail(request, **kwargs):
    order_pk = kwargs.get("order_pk")
    detail_list = OrderDetail.objects.all()
    if order_pk:
        detail_list = OrderDetail.objects.filter(order_id=order_pk)
    pagination, page_data = get_page(request, detail_list)
    return render(request, "orderdetail.html", {"page_data": page_data, "pagination": pagination})
