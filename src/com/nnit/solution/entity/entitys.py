from django.db import models
from com.nnit.solution.local.util import utils

"""
class Member(models.Model):
    ID = models.UUIDField
    cell_phone = models.CharField(max_length=15)
    nick_name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    session_id = models.UUIDField
    latest_login = models.DateTimeField
    fetch_back_pwd = models.CharField(max_length=120)
    account_number = models.CharField(max_length=45)
    grade = models.CharField(max_length=255)
    status = models.CharField(max_length=48)
    is_online = models.CharField(max_length=48)
    gender = models.CharField(max_length=48)
    pic = models.CharField(max_length=300)
    email_addr = models.EmailField
    type = models.CharField(max_length=48)

    def create(cls, cell_phone, password):
        primary_id = utils.PrimaryIDGenerator.primary_id_generator();
        member = cls(cell_phone=cell_phone, password=password, ID=primary_id)
        return member
"""

class Groupon(object):
    id=''
    shop_id=''
    title=''
    picture=''
    original_price=0.00
    current_price=0.00
    start_time=None
    end_time=None
    details=''
    create_time=None

