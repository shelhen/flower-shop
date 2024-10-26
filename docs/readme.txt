# 生成删除的app migrations文件夹
python manage.py makemigrations --empty appname

python manage.py makemigrations --empty users
python manage.py makemigrations
python manage.py migrate users
python manage.py migrate

python .\manage.py migrate
python .\manage.py makemigrations

# 数据库的创建与删除
create database flower charset=utf8;
use flower;
drop database flower;
show tables;

mysql -h127.0.0.1 -uroot -pPassword123. flower < areas.sql

python manage.py createsuperuser
python manager.py changepassword 

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt