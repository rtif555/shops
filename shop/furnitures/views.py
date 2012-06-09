# -*- coding: utf-8 -*-
import datetime

from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.db.models import Sum
from django.views.generic.simple import direct_to_template
from shop.furnitures.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.uploadedfile import SimpleUploadedFile

def this_is(user,str=''):
    """Метод опрелделения пользователя на
    совершения тех или иных действий"""
    use=user.get_profile()
    if str=='':    
        return use.post
    if use.post==str:
        return True
    else:
        return False

def home(request):
    """Обычная заглушка на homepage"""
    return HttpResponseRedirect("/find/")
		
def choose_form(type,param=None,files=None,*args, **kwargs):
    """Метод возвращает объект формы для добавления предметов мебели"""
    if type!='':
        if type==u"Шкаф":        
            form=CupboardFormAdd(param,files,*args, **kwargs)
        elif type==u"Кресло":
            form=ArmchairFormAdd(param,files,*args, **kwargs)
        elif type==u"Стул":
            form=ChairFormAdd(param,files,*args, **kwargs)
        elif type==u"Полка":
            form=ShelfFormAdd(param,files,*args, **kwargs)
        return form
    else:
        raise NotFurnityreType("Unknown type of furniture")

def choose_model(type):
    """Возвращение модели по ее типу"""
    if type!='':
        if type==u"Шкаф":        
            model=Cupboard.objects
        elif type==u"Кресло":
            model=Armchair.objects
        elif type==u"Стул":
            model=Chair.objects
        elif type==u"Полка":
            model=Shelf.objects
        elif type=='---------':
            model=PieceOfFurniture.objects
        return model
    else:
        raise NotFurnityreType("Unknown type of furniture")

	
def choose_handbook(type,param=None,*args, **kwargs):
    """ Метод возвращает формы для добавления в справочники"""
    if type!='':            
        if type==u'Производитель':        
            form=ProduserFormAdd(param,*args, **kwargs)
        elif type==u'Цвет': 
            form=ColorFormAdd(param,*args, **kwargs)
        elif type==u'Материал':  
            form=MaterialFormAdd(param,*args, **kwargs)       
        return form
    else:
        raise NotHandbookType("Unknown type of handbook")
	
def help(request):
    """Выдают справку в соответсвии с должностью"""
    user=request.user
    if user.is_authenticated():
        if this_is(user,u'BM'):
            return render_to_response('help/helpSeller.html', 
                              context_instance=RequestContext(request))
        if this_is(user,u'KL'):
            return render_to_response('help/HelpStoreKeeper.html', 
                              context_instance=RequestContext(request))
        if this_is(user,u'DR'):
            return render_to_response('help/HelpDirector.html',
                              context_instance=RequestContext(request))
    else:
       	    return render_to_response('help/helpuser.html', 
                              context_instance=RequestContext(request))
	
		
