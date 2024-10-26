```shell
# 生成删除的app migrations文件夹
python manage.py makemigrations --empty appname

python manage.py makemigrations --empty product
python manage.py makemigrations
python manage.py migrate product
python manage.py migrate

python .\manage.py migrate
python .\manage.py makemigrations
```



```mysql
# 数据库的创建与删除
create database flower charset=utf8;
use flower;
drop database flower;
show tables;

mysql -h127.0.0.1 -uroot -pPassword123. flower < areas.sql
```



```shell
python manage.py createsuperuser
python manager.py changepassword 
# 重新设置管理员密码
python manage.py shell 
from django.contrib.auth import get_user_model 
User = get_user_model().objects.get(pk=1)
User.set_password('root')
User.save()
```



```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt
```

