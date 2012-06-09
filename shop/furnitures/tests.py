"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime
import re
from decimal import Decimal
from django_webtest import WebTest
from shop.furnitures.models import *
from django.contrib.auth.models import User
 
class FindTest(WebTest):

    def setUp(self):
        self.prod = Producer.objects.create( name=u'Рога',country='Россия',adress=u'Мира',phone='545678')
        self.color=Color.objects.create(name=u'Cиний')
        self.chair=Chair(model=u'Стул1', manufacturer=self.prod, dimensions=u'56x56x45',
              color=self.color, price=455, quantity_of_legs=5, height_spin=10,
              statys=False)
        self.chair.save()
        self.shelf=Shelf(model=u'Полка1',manufacturer=self.prod,
              dimensions=u'56x56x34',color=self.color,price=4343,
              statys=False,max_weight=200)
        self.shelf.save()
        self.user=User.objects.create_user(username=u'sandra',password=u'1')
        self.user.is_active=True
        self.user.save()
        self.user1=User.objects.create_user(username=u'qwerty',password=u'1')
        self.user1.is_active=True
        self.user1.save()
        self.user2=User.objects.create_user(username=u'rtif',password=u'1')
        self.user2.is_active=True
        self.user2.is_staff=True
        self.user2.is_superuser=True
        self.user2.save()
        self.emploeer=Emploeer.objects.create(passport='1234 56789',post=u'BM',salary=5000,user = self.user)
        self.emploeer1=Emploeer.objects.create(passport='1234 56779',post=u'KL',salary=5500,user = self.user1)
        self.emploeer2=Emploeer.objects.create(passport='1234 57779',post=u'DR',salary=5500,user = self.user2)
        self.order=Order.objects.create(emploeer=self.emploeer,statys=True,issuance=False)
        self.shelf1=Shelf(model=u'Полка2',manufacturer=self.prod,
              dimensions=u'56x56x34',color=self.color,price=4343,
              max_weight=455, statys=True)
        self.shelf1.save()
        self.fio=FurnitureInOrders.objects.create(id_orders= self.order,id_furniture=self.shelf1) 
        self.order2=Order.objects.create(emploeer=None,statys=True,issuance=False)
        self.shelf2=Shelf(model=u'Полка3',manufacturer=self.prod,
              dimensions=u'56x56x34',color=self.color,price=4343,
              max_weight=455, statys=True)
        self.shelf2.save()
        self.fio1=FurnitureInOrders.objects.create(id_orders= self.order2,id_furniture=self.shelf2) 
        self.io=InternetOrders.objects.create(id_orders=self.order2,passport='1568 245678')
        self.material=Material.objects.create(name=u'Ситец') 

		


    def testSee(self): #тестим первую страницу
        page = self.app.get('/find/')
        #print(page.body)
        #page.showbrowser ()
        assert '<td>Стул</td>' in page
        assert '<td>Стул1</td>' in page
        assert '<td>Cиний</td>' in page
        assert '<td>56x56x45</td>' in page
        str='''<td>Полка</td>
		    <td>Полка1</td>
		    <td>Cиний</td>'''
        assert str in page
        print(u'Просмотр пройден')		

    def testSearch(self):#тестим поиск
       page = self.app.get('/find/')
       #print(page.forms[0].fields.values())
       page.forms[0].set('type', u'Стул')
       #------------------------
       res=page.forms[0].submit()	   
       #res.showbrowser()
       assert '<td>Полка</td>' not in res
       print(u'Поиск пройден')	

    def testBuyOne(self):#тестим одиночную покупку
       page = self.app.get('/find/')
       #page.showbrowser()
       #------------------------
       res=page.click(href="/furniture/"+str(self.chair.id)+"/")
       assert '<th>Модель</th><td>Стул1</td>' in res
       #------------------------
       res1=res.form.submit().follow()
       assert '<td>Стул</td>' not in res1
       print(u'Выбор товара пройден')	
       assert u'Корзина' in res1
       #------------------------
       res2=res1.click(href="/basket").follow() 
       assert u'<td> Чек №' in res2
       print(u'Просмотр корзины пройден')
       #------------------------	
       res3=res2.form.submit().follow() 
       assert u'Серия паспорта:' in res3
       res3.form['seria']='1568'
       res3.form['number']='245678'
       #------------------------
       res4=res3.form.submit().follow()
       print(u'Интернет покупка пройдена')
       self.assertEqual(self.shelf.statys, False)
       #res4.showbrowser()


    def testEnter(self):#тестим авторизацию	
        page = self.app.get('/avtoriz/') 
        page.form.set("login",self.user.username)
        page.form.set("password",u'1')
       #------------------------
        res=page.form.submit()
        assert 'Неправильная пaра' not in res
		#--------------------------------
        print(u'Аунтификация прошла успешна')	
        page = self.app.get('/avtoriz/') 
        page.form.set("login",self.user.username)
        page.form.set("password",u'qwerty')
       #------------------------
        res=page.form.submit()
        #res.showbrowser()
        assert 'Неправильная пара'  in res
        print(u'Проверка ввода неверного прошла успешно')	        
        #assert u'Логин' not in res
	   
    def testEnterBR(self):#тестим покупку через продавца
       page = self.app.get('/find/', user=self.user)
       assert 'Выход' in page
       #page.showbrowser()	   
       #print(page.form.fields.values())
       #------------------------
       res=page.click(href="/furniture/"+str(self.shelf.id)+"/")
       #res.showbrowser() 
       assert '<th>Модель</th><td>Полка1</td>' in res
       res1=res.form.submit().follow()
       #res1.showbrowser() 
       assert '<td>Полка1</td>' not in res1
       print(u'Выбор BR товара пройден')	
       assert u'Корзина' in res1
       #------------------------
       res2=res1.click(href="/basket").follow() 
       assert u'<td> Чек №' in res2 
       #------------------------      
       res3=res2.form.submit().follow()  
       assert '<td>Полка</td>' not in res3
       print(u'Просмотр BR корзины пройден')  
       #res3.showbrowser()


	
    def testEnterKL(self):#тестим работу кладовщика
       page = self.app.get('/storekeeper/', user=self.user1)
       assert '<td class="centre">'+str(self.order.id)+'</td>' in page
       print(u'Просмотр заказа пройден')
       #------------------------
       res=page.click(href="/storekeeper/order/"+str(self.order.id)+"/")
       assert '<td>Полка2</td>' in res###############       
       #res.form['Action']=u'Товар выдан'
       #------------------------
       res1=res.form.submit().follow()
       assert '<td class="centre">'+str(self.order.id)+'</td>' not in res1###############
       print(u'Заказ выдан')
       #page.showbrowser()

    
    def testEnterIO(self):#проверяем индификацию покупателя
       page = self.app.get('/find/', user=self.user)
       #------------------------
       res=page.click(href="/internetorders/")
       #res.showbrowser()
       assert u'Серия паспорта:' in res
       res.form['seria']='1568'
       res.form['number']='245678'
       #------------------------
       res1=res.form.submit().follow()
       print(u'Индефикация покупателя прошла успешно')
       #res1.showbrowser()
       #------------------------
       assert u'<td> Чек №' in res1
       res2=res1.form.submit().follow()
  

    def testInputShelf(self):
       page = self.app.get('/storekeeper/', user=self.user1)
       #page.showbrowser()
       assert '<td class="centre">'+str(self.order.id)+'</td>' in page###############       
       #------------------------
       page.form['piece']=u'Полка'
       res=page.form.submit()
       res.form['model']='Полка5'
       res.form['manufacturer']=self.prod.id
       res.form['dimensions']='36x36x36'
       res.form['color']=self.color.id
       res.form['price']='255'
       res.form['max_weight']='25'
       #------------------------
       res1=res.form.submit('piece').follow()
       #res1.showbrowser()	   
       assert 'Полка5' in res1
       print(u"Добавление полки выполнено")
	   
    def testInputChairs(self):
       page = self.app.get('/storekeeper/', user=self.user1)

       #------------------------
       page.form['piece']=u'Стул'
       res=page.form.submit()
       res.form['model']='Стул3'
       res.form['manufacturer']=self.prod.id
       res.form['dimensions']='36x36x36'
       res.form['color']=self.color.id
       res.form['price']='255'
       res.form['quantity_of_legs']='5'
       res.form['height_spin']='5'
       #------------------------
       res1=res.form.submit('piece').follow()
       #res1.showbrowser()	   
       assert 'Стул3' in res1

    def testInputCupboard(self):
       page = self.app.get('/storekeeper/', user=self.user1)
       #------------------------
       page.form['piece']=u'Шкаф'
       res=page.form.submit()
       res.form['model']='Шкаф1'
       res.form['manufacturer']=self.prod.id
       res.form['dimensions']='36x36x36'
       res.form['color']=self.color.id
       res.form['price']='255'
       res.form['quantity_of_doors']='5'
       res.form['has_lock']=True
       #------------------------
       res1=res.form.submit('piece').follow()
       #res1.showbrowser()	   
       assert 'Шкаф1' in res1
       print(u"Добавление шкафа выполнено")	 

    def testInputArmchair(self):
       page = self.app.get('/storekeeper/', user=self.user1)
       
       #------------------------
       page.form['piece']=u'Кресло'
       res=page.form.submit()
       res.form['model']='Кресло1'
       res.form['manufacturer']=self.prod.id
       res.form['dimensions']='36x36x36'
       res.form['color']=self.color.id
       res.form['price']='255'
       res.form['material']=self.material.id
       res.form['has_gazopatron']=True
       #------------------------
       res1=res.form.submit('piece').follow()
       #res1.showbrowser()	   
       assert 'Кресло1' in res1
       print(u"Добавление кресло выполнено")	   	   

    def testInputProducer(self):
       page = self.app.get('/storekeeper/', user=self.user1)
   
       #------------------------
       page.form['piece']=u'Кресло'
       res=page.form.submit()
       res.form['what']=u'Производитель'
	   #------------------------
       res1=res.form.submit()
       #res1.showbrowser()
       res1.form['name']=u'Папа Карло'
       res1.form['country']=u'Россия'	   
       res1.form['adress']=u'ул Мира 61'
       res1.form['phone']='456789'   
       res2=res1.form.submit('piece')     	   
       assert 'Папа Карло' in res2
       print(u"Добавление производителя выполнено")	
	   
    def testInputMaterial(self):
       page = self.app.get('/storekeeper/', user=self.user1)
  
       #------------------------
       page.form['piece']=u'Кресло'
       res=page.form.submit()
       res.form['what']=u'Материал'
	   #------------------------
       res1=res.form.submit()
       #res1.showbrowser()
       res1.form['name']=u'Ротанг'
       res2=res1.form.submit('piece')     	   
       assert u'Ротанг' in res2
       print(u"Добавление материала выполнено")	
	   
    def testInputColor(self):
       page = self.app.get('/storekeeper/', user=self.user1)
       #page.showbrowser()

       page.form['piece']=u'Кресло'
       res=page.form.submit()
       res.form['what']=u'Цвет'
	   #------------------------
       res1=res.form.submit()
       #res1.showbrowser()
       res1.form['name']=u'Бирюзовый'
       res2=res1.form.submit('piece')     	   
       assert u'Бирюзовый' in res2
       print(u"Добавление цвета выполнено")
	   
    def testInpuErrorDimisions(self):
       page = self.app.get('/storekeeper/', user=self.user1)

       page.form['piece']=u'Кресло'
       res=page.form.submit()
       res.form['model']='Кресло1'
       res.form['manufacturer']=self.prod.id
       res.form['dimensions']='36y3yx36'
       res.form['color']=self.color.id
       res.form['price']='255'
       res.form['material']=self.material.id
       res.form['has_gazopatron']=True
       #------------------------
       res1=res.form.submit('piece')
       #res1.showbrowser()	   
       assert 'Габариты должны быть формате(пример):55х55х55' in res1
       print(u"Ошибка в габаритах найдена")

    def testUpdate(self):
       page = self.app.get('/storekeeper/', user=self.user1)
       res=page.click(href="/furniture/update/"+str(self.shelf.id)+"/")
       #------------------------
       #res.showbrowser()	
       res.form['model']='Полка25'

       #------------------------
       res1=res.form.submit('piece').follow()
       #res1.showbrowser()	   
       assert 'Полка25' in res1
       assert 'Полка1' not in res1
	   
    def testPage(self):
       page = self.app.get('/storekeeper/', user=self.user1)
       
        #------------------------
       for s in range(1,25,1):
           page.form['piece']=u'Кресло'
           res=page.form.submit()
           res.form['model']='Кресло1'
           res.form['manufacturer']=self.prod.id
           res.form['dimensions']='36x36x36'
           res.form['color']=self.color.id
           res.form['price']='255'
           res.form['material']=self.material.id
           res.form['has_gazopatron']=True
       #------------------------
           page=res.form.submit('piece').follow()
	   
	   res=page.click(href="/storekeeper/see/")
	   #------------------------       
       assert u'Страница 1 из 3' in res
       print(u"Пагинация пройдена")
     
    def testCancelFirnitures(self):#тестим отмену покупку 
       page = self.app.get('/find/', user=self.user)
       #------------------------
       res=page.click(href="/furniture/"+str(self.shelf.id)+"/")
       #res.showbrowser() 
       res1=res.form.submit().follow()
       
       res=res1.click(href="/furniture/"+str(self.chair.id)+"/")
       res1=res.form.submit().follow()      
       #------------------------
       res2=res1.click(href="/basket").follow() 
       res3=res2.click(href="/cancel/orders/").follow()        
       #res3.showbrowser()
       assert u'<td> Чек №' not in res3
       assert '<td>Стул</td>' in page
       assert '<td>Стул1</td>' in page
       assert '<td>Cиний</td>' in page
       assert '<td>56x56x45</td>' in page
       str1='''<td>Полка</td>
		    <td>Полка1</td>
		    <td>Cиний</td>'''
       assert str1 in page
       #------------------------      