def find(request,orders=""):
    """Поиск товаров по критериям"""
    ord=orders #пришеший номер заказа
    basket=False  #Ссылка на корзину
    BM=False
    user=request.user
    if user.is_authenticated():
        if this_is(user,u'BM') or this_is(user,u'DR'):
            BM=True
    if orders!="":  # если составляем заказ то создаем ссылку на корзину
        basket=True
    initial0={}
    objects=PieceOfFurniture.objects
    if request.method == 'POST':
        objects=choose_model(request.POST['type'])
        initial0['type']=request.POST['type']
        for item in request.POST:
            if request.POST[item]!='---------' and request.POST[item]!='':                    
                    if (item=='model'):
                        objects=objects.filter(model=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='color'):
                        objects=objects.filter(color=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='manufacturer'):
                        objects=objects.filter(manufacturer=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='material'):
                        objects=objects.filter(material=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='has_gazopatron'):
                        objects=objects.filter(has_gazopatron=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='quantity_of_doors'):
                        objects=objects.filter(quantity_of_doors=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='has_lock'):
                        initial0[item]=request.POST[item]
                        objects=objects.filter(has_lock=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='quantity_of_legs'):
                        objects=objects.filter(quantity_of_legs=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='height_spin'):
                        objects=objects.filter(height_spin=request.POST[item])
                        initial0[item]=request.POST[item]
                    if (item=='max_weight'):
                        objects=objects.filter(max_weight=request.POST[item])
                        initial0[item]=request.POST[item]

    form0=FindForm(initial=initial0,objects=PieceOfFurniture.objects.all())#форма поиска товара
    form1=ArmchairFormFind(initial=initial0)
    form2=CupboardFormFind(initial=initial0,objects=Cupboard.objects.all())
    form3=ChairFormFind(initial=initial0,objects=Chair.objects.all())
    form4=ShelfFind(initial=initial0,objects=Shelf.objects.all())
    piese=objects.filter(statys=False);
    pages=Paginator(piese, 10)
        #piese=.filter(type=type).filter(model=model).filter(color=color).filter(manufacturer=manufacturer)
    page1 = request.GET.get('page') 
    try: 
        page = pages.page(page1) 
    except PageNotAnInteger: # Если page не целое число, номер страницы=1 
        page = pages.page(1) 
    except EmptyPage: # Если значение page вышло за границу допустимых, показываем последнюю страницу 
        page = pages.page(pages.num_pages)    		
    return render_to_response('abstractForm.html', {'title':'Поисковая форма',
                              'nameform':'find','form':form0.as_table(),
                              'form1':form1.as_table(),'form2':form2.as_table(),
                              'form3':form3.as_table(),'form4':form4.as_table(),							  
                              'pieceoffurnitures':page, 'Orders':ord, 
                              'Basket':basket,'BM':BM},   
                              context_instance=RequestContext(request))
	
def buy_web(request, offset,ord):
    """Просмотр товара"""
    try:
        offset = int(offset)#получили № товар 
    except ValueError:
        raise Http404()
    piese=PieceOfFurniture.objects.get(id__exact=offset)
    return render_to_response('buyForm.html', {'title':'Товар',
                              'nameform':'buy','pieceoffurniture':piese, 
                              'Orders':ord},
                               context_instance=RequestContext(request))


def buy(request, offset,ord=""):
    """Резервирование мебели"""
    ord=request.POST['Orders']
    if ord=="": #создаем новый заказ
        #empl=Emploeer.objects.get(id=1)
        order=Order(emploeer=None,statys=False)
        order.save()        
        ord=order.id        
    else:
        try:
            ord = int(ord)
            offset = int(offset)#получили № товар и № зааказа
        except ValueError:
            raise Http404()
    orders=Order.objects.get(id__exact=ord)
    if orders.statys==False:
        piese=PieceOfFurniture.objects.get(id__exact=offset)
        piese.statys=True
        piese.save()
        product_in_orders=FurnitureInOrders(id_orders=orders,id_furniture=piese)
        product_in_orders.save()
    return HttpResponseRedirect("/find/"+str(ord))


def basket(request, ord):
    try:
        ord = int(ord)    
        orders=Order.objects.get(id__exact=ord)
    except ValueError,DoesNotExist:
        raise Http404()
    act=u"Зарезервировать"
    acts=True
    user=request.user
    name=''
    if user.is_authenticated():
        if this_is(user,u'BM') or this_is(user,u'DR'):
            act=u"Оформить"
            acts=False
            name=user.first_name+' '+user.last_name
    if orders.emploeer==None:
        product_in_orders=FurnitureInOrders.objects.filter(id_orders=ord)        
        price=PieceOfFurniture.objects.filter(id__in=(
                                             FurnitureInOrders.objects.filter(
                                             id_orders=ord).values_list(
                                             'id_furniture'))).aggregate(
                                             Sum('price'))
        piese=PieceOfFurniture.objects.filter(
                         id__in=product_in_orders.values_list('id_furniture'))
        return render_to_response('basket.html', {'nameform':'basket','Act':act,
		                       'Acts':acts,
                              'pieceoffurnitures':piese, 'Orders':ord, 
                              'price__sum':price['price__sum'], 'namebuyer': name}, 
                              context_instance=RequestContext(request))
    else:
        raise Http404()

							  
