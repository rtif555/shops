from django.db import models
from django.contrib.auth.models import User
from shop.furnitures.field import *
#from django.contrib.admin.options import ModelAdmin
#from django.views.generic.simple import direct_to_template

# Create your models here.

class Producer(models.Model):
    name=models.CharField(max_length=50, verbose_name=u"Наименование")
    country=models.CharField(max_length=50, verbose_name=u"Страна")
    adress=models.CharField(max_length=100, verbose_name=u"Адрес")
    phone=models.CharField(max_length=15, verbose_name=u"Телефон")

    class Meta:
        verbose_name = u'Производитель'
        verbose_name_plural = u'Производители'
		
    def __unicode__(self):
        return self.name

class Color(models.Model):
    name=models.CharField(max_length=70, unique=True, verbose_name=u"Название")    

    class Meta:
        verbose_name = u'Цвет'
        verbose_name_plural = u'Цвета'
		
    def __unicode__(self):
        return self.name
		
class Material(models.Model):
    name=models.CharField(max_length=50, verbose_name=u"Название")    

    class Meta:
        verbose_name = u'Материал'
        verbose_name_plural = u'Материлы'
		
    def __unicode__(self):
        return self.name
		
class PieceOfFurniture(models.Model):
    date_give=models.DateField(auto_now_add=True, editable=True, verbose_name=u"Дата принятия")   
    type=models.CharField(max_length=50, null=True, blank=True, editable=False, verbose_name=u"Тип") 
    model=models.CharField(max_length=50, verbose_name=u"Модель")
    manufacturer=models.ForeignKey(Producer, verbose_name=u"Производитель")
    dimensions=models.CharField(max_length=11, verbose_name=u"Размеры")
    color=models.ForeignKey(Color, verbose_name=u"Цвет")
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

    class Meta:
        verbose_name = u'Шкаф'
        verbose_name_plural = u'Шкафы'

    def save(self):
        if not self.type: self.type = u"Шкаф"
        super(Cupboard,self).save()		
    
    def __unicode__(self):
        return u'Шкаф %s' % (self.model)
		
class Armchair(PieceOfFurniture):    
    material=models.ForeignKey(Material, verbose_name=u"Материал")
    has_gazopatron=models.BooleanField(verbose_name=u"Наличие газопатрона")#
	
    class Meta:
        verbose_name = u'Кресло'
        verbose_name_plural = u'Кресла'
	
    def save(self):
        if not self.type: self.type = u"Кресло"
        super(Armchair,self).save()		

    def __unicode__(self):
        return u'Кресло %s' % (self.model)
		
class Chair(PieceOfFurniture):
    quantity_of_legs=models.IntegerField(verbose_name=u"Количество ножек")#
    height_spin=models.IntegerField(verbose_name=u"Высота спинки")#

    class Meta:
        verbose_name = u'Стул'
        verbose_name_plural = u'Стулья'
	
    def save(self):
        if not self.type: self.type = u"Стул"
        super(Chair,self).save()		

    def __unicode__(self):
        return u'Стул %s' % (self.model)

class Shelf(PieceOfFurniture):
    max_weight=models.IntegerField(verbose_name=u"Максимальная масса содержимого")#

    class Meta:
        verbose_name = u'Полка'
        verbose_name_plural = u'Полки'
		
    def save(self):
        if not self.type: self.type = u"Полка"
        super(Shelf,self).save()		
    
    def __unicode__(self):
        return u'Полка %s' % (self.model)
		
class Emploeer(models.Model):
    CHOICES = (
        (u'DR', u'Директор'),
        (u'KL', u'Кладовщик'),
        (u'BM', u'Продавец'),    
    )
    passport=models.CharField(max_length=20,verbose_name=u"Паспортные данные сотрудника")    
    post=models.CharField(max_length=10, verbose_name=u"Должность", choices=CHOICES)#
    salary=models.DecimalField(max_digits = 8, decimal_places=2, verbose_name=u"Заработная плата")
    user = models.ForeignKey(User, unique=True)
	
    class Meta:
        verbose_name = u'Cотрудник'
        verbose_name_plural = u'Сотрудники'
	
    def __unicode__(self):
        return '%s %s' % (self.post,self.user)
	
class Order(models.Model):
    id=models.AutoField(primary_key=True, verbose_name=u"Индификатор заказа")	
    emploeer=models.ForeignKey(Emploeer, null=True, blank=True, verbose_name=u"Оформляющий сотрудник")
    date_orders=models.DateField(auto_now_add=True, verbose_name=u"Дата заказа")
    statys=models.BooleanField(verbose_name=u"Статус заказа")
    cost=models.DecimalField(max_digits = 10,decimal_places=2, verbose_name=u"Общая стоимость заказа",null=True, blank=True)
    issuance=models.BooleanField(verbose_name=u"Товар выдан")
	
    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'
	
    def __unicode__(self):
        return ' %d' % (self.id)
		
class InternetOrders(models.Model):
    id_orders=models.ForeignKey(Order)
    passport=models.CharField(max_length=20)

    class Meta:
        verbose_name = u'Интернет заказ'
        verbose_name_plural = u'Интеренет заказы'
	
    def __unicode__(self):
         return ' %d' % (self.id)


		 
class FurnitureInOrders(models.Model):
    id_orders=models.ForeignKey(Order,verbose_name=u"Индефикатор заказа")
    id_furniture=models.ForeignKey(PieceOfFurniture, verbose_name=u"Индефикатор товара")

    class Meta:
        verbose_name = u'Товары  в заказах'
        verbose_name_plural = u'Товары  в заказах'
	
	
#class Statistics(models.Model):
#    class Meta:
#        managed = False
#        verbose_name = u'Статистика по заказам'
#        verbose_name_plural = u'Статистика'	
#       
#
#class LogAdmin(ModelAdmin):
#    _registery = {}
#
#    def changelist_view(self, request, extra_context=None):
#        opts = self.model._meta
#        app_label = opts.app_label
#        title = opts.verbose_name_plural #берем название из модели, что бы не хардкодить в двух местах     
#        orders=Order.objects.filter(issuance=True)
#        dict_ord={}
#        dict_count={"data": u"Итого", "chair": 0, "armchair": 0, "cupboard": 0, "shelf":0}
#        registery = []
#        for order in orders:
#            dict_ord["data"]=order.date_orders
#            dict_ord["cost"]=order.cost
#            furnitures=FurnitureInOrders.objects.filter(id_orders=order.id)
#            dict_ord["chair"]=PieceOfFurniture.objects.filter(
#                                     id__in=furnitures.values_list(
#                                     "id_furniture")).filter(
#                                     type=u"Стул").aggregate(models.Count(
#                                     'type'))["type__count"]
#            dict_count["chair"]=dict_count["chair"]+dict_ord["chair"]
#            dict_ord["armchair"]=PieceOfFurniture.objects.filter(
#                                     id__in=furnitures.values_list(
#                                     "id_furniture")).filter(
#                                     type=u"Кресло").aggregate(models.Count(
#                                     'type'))["type__count"]
#            dict_count["armchair"]=dict_count["armchair"]+dict_ord["armchair"]									 
#            dict_ord["cupboard"]=PieceOfFurniture.objects.filter(
#                                     id__in=furnitures.values_list(
#                                     "id_furniture")).filter(
#                                     type=u"Шкаф").aggregate(models.Count(
#                                     'type'))["type__count"]
#            dict_count["cupboard"]=dict_count["cupboard"]+dict_ord["cupboard"]									 
#            dict_ord["shelf"]=PieceOfFurniture.objects.filter(
#                                     id__in=furnitures.values_list(
#                                     "id_furniture")).filter(
#                                     type=u"Полка").aggregate(models.Count(
#                                     'type'))["type__count"]					 
#            dict_count["shelf"]=dict_count["shelf"]+dict_ord["shelf"]
#            registery.append(dict_ord)
#            dict_ord={}
#        dict_count["cost"]=orders.aggregate(models.Sum('cost'))["cost__sum"]
#        registery.append(dict_count)
                 			 
        #какая-то логика выбора logger-ов для отображения
        


#        context = {
#            'app_label': app_label,
#            'registery': registery,   #список logger-ов для отображения
#            'selected_logger': '',  #название выбранного logger-а
#            'filter_choices': '',
#            'title': title
#        }
#        return direct_to_template(request, 'changelist_view.html', context)

#    def has_change_permission(self, request, obj=None):
#        return not bool(obj)

#    def has_add_permission(self, request):
#        return False

#    def has_delete_permission(self, request, obj=None):
#        return False	