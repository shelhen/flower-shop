




# class StaticCountView(View):
#     """后台数据统计"""
#
#     def get(self, request):
#         # 获取当前时间
#         # now_date = datetime.date.today()
#         aware_datetime = datetime.datetime.now()
#         # now_date = make_aware(aware_datetime)
#         now_date=datetime.date.today()
#         # 获取所有用户总数
#         user_count = User.objects.all().count()
#         # 获取当日注册用户数量 date_joined 记录创建账户时间
#         dayregister_count = User.objects.filter(date_joined__gte=now_date).count()
#         # 获取当日登录用户数量  last_login记录最后登录时间
#         last_login_count = User.objects.filter(last_login__gte=now_date).count()
#         # 获取当日下单用户数量  create_time__gte 订单创建时间
#         orders_count_list = []
#         orders_count_list2 = []
#         for e in OrderInfo.objects.filter(create_time__gte=now_date):
#             orders_count_list.append({
#                 'id': e.user_id,
#             })
#         for a in orders_count_list:
#             orders_count_list2.append(a['id'])
#         orders_count = len(set(orders_count_list2))
#
#         # 设计月增用户——统计图数据
#         # 获取一月前日期
#         start_date = now_date - datetime.timedelta(29)
#         # 创建空列表保存每天的用户量
#         # print(start_date)
#         date_list = []
#         moon_count_list = []
#         count_list=[]
#         for i in range(30):
#             # 循环遍历获取当天日期
#             index_date = start_date + datetime.timedelta(days=i)
#             # 指定下一天日期
#             cur_date = start_date + datetime.timedelta(days=i + 1)
#             # 查询条件是大于当前日期index_date，小于明天日期的用户cur_date，得到当天用户量
#             count = User.objects.filter(date_joined__gte=index_date, date_joined__lt=cur_date).count()
#             moon_count_list.append({
#                 'count':count,
#                 'date':str(index_date)[0:11],
#             })
#             count_list.append(count)
#             date_list.append(str(index_date)[0:11])
#         # that_day=now_date-datetime.timedelta(2)
#         data = GoodsVisitCount.objects.filter(date=now_date)
#         # data = GoodsVisitCount.objects.filter(date=that_day)
#         visitacount_list = []
#         goodname_list=[]
#         for e in data:
#             visitacount_list.append(e.count)
#             goodname_list.append(GoodsCategory.objects.filter(id=e.category_id)[0].name)
#
#         return http.JsonResponse({
#             'code': RETCODE.OK,
#             "user_count": user_count-1,
#             "dayregister_count": dayregister_count,
#             "last_login_count": last_login_count-1,
#             'orders_count': orders_count,
#             # 'moon_count_list':moon_count_list,
#             'count_list':count_list,
#             'date_list':date_list,
#             'visitacount_list':visitacount_list,
#             'goodname_list':goodname_list,
#         })