def cancel_product(request, offset,ord):
    """Отмена товара из заказа"""
    try:
        ord = int(ord)
        offset = int(offset)#получили № товар и № зааказа
    except ValueError:
        raise Http404()
    if Order.objects.filter(id=ord).exists():
        PieceOfFurniture.objects.filter(id=offset).update(statys=False)#Делаем не зарезервированым товар
        FurnitureInOrders.objects.filter(id_orders=ord,
                                         id_furniture=offset).delete()#удаляем из списка заказов
        if FurnitureInOrders.objects.filter(id_orders=ord).exists()==False:#cписок товаров заказа пуст 
            Order.objects.filter(id=ord).delete()
            return HttpResponseRedirect("/find/")
        else:
            return HttpResponseRedirect("/basket"+str(ord))
    else:
        return HttpResponseRedirect("/find/")
		

def cancel_orders(request,ord):
    """Отмена заказа"""
    try:
        ord = int(ord)
        #получили  № зааказа
    except ValueError:
        raise Http404()
    if Order.objects.filter(id=ord).exists():
        PieceOfFurniture.objects.filter(
             id__in=FurnitureInOrders.objects.filter(
             id_orders=ord).values_list("id_furniture")).update(statys=False)
        FurnitureInOrders.objects.filter(id_orders=ord).delete()
        Order.objects.filter(id=ord).delete()
    return HttpResponseRedirect("/find/")

	
def buyall(request,ord):
    """оформление всего заказа"""
    try:
        ord = int(ord)
        act=request.POST['Action']
        #получили  № зааказа
    except ValueError:
        raise Http404()
    user=request.user
    if act==u"Оформить" and user.is_authenticated():
        if this_is(user,u'BM') or this_is(user,u'DR'):
            if Order.objects.filter(id=ord).exists():        
                Order.objects.filter(id=ord).update(statys=True)
                Order.objects.filter(id=ord).update(emploeer=user.get_profile())
                Order.objects.filter(id=ord).update(
                                 emploeer=user.get_profile().id)
                cost1=PieceOfFurniture.objects.filter(id__in=(
                              FurnitureInOrders.objects.filter(
                                  id_orders=ord).values_list(
                                     'id_furniture'))).aggregate(
                                         Sum('price'))
                #print(cost1)
                Order.objects.filter(id=ord).update(
                          cost=cost1["price__sum"])
                order= Order.objects.get(id=ord)
                try:
                    internet_order=InternetOrders.objects.get(id_orders=order)
                    internet_order.delete()
                except InternetOrders.DoesNotExist:
                    print(u"Это не интернет заказ")
                return HttpResponseRedirect("/find/")
    if act==u"Зарезервировать":                
        return HttpResponseRedirect("/indification/"+str(ord)+"/") 


