import datetime
from django.utils.timezone import make_aware
from users.models import User
from orders.models import OrderInfo
from goods.models import Goods


def get_dashboard_data():
    # 获取所有用户总数
    now_date = make_aware(datetime.datetime.now())
    start_date = now_date.date() - datetime.timedelta(1)
    # create_time__gte=index_date, create_time__lt=cur_date
    user_count = User.objects.all().count()
    # 获取当日注册用户数量 date_joined 记录创建账户时间
    user_count1 = User.objects.filter(date_joined__gte=start_date,date_joined__lt=now_date).count()
    # 当日活跃用户量
    user_count2 = User.objects.filter(last_login__gte=start_date, last_login__lt=now_date).count()

    goods_count = Goods.objects.all().count()
    goods_count1 = Goods.objects.filter(create_time__gte=start_date,create_time__lt=now_date).count()

    order_count = OrderInfo.objects.all().count()
    orders=OrderInfo.objects.filter(create_time__gte=start_date,create_time__lt=now_date)
    order_count1 = orders.count()
    order_count2=OrderInfo.objects.filter(create_time__gte=start_date,create_time__lt=now_date, status=6).count()
    users=set()
    for order in orders:
        users.add(order.user)
    user_count3=len(users)

    total_amount=total_amount1=total_amount2=0
    for order in OrderInfo.objects.filter(status=6):
        total_amount+=order.total_amount
    for order in OrderInfo.objects.filter(create_time__gte=start_date,create_time__lt=now_date, status=6):
        total_amount1+=order.total_amount

    return {'user': [user_count, user_count1,user_count2,user_count3],'goods': [goods_count, goods_count1],'order': [order_count, order_count1,order_count2],'total': [f'{total_amount/10000:.2f}', f'{total_amount1/10000:.2f}']}


def get_deals():
    orders = list(OrderInfo.objects.filter(status=2).order_by("create_time"))
    orders2 = list(OrderInfo.objects.filter(status=4).order_by("create_time"))
    orders.extend(orders2)
    deals = []
    for order in orders:
        deals.append({
            "order_id": order.order_id,
            "username": order.user,
            'total_amount': order.total_amount,
            'datetime': str(order.update_time)[:-13],
            'pay_method': '货到付款' if order.pay_method == 1 else '支付宝',
            'status': order.status,
        })
    return sorted(deals, key=lambda x: x['order_id'])


def get_sales():
    now_date = make_aware(datetime.datetime.now())
    start_date = now_date.date() - datetime.timedelta(7)
    week_counts = []
    week_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weeks=[]
    for i in range(7):
        # 循环遍历获取当天日期
        index_date = start_date + datetime.timedelta(days=i)
        # 指定下一天日期
        cur_date = start_date + datetime.timedelta(days=i+1)
        count = OrderInfo.objects.filter(create_time__gte=index_date, create_time__lt=cur_date).count()
        week_counts.append(count)
        weeks.append(week_list[index_date.weekday()])
    return week_counts, weeks

