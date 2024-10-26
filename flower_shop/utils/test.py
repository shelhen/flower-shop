from pathlib import Path
import pymysql
from datetime import datetime
from HuaSpider import HuaSpider
from flower_shop.settings.dev import DATABASES

BASE_DIR = Path(__file__).resolve().parent.parent.parent
database = DATABASES['default']


def pre_action():
    mysql = pymysql.connect(
        host=database['HOST'],
        user=database['USER'],
        password=database['PASSWORD'],
        port=database['PORT'],
        charset='utf8',
        database=database['NAME']
    )
    db = mysql.cursor()  # 创建游标

    url = f"http://{database['HOST']}:{database['PORT']}"
    with open(BASE_DIR / 'docs/slides.json', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '').split('	')
            sql = 'insert into tb_slide(create_time, update_time, name, image,url) values(%s,%s,%s,%s,%s)'
            data = (str(datetime.now())[0:-7], str(datetime.now())[0:-7], 'banner_0 ' +str(line[0]), line[4] ,url)
            try:
                db.execute(sql, data)
                mysql.commit()
            except Exception as e:
                print(e)
                continue
    print('数据库存储slides.txt内容成功')
    with open(BASE_DIR / 'docs/goodcategory.json', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '').split('	')
            sql2 = 'insert into tb_goods_category(create_time, update_time, name) values(%s,%s,%s)'
            data2 = (str(datetime.now())[:-7], str(datetime.now())[:-7] ,line[3])
            try:
                db.execute(sql2, data2)
                mysql.commit()
            except Exception as e:
                print(e)
                continue
    print('数据库存储goodcategory.txt内容成功')
    # with open('tb_areas.txt', 'r', encoding='utf8') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         line = line.replace('\n', '').split('	')
    #         sql3 = 'insert into tb_goods_category(id, name, parent_id) values(%s,%s,%s)'
    #         data3 = (line[0], line[1] ,line[2])
    #         try:
    #             db.execute(sql3, data3)
    #             mysql.commit()
    #         except Exception as e:
    #             print(e)
    #             continue
    # print('数据库存储tb_areas.txt内容成功')
    db.close()  # 关闭游标连接
    mysql.close()  # 关闭数据库


if __name__ == '__main__':
    pre_action()
    hua = HuaSpider()
    hua.main()
    # hua.get_news()