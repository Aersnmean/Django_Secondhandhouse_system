import mongoengine


class HouseInfo(mongoengine.Document):
    title = mongoengine.StringField(max_length=256, verbose_name='标题')
    imgs = mongoengine.ListField(verbose_name='照片')
    bedroom = mongoengine.StringField(max_length=20, verbose_name='室厅')
    area = mongoengine.StringField(max_length=20, verbose_name='建筑面积')
    total_price = mongoengine.FloatField(verbose_name='总价格')
    plot = mongoengine.StringField(max_length=20, verbose_name='所属小区')
    type = mongoengine.ListField(verbose_name='室厅卫')
    unit_price = mongoengine.FloatField(verbose_name='房屋单价(元/平方米)')
    position = mongoengine.ListField(verbose_name='所在位置')
    down_payment = mongoengine.StringField(max_length=20, verbose_name='参考首付')
    year = mongoengine.StringField(max_length=10, verbose_name='建造年份')
    direction = mongoengine.StringField(max_length=10, verbose_name='房屋朝向')
    house_type = mongoengine.StringField(max_length=10, verbose_name='房屋类型')
    floor = mongoengine.StringField(max_length=20, verbose_name='所在楼层')
    decoration = mongoengine.StringField(max_length=10, verbose_name='装修程度')
    property_year = mongoengine.StringField(max_length=20, verbose_name='产权年限')
    elevator = mongoengine.StringField(max_length=10, verbose_name='配套电梯')
    house_year = mongoengine.StringField(max_length=20, verbose_name='房本年限')
    property = mongoengine.StringField(max_length=10, verbose_name='产权性质')
    heating = mongoengine.StringField(max_length=10, verbose_name='配套供暖')
    only = mongoengine.StringField(max_length=10, verbose_name='唯一住房')
    one_hand = mongoengine.StringField(max_length=10, verbose_name='一手房源')
    core_point = mongoengine.StringField(verbose_name='核心卖点')
    owner_men = mongoengine.StringField(verbose_name='业主心态')
    service_introduction = mongoengine.StringField(verbose_name='服务介绍')
    house_code = mongoengine.StringField(verbose_name='房屋编码')
    add_date = mongoengine.DateField(verbose_name="发布时间")

    meta = {'collection': 'TaiYuanHouse'}