def internetorder(request,ord):
    """Интернет заказ"""
    try:
        ord = int(ord)
        #получили  № зааказа
    except ValueError:
        raise Http404()
    #print(ord)
    #print(request.POST["seria"]+" "+request.POST["number"])
    if request.POST and "seria" in request.POST:
        pattern='^\d{4}$'
        if re.match(pattern, request.POST["seria"]):
            pattern='^\d{6}$'
            if re.match(pattern, request.POST["number"]):
                id_ord=Order.objects.get(id=ord)
                orders=InternetOrders(id_orders=id_ord,
                passport=request.POST["seria"]+" "+request.POST["number"])
                orders.save() 
                Order.objects.filter(id=ord).update(statys=True)
                return HttpResponseRedirect("/find/")
            else:
                return render_to_response('ayntificationBuyer.html', {
                              "error":"Непрвильно указан номер паспорта",
                              "ord":ord
                              }, 
                              context_instance=RequestContext(request))
        else:
            return render_to_response('ayntificationBuyer.html', {
                              "error":"Непрвильно указана серия паспорта",
                               "ord":ord
                              }, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('ayntificationBuyer.html',  {"ord":ord},
                              context_instance=RequestContext(request))

def buyinternetorder(request):
    """ Регистрация персональных данных пользователя"""
    if request.POST:
        passport=request.POST["seria"]+" "+request.POST["number"]
        try:
            number=InternetOrders.objects.get(passport=passport)
            ord=number.id_orders			
        except InternetOrders.DoesNotExist:		
            return render_to_response('ayntificationBuyer.html', {
                                      'error':'С таким данными интернет '+
                                      'заказов не поступало'
                                     },
                                     context_instance=RequestContext(request))
        except InternetOrders.MultipleObjectsReturned:
            number=InternetOrders.objects.filter(passport=passport)
            orders=Order.objects.filter(id__in=number.values_list('id_orders'))
            orders=orders.filter(emploeer=None)
            return render_to_response('ayntificationBuyer.html', {
                                      'orders':orders
                                     },
                                     context_instance=RequestContext(request))
        if number:        
            return HttpResponseRedirect("/basket"+str(ord.id)+"/")
           
    return render_to_response('ayntificationBuyer.html', 
                              context_instance=RequestContext(request))


def store(request):
    """Рабочая зона кладовщика"""
    user=request.user
    if user.is_authenticated():
        if this_is(user,u'KL') or this_is(user,u'DR'):
            order=Order.objects.exclude(statys=False)
            order=order.exclude(issuance=True)
            order=order.exclude(emploeer=None)
            form=TypeForm()
            try:
                chairs=PieceOfFurniture.objects.filter(statys=False).latest('id')
            except PieceOfFurniture.DoesNotExist:
                chairs=''
            return render_to_response('storeForm.html', {'title':'Cклад','form':form.as_tale,
                              'nameform':'add', 'orders':order, 'chairs':chairs},   
                              context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/find/")
    else:
        return HttpResponseRedirect("/avtoriz/")
		
		
def store_see_furniture(request):
    """Просмотр имеющихся товаров"""
    user=request.user
    if user.is_authenticated():
        manafactyrer=''
        if 'manufacturer'in request.POST:
                manafactyrer=request.POST['manufacturer']
        if this_is(user,u'KL') or this_is(user,u'DR'):
            chairs=Chair.objects.filter(statys=False)
            armchairs=Armchair.objects.filter(statys=False)
            cupboards=Cupboard.objects.filter(statys=False)			
            furnitures=Shelf.objects.filter(statys=False)		
            objects=list(armchairs)+list(cupboards)+list(furnitures)+list(chairs)
            pages=Paginator(objects, 10)
			
            if manafactyrer!='':
                chairs=chairs.filter(manufacturer=manafactyrer)
                armchairs=armchairs.filter(manufacturer=manafactyrer)
                cupboards=cupboards.filter(manufacturer=manafactyrer)
                furnitures=furnitures.filter(manufacturer=manafactyrer)
                objects=list(armchairs)+list(cupboards)+list(furnitures)+list(chairs)
                pages=Paginator(objects, 10)
            form=ProduserForm(initial=request.POST)
            page1 = request.GET.get('page') 
            try: 
               page = pages.page(page1) 
            except PageNotAnInteger: # Если page не целое число, номер страницы=1 
               page = pages.page(1) 
            except EmptyPage: # Если значение page вышло за границу допустимых, показываем последнюю страницу 
               page = pages.page(pages.num_pages) 
            #furniture=chairs[:]+armchairs[:]+cupboards[:]+furnitures[:]
            return render_to_response('storeSee.html', {'title':'Просмотр',
                              'nameform':'add', 
                              'furnityres': page,
                               "form":form.as_tale()},   
                              context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/find/")
    else:
        return HttpResponseRedirect("/avtoriz/")
 
def storeorder(request,order):
    """Просмотр товаров в заказе"""
    user=request.user
    if user.is_authenticated():
        if this_is(user,u'KL') or this_is(user,u'DR'):
            try:
                ord = int(order)
              #получили  № зааказа
            except ValueError:
                raise Http404()
            piese=PieceOfFurniture.objects.filter(id__in=(
	             FurnitureInOrders.objects.filter(
				 id_orders=ord).values_list('id_furniture')))
            return render_to_response('storeOrderForm.html', {'title':'Выдача',
                              'nameform':'give', 'pieceoffurnitures': piese},
                               context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/find/")
    else:
        return HttpResponseRedirect("/avtoriz/")


def storeordergive(request,order):
    """Выдача заказа"""
    user=request.user
    if user.is_authenticated():
        if this_is(user,u'KL') or this_is(user,u'DR'):
            try:
                ord = int(order)
                #получили  № зааказа
            except ValueError:
                raise Http404()
            Order.objects.filter(id=ord).update(issuance=True)
            return HttpResponseRedirect("/storekeeper/")
        else:
            return HttpResponseRedirect("/find/")
    else:
        return HttpResponseRedirect("/avtoriz/")
	
#самый большой костыль
def storeget(request):
    user=request.user
    if user.is_authenticated():
        if this_is(user,u'KL') or this_is(user,u'DR'): 
            act=''
            type=''
            what=''				
            if 'piece'in request.POST:
                act=request.POST['piece']
            if 'Type'in request.POST:
                type=request.POST['Type']
            if 'what'in request.POST:
                what=request.POST['what']
                
            if act==u'Назад':
                return HttpResponseRedirect("/storekeeper/")
			#добавляем в справочники	
            if act==u'Добавить':
                form=choose_handbook(what,request.POST)
                if form!='':
                    if form.is_valid():     
                        form.save() 		
                        forms=choose_form(type)
                        return render_to_response('storeAddForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':forms.as_table,
                              'Type':type,'what':what},
                              context_instance=RequestContext(request))
                    else:
                        return render_to_response('storeAddProdForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':form.as_table,
                              'Type':type,'what':what},
                              context_instance=RequestContext(request))
                else:
				    return HttpResponseRedirect("/storekeeper/")				
 			#создаем форму справочников 							  
            if what!='':        
                form=choose_handbook(what)
                if form!='':
                    return render_to_response('storeAddProdForm.html', 
                              {'title':'Добавление',
                              'nameform':'gуеs', 'form':form.as_table,
                              'Type':type,'what':what},
                               context_instance=RequestContext(request))
                else:
				    return HttpResponseRedirect("/storekeeper/")
 			#добавляем в товар	           
            if act==u'Добавить товар':
                form=choose_form(type,request.POST,request.FILES)
                if form.is_valid():
                    form.save()
                    #user.message_set.create(
                       # message=form.type+form.model+" был успешно добавлен.")
                    return HttpResponseRedirect("/storekeeper/")
                else: 
                    return render_to_response('storeAddForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':form.as_table,
                              'Type':type},
                              context_instance=RequestContext(request))

            form=choose_form(act)
            type=act
            return render_to_response('storeAddForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':form.as_table,
                              'Type':type},
                              context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/find/")
    else:
        return HttpResponseRedirect("/avtoriz/")
	
def storeupdate(request, offset=''):
    """Изменение товара"""
    if offset!='':
        try:
            id= int(offset)
           #получили  № заказа
        except ValueError:
            raise Http404()
        if request.POST:
            try:
                furnityre=choose_model(request.POST["Type"])
                furnityre=furnityre.get(id=request.POST["id"])
                form=choose_form(request.POST["Type"],request.POST,request.FILES)
                if form.is_valid():                    
                    form.save()#добавляем новую
                    chairs=PieceOfFurniture.objects.latest('id')
                    if chairs.image=="":
                        ob=PieceOfFurniture.objects.get(id=chairs.id)
                        ob.image=furnityre.image
                        ob.save()
                    furnityre.delete()#удаляем старую
                    return HttpResponseRedirect("/storekeeper/")
                else: 
                    return render_to_response('storeUpdateForm.html', {'title':'Изменение',
                              'nameform':'piece', 'form':form.as_table,
                              'Type':type},
                              context_instance=RequestContext(request))
                #furnityre.update(request.POST)
                return HttpResponseRedirect("/storekeeper/")
            except:
                raise Http404()			
        piece=PieceOfFurniture.objects.get(id__exact=id)
        shelf=choose_model(piece.type)
        shelf=shelf.filter(id__exact=id).values()
        piece_furniture=shelf[0]
        piece_furniture["manufacturer"]=shelf[0]["manufacturer_id"]
        piece_furniture["color"]=shelf[0]["color_id"]
        if "material_id" in shelf[0]:
            piece_furniture["material"]=shelf[0]["material_id"]		
        form=choose_form(piece.type,piece_furniture)
        image=piece.image
        return render_to_response('storeUpdateForm.html', {'title':'Изменение',
                              'nameform':'piece', 'Id':id, 'Type': piece.type,
                              'form':form,'image':image},
                              context_instance=RequestContext(request))

def logout(request):
    """Выход"""
    auth.logout(request)
    return HttpResponseRedirect("/avtoriz/")

def avtorization(request):
    """Страница авторизации"""
    return render_to_response('Avtorization.html', {'Error':''},
                              context_instance=RequestContext(request))	

def enter(request):
    """Индификация"""
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
        auth.login(request, user)        
        if this_is(user,u'KL'):
           return HttpResponseRedirect("/storekeeper/")
        if this_is(user,u'BM'):
           return HttpResponseRedirect("/find/")
        if this_is(user,u'DR'):
           return HttpResponseRedirect("/admin/")
    else:
        # Отображение страницы с ошибкой
        return render_to_response('Avtorization.html', {'error':'Неправильная пара логин-пароль'},
                              context_instance=RequestContext(request))

def statistics(request):
    """Статистика Заказов"""
    user=request.user
    if user.is_superuser:
         title = u"Статистика" #берем название из модели, что бы не хардкодить в двух местах   
         registery = []
         form=DataOrders()
         dict_ord={}
         dict_count={"data": u"Итого", "chair": 0, "armchair": 0, "cupboard": 0, "shelf":0}
         date_by=datetime.date.today()
         date_with=datetime.date.today()+datetime.timedelta(days=-30)
         if request.POST:
             form=DataOrders(request.POST)
             if form.is_valid():
                 print('ff')
                 date_with=form.cleaned_data['date_with']
                 date_by=form.cleaned_data['date_by']
         orders=Order.objects.filter(issuance=True)
         orders=orders.filter(date_orders__gte=date_with)
         orders=orders.filter(date_orders__lte=date_by)
         for order in orders:
            dict_ord["data"]=order.date_orders
            dict_ord["cost"]=order.cost
            furnitures=FurnitureInOrders.objects.filter(id_orders=order.id)
            dict_ord["chair"]=PieceOfFurniture.objects.filter(
                                     id__in=furnitures.values_list(
                                     "id_furniture")).filter(
                                     type=u"Стул").aggregate(models.Count(
                                     'type'))["type__count"]
            dict_count["chair"]=dict_count["chair"]+dict_ord["chair"]
            dict_ord["armchair"]=PieceOfFurniture.objects.filter(
                                     id__in=furnitures.values_list(
                                     "id_furniture")).filter(
                                     type=u"Кресло").aggregate(models.Count(
                                     'type'))["type__count"]
            dict_count["armchair"]=dict_count["armchair"]+dict_ord["armchair"]									 
            dict_ord["cupboard"]=PieceOfFurniture.objects.filter(
                                     id__in=furnitures.values_list(
                                     "id_furniture")).filter(
                                     type=u"Шкаф").aggregate(models.Count(
                                     'type'))["type__count"]
            dict_count["cupboard"]=dict_count["cupboard"]+dict_ord["cupboard"]									 
            dict_ord["shelf"]=PieceOfFurniture.objects.filter(
                                     id__in=furnitures.values_list(
                                     "id_furniture")).filter(
                                     type=u"Полка").aggregate(models.Count(
                                     'type'))["type__count"]					 
            dict_count["shelf"]=dict_count["shelf"]+dict_ord["shelf"]
            registery.append(dict_ord)
            dict_ord={}
         dict_count["cost"]=orders.aggregate(models.Sum('cost'))["cost__sum"]
         registery.append(dict_count)
   			 
        #какая-то логика выбора logger-ов для отображения
        

         context = {
            'form': form,
            'registery': registery,   #список logger-ов для отображения
            'filter_choices': '',
            'title': title
         }
         return direct_to_template(request, 'changelist_view.html', context)
















							  