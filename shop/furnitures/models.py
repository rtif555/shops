from django.db import models
from django.contrib.auth.models import User
from shop.furnitures.field import *

# Create your models here.

class Producer(models.Model):
    name=models.CharField(max_length=50, verbose_name=u"Наименование")
    country=models.CharField(max_length=50, verbose_name=u"Страна")
    adress=models.CharField(max_length=100, verbose_name=u"Адрес")
    phone=models.CharField(max_length=15, verbose_name=u"Телефон")

    def __unicode__(self):
        return self.name

class PieceOfFurniture(models.Model):
    date_give=models.DateField(auto_now_add=True, verbose_name=u"Дата принятия")   
    type=models.CharField(max_length=50, null=True, blank=True, editable=False, verbose_name=u"Тип") 
    model=models.CharField(max_length=50, verbose_name=u"Модель")
    manufacturer=models.ForeignKey(Producer, verbose_name=u"Производитель")
    dimensions=models.CharField(max_length=11, verbose_name=u"Размеры")
    color=models.CharField(max_length=15, verbose_name=u"Цвет")
    price=models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name=u"Цена")
    statys=models.BooleanField(verbose_name=u"Зарезервирован")
    image=models.ImageField(upload_to='photos', null=True, blank=True, verbose_name=u"Изображение")
    
    def __unicode__(self):
        return u'%s %s' % (self.type, self.model)	

    def get_type(self):
        return u'%s ' % (self.type)

    def get_model(self):
        return u'%s' % (self.model)
		
    def get_color(self):
        return u'%s' % (self.color)

    def get_manufacturer(self):
        return self.manufacturer.__unicode__()

class Cupboard(PieceOfFurniture):    
    quantity_of_doors=models.IntegerField(verbose_name=u"Количество дверей")
    has_lock=models.BooleanField(verbose_name=u"Наличие замка")

    def save(self):
        if not self.type: self.type = u"Шкаф"
        super(Cupboard,self).save()		
    
    def __unicode__(self):
        return u'Шкаф %s' % (self.model)
		
class Armchair(PieceOfFurniture):    
    material=models.CharField(max_length=50, verbose_name=u"Материал")
    has_gazopatron=models.BooleanField(verbose_name=u"Наличие газопатрона")#
	
    def save(self):
        if not self.type: self.type = u"Кресло"
        super(Armchair,self).save()		

    def __unicode__(self):
        return u'Кресло %s' % (self.model)
		
class Chair(PieceOfFurniture):
    quantity_of_legs=models.IntegerField(verbose_name=u"Количество ножек")#
    height_spin=models.IntegerField(verbose_name=u"Высота спинки")#
	
    def save(self):
        if not self.type: self.type = u"Стул"
        super(Chair,self).save()		

    def __unicode__(self):
        return u'Стул %s' % (self.model)

class Shelf(PieceOfFurniture):
    max_weight=models.IntegerField(verbose_name=u"Максимальная масса содержимого")#

    def save(self):
        if not self.type: self.type = u"Полка"
        super(Shelf,self).save()		
    
    def __unicode__(self):
        return u'Полка %s' % (self.model)
		
class Emploeer(models.Model): 
    passport=models.CharField(max_length=20,verbose_name=u"Паспортные данные сотрудника")    
    post=models.CharField(max_length=10, verbose_name=u"Должнлость")#
    salary=models.DecimalField(max_digits = 8, decimal_places=2, verbose_name=u"Заработная плата")
    user = models.ForeignKey(User, unique=True)
	
    def __unicode__(self):
        return '%s %s' % (self.post,self.user)
	
class Order(models.Model):
    id=models.AutoField(primary_key=True, verbose_name=u"Индификатор заказа")	
    emploeer=models.ForeignKey(Emploeer, null=True, blank=True, verbose_name=u"Оформляющий сотрудник")
    date_orders=models.DateField(auto_now_add=True, verbose_name=u"Дата заказа")
    statys=models.BooleanField(verbose_name=u"Статус заказа")
    cost=models.DecimalField(max_digits = 10,decimal_places=2, verbose_name=u"Общая стоимость заказа",null=True, blank=True)
    issuance=models.BooleanField(verbose_name=u"Товар выдан")
	
    def __unicode__(self):
        return ' %d' % (self.id)
		
class InternetOrders(models.Model):
    id_orders=models.ForeignKey(Order)
    date_orders=models.DateField()
    passport=models.CharField(max_length=20)
	
    def __unicode__(self):
         return ' %d' % (self.id)
		
class FurnitureInOrders(models.Model):
    id_orders=models.ForeignKey(Order,verbose_name=u"Индефикатор заказа")
    id_furniture=models.ForeignKey(PieceOfFurniture, verbose_name=u"Индефикатор товара")
	
	
