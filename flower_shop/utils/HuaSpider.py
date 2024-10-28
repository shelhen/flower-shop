import time
import requests
from datetime import datetime
import pymysql
import re
from w3lib.html import replace_entities, remove_tags, replace_tags
import hashlib
import os
import json
import random
from parsel import Selector
from flower_shop.settings.dev import DATABASES
from pathlib import Path


class HuaSpider(object):
    def __init__(self):
        self.regex = re.compile("</?[^ >/]+.*?>", re.DOTALL | re.IGNORECASE)
        self.session = requests.Session()
        self.session.timeout = 30
        self.base_url = 'https://www.hua.com/'
        self.goodsUrls = {
            1: ['aiqingxianhua', ],
            2: ['businessFlower/kaiyehualan', ],
            3: ['youqingxianhua', 'zhufuqinghexianhua'],
            4: ['songzhangbeixianhua', 'songlaoshixianhua'],
            5: ['tanbingweiwenxianhua', ],
            6: ['daoqianxianhua', ],
            7: ['hunqingxianhua', 'zhufuqinghexianhua'],
        }
        self.pageNum = 1  # 爬取的花语新闻页码数目，不应超过43
        self.projectPath = Path(__file__).resolve().parent.parent.parent
        self.stock = random.randint(50, 256)
        self.database = DATABASES['default']
        self.year = str(datetime.now())[0:4]
        self.data_path_map = {
            "slides": self.projectPath / 'docs/slides.json',
            "goodcategory": self.projectPath / 'docs/goodcategory.json',
            "areas": self.projectPath / 'docs/areas.json'
        }
        self.mysql = None
        self.sql_map = {
            'goods': """
            insert into tb_goods(
            id, 
            create_time, 
            update_time, 
            name,
            intro, 
            caption, 
            price, 
            cost_price,
            market_price, 
            stock, 
            sales,
            sales2, 
            comments, 
            material, 
            desc_detail, 
            desc_pack, 
            is_launched, 
            default_image, 
            category_id
            ) values (
            '{id}',
            '{create_time}',
            '{update_time}',
            '{title}',
            '{intro}',
            '{caption}',
            '{price}',
            '{cost_price}',
            '{mprice}',
            '{stock}',
            '{sales}',
            '{sales2}',
            '{comments}',
            '{material}',
            '{detail}',
            '{pack}',
            '{is_launched}',
            '{default_image}',
            '{category_id}') ON DUPLICATE KEY UPDATE 
            update_time='{update_time}',
            name='{title}',
            intro='{intro}',
            caption='{caption}',
            price = '{price}',
            cost_price = '{cost_price}',
            market_price = '{mprice}',
            stock = '{stock}',
            sales = '{sales}',
            sales2 = '{sales2}',
            comments = '{comments}',
            material='{material}',
            desc_detail = '{detail}',
            desc_pack = '{pack}',
            default_image='{default_image}',
            category_id='{category_id}'
            """,
            'images1': """
            insert into tb_good_image(
            create_time,
            update_time,
            image,
            good_id
            ) values( 
            '{create_time}',
            '{update_time}',
            '{image}',
            '{good_id}'
            ) ON DUPLICATE KEY UPDATE 
            update_time='{update_time}',
            image='{image}',
            good_id='{good_id}'
            """,
            'images2': """
            insert into tb_detail_image(
            create_time,
            update_time,
            image,
            good_id
            ) values( 
            '{create_time}',
            '{update_time}',
            '{image}',
            '{good_id}'
            ) ON DUPLICATE KEY UPDATE 
            update_time='{update_time}',
            image='{image}',
            good_id='{good_id}'
            """,
            'images3': """
            insert into tb_content_image(
            create_time,
            update_time,
            image,
            content_id,
            good_id
            ) values( 
            '{create_time}',
            '{update_time}',
            '{image}',
            '{content_id}',
            '{good_id}'
            ) ON DUPLICATE KEY UPDATE 
            update_time='{update_time}',
            image='{image}',
            content_id='{content_id}',
            good_id='{good_id}'
            """,
            'content': """
            insert into tb_content(
            id,
            create_time,
            update_time,
            title,
            intro,
            count, 
            image,
            text
            ) values(
            '{id}',
            '{create_time}',
            '{update_time}',
            '{title}',
            '{intro}',
            '{count}',
            '{image}',
            '{text}'
            ) ON DUPLICATE KEY UPDATE 
            update_time='{update_time}',
            title='{title}',
            intro='{intro}',
            count='{count}',
            image='{image}',
            text='{text}'
            """,
            "slides": """
            insert into tb_slide(id, create_time, update_time, name, image, url) values 
            ('{id}','{create_time}','{update_time}','{name}','{image}', '{url}')
            """,
            "goodcategory": """
            insert into tb_goods_category(id, create_time, update_time, name) values(
            '{id}', '{create_time}', '{update_time}', '{name}')
            """,
            "areas": """
            insert into tb_areas(id, name, parent_id) values('{id}', '{name}',{parent_id})
            """
        }

    def save(self, db, sql_key, data):
        mysql_commend = self.sql_map[sql_key]
        try:
            db.execute(mysql_commend.format(**data))
        except Exception as e:
            print(f'Error {e}')

    def crawl_goods(self):
        for key, apis in self.goodsUrls.items():
            for api in apis:
                print(f"开始爬取类型为{key}中api为{api}的商品")
                count = 0
                db = self.mysql.cursor()
                for data in self.get_list_pages(api, cid=key):
                    images = data.pop('images')
                    detail_images = data.pop('detail_images')

                    self.save(db, 'goods', data)
                    for image in images:
                        _img = {
                            "create_time": str(datetime.now())[0:-7],
                            "update_time": str(datetime.now())[0:-7],
                            "image": image,
                            "good_id": data['id']
                        }
                        self.save(db, 'images1', _img)
                    for image in detail_images:
                        _img = {
                            "create_time": str(datetime.now())[0:-7],
                            "update_time": str(datetime.now())[0:-7],
                            "image": image,
                            "good_id": data['id']
                        }
                        self.save(db, 'images2', _img)
                    count += 1
                    if count % 20 == 0:
                        self.mysql.commit()
                db.close()
                print(f"保存类型为{key}中api为{api}的商品数据成功")
                time.sleep(0.1)
        print('所有鲜花商品爬取完毕！')

    def load_datas(self):
        db = self.mysql.cursor()  # 创建游标
        for key, value in self.data_path_map.items():
            print(f'开始载入{key}数据！')
            with open(value, 'r', encoding='utf8') as f:
                datas = json.load(f)
            for data in datas:
                sql = self.sql_map[key]
                try:
                    db.execute(sql.format(**data))
                except Exception as e:
                    if e.args[0] == 1062:
                        continue
                    else:
                        print(e)
            print('载入成功。')

        self.mysql.commit()
        db.close()

    def main(self):
        self.session.headers['User-Agent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                              'like Gecko) Chrome/109.0.0.0 Safari/537.36')
        self.mysql = pymysql.connect(
            host=self.database["HOST"],
            user=self.database['USER'],
            password=self.database['PASSWORD'],
            port=self.database['PORT'],
            charset='utf8',
            database=self.database['NAME']
        )
        # 外部导入数据
        self.load_datas()
        time.sleep(2)
        self.crawl_goods()
        time.sleep(2)

        datas = self.get_content()
        db = self.mysql.cursor()
        for data in datas:
            images = data.pop('images')
            self.save(db, 'content', data)
            for image in images:
                _img = {
                    'content_id': data['id'],
                    "create_time": str(datetime.now())[0:-7],
                    "update_time": str(datetime.now())[0:-7],
                    "image": image['img_url'],
                    "good_id": image['id']
                }
                self.save(db, 'images3', _img)

        self.mysql.commit()
        db.close()
        self.mysql.close()

    def get_list_pages(self, api, cid, page=1):
        list_url = 'https://www.hua.com/{}/?pg={}'
        response = self.session.get(list_url.format(api, {page}))
        html = Selector(text=response.text)
        # 获取所有的spu_id,列表页获取价格等信息，携带各个商品的价格信息前往详情页，返回解析数据。
        pids = html.xpath('//span/@data-pp').getall()
        # self.session.get('https://www.hua.com/home/CheckAgent', timeout=10)
        response = self.session.post(f'{self.base_url}/home/GetProductListPrice',
                                     data={'itemcodes': ','.join(pids), 'perf': ''}, timeout=10).json()
        products = response['Datas']['ProductPrices']
        for product in products:
            detail_url = f"{self.base_url}product/{product['ItemCode']}.html"
            response = self.session.get(detail_url)
            detail_page = Selector(text=response.text)
            # 解析详情页
            floral = detail_page.xpath('//div[@class="huayu"]/div[2]/p/text()').get()
            material = detail_page.xpath('//div[@class="huayu"]/div[3]/p/text()').get()
            package = detail_page.xpath('//div[@class="huayu"]/div[4]/p/text()').get()
            # 标签，有的有，有的没有
            caption = detail_page.xpath('//span[@class="title-point"]/text()').getall()
            caption = caption[0][1:-1] if caption else f'{self.year}畅销热卖款'
            pics = detail_page.xpath('//div[@class="preview-list-item"]/img')
            img_node = detail_page.xpath('//div[@class="detail-product-content"]')
            img_paths = [self.download(img.xpath('./@data-original').get())
                         for img in img_node.xpath('./img|./p/img|./div/img')]
            pic_path = [self.download(pic.xpath('./@src').get()) for pic in pics]
            default_image = self.download(f"//img01.hua.com/uploadpic/newpic/{product['ItemCode']}.jpg")
            sales = float(product['Sales'][:-1]) * 10000 if product['Sales'][-1] == '万' else float(product['Sales'])
            yield dict(
                id=product['ItemCode'],
                create_time=str(datetime.now())[0:-7],
                update_time=str(datetime.now())[0:-7],
                title=product['Cpmc'],
                intro=product['Instro'],
                caption=caption,
                price=product['Price'],
                cost_price=float(product['Price']) - 20.00,
                mprice=product['LinePrice'],
                sales=sales,
                sales2=product['Sales'],
                detail=floral,
                material=material,
                pack=package,
                default_image=default_image,
                category_id=cid,
                images=pic_path,
                comments=0,
                stock=self.stock,
                is_launched=1,
                detail_images=img_paths
            )
        # 翻页
        next_page = html.xpath('//ul[@class="pagination"]/li[last()]/a/@href')
        if next_page != '#':
            # 执行下一页
            page += 1
            self.get_list_pages(api, cid=cid, page=page)

    def get_content(self):
        # 爬取花语信息
        datas = []
        for i in range(self.pageNum):
            response = self.session.get("{0}huayu/huayu{1}.html".format(self.base_url, i))
            html = Selector(text=response.text)
            nodes = html.xpath('//div[@class="Item_Brief"]/a')
            for node in nodes:
                pid = node.xpath('./@href').get()[7:12]
                content = node.xpath('./text()').get()
                introduce = '' if content is None else content.replace('中国鲜花礼品网（花礼网）', '花里有花鲜花网')
                response = self.session.get(f'{self.base_url}huayu/{pid}.html')
                detail = Selector(text=response.text)
                title = detail.xpath('//div[@class="title"]/h4/text()').get()
                article = detail.xpath('//div[@class="article"][1]')
                img_nodes = article.xpath('./p//img/..|./div//img/..')

                article = remove_tags(article.get(), keep=('strong',))
                text = replace_entities('\n'.join([text.strip() for text in article.split('\n') if text.strip()]))
                text = text.replace('花礼网', ' 花里有花网 ').replace('鲜花推荐/', '').replace('/', '').replace('~', '')
                imgs = []
                if img_nodes:
                    for node in img_nodes:
                        try:
                            target_id = node.xpath('./@href')[0][9:16] if node.xpath('./@href') else '9999999'
                            img_path = self.download(node.xpath('.//img/@data-original').get())
                        except:
                            continue
                        imgs.append({"id": target_id, "img_url": img_path})
                datas.append(dict(
                    id=pid,
                    create_time=str(datetime.now())[0:-7],
                    update_time=str(datetime.now())[0:-7],
                    title=title,
                    intro=introduce,
                    text=text,
                    images=imgs,
                    image=imgs[0]['img_url'] if imgs else '',
                    count=random.randint(1, 999)
                ))
        return datas

    def download(self, url):
        """存储图片，并需要返回相对于static的存储路径"""
        dirname = self.projectPath / 'flower_shop/static/imgs/products'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        response = self.session.get(f"https:{url}").content
        filename = hashlib.md5(response)
        with open(dirname / f'{filename.hexdigest()}.jpg', 'wb') as f:
            f.write(response)
        path = str(dirname / f'{filename.hexdigest()}.jpg').split('flower_shop')[-1].strip("\\")
        return path.replace('\\', '\\\\')


if __name__ == '__main__':
    hua = HuaSpider()
    hua.main()
