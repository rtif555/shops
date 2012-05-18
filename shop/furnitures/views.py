# -*- coding: utf-8 -*-
import datetime

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.db.models import Sum

from shop.furnitures.forms import *

completedform=''
doesError=False

def find(request,orders=""):
    ord=orders #пришеший номер заказа
    basket=False  #Ссылка на корзину
    if orders!="":  # если составляем заказ то создаем ссылку на корзину
        basket=True	
    forms=FindForm(objects=PieceOfFurniture.objects.all())#форма поиска товара
    piese=PieceOfFurniture.objects.filter(statys=False)
    if request.method == 'POST':        
        objects=PieceOfFurniture.objects
        for item in forms.fields.keys():
            if request.POST[item]!='---------' and request.POST[item]!='':                    
                    if (item=='type'):
                        objects=objects.filter(type=request.POST[item])
                    if (item=='model'):
                        objects=objects.filter(model=request.POST[item])
                    if (item=='color'):
                        objects=objects.filter(color=request.POST[item])
                    if (item=='manufacturer'):
                        objects=objects.filter(manufacturer=request.POST[item])
                    piese=objects.filter(statys=False);					
        #piese=.filter(type=type).filter(model=model).filter(color=color).filter(manufacturer=manufacturer)
        		
    return render_to_response('abstractForm.html', {'title':'Поисковая форма',
                              'nameform':'find','form':forms.as_table, 
                              'pieceoffurnitures':piese, 'Orders':ord, 
                              'Basket':basket},   
                              context_instance=RequestContext(request))
	
def buy_web(request, offset,ord):
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
    ord=request.POST['Orders']
    if ord=="": #создаем новый заказ
        empl=Emploeer.objects.get(id=1)
        order=Order(emploeer=empl,statys=False)
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
    except ValueError:
        raise Http404()
    orders=Order.objects.get(id__exact=ord)
    if orders.statys==False:
        product_in_orders=FurnitureInOrders.objects.filter(id_orders=ord)
        price=PieceOfFurniture.objects.filter(id__in=(FurnitureInOrders.objects.filter(
               id_orders=ord).values_list('id_furniture'))).aggregate(Sum('price'))
        piese=PieceOfFurniture.objects.filter(id__in=product_in_orders.values_list('id_furniture'))
    return render_to_response('basket.html', {'nameform':'basket','pieceoffurnitures':piese, 
                              'Orders':ord, 'price__sum':price['price__sum']}, context_instance=RequestContext(request))

def cancel_product(request, offset,ord):
    try:
        ord = int(ord)
        offset = int(offset)#получили № товар и № зааказа
    except ValueError:
        raise Http404()
    if Order.objects.filter(id=ord).exists():
        PieceOfFurniture.objects.filter(id=offset).update(statys=False)#Делаем не зарезервированым товар
        FurnitureInOrders.objects.filter(id_orders=ord,id_furniture=offset).delete()#удаляем из списка заказов
        if FurnitureInOrders.objects.filter(id_orders=ord).exists()==False:#cписок товаров заказа пуст 
            Order.objects.filter(id=ord).delete()
            return HttpResponseRedirect("/find/")
        else:
            return HttpResponseRedirect("/basket"+str(ord))
    else:
        return HttpResponseRedirect("/find/") 

def cancel_orders(request,ord):
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
    try:
        ord = int(ord)
        #получили  № зааказа
    except ValueError:
        raise Http404()
    if Order.objects.filter(id=ord).exists():        
        Order.objects.filter(id=ord).update(statys=True)
        Order.objects.filter(id=ord).update(
		     cost=PieceOfFurniture.objects.filter(id__in=(
             FurnitureInOrders.objects.filter(
             id_orders=ord).values_list('id_furniture'))).aggregate(
             Sum('price')))
    return HttpResponseRedirect("/find/")


def store(request):
    #/проверить что это кладовщик
    global completedform
    completedform=''
    order=Order.objects.filter(statys=True,issuance=False)
    return render_to_response('storeForm.html', {'title':'Cклад',
                              'nameform':'add', 'orders':order},   
                              context_instance=RequestContext(request))

def storeorder(request,order):
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

def storeordergive(request,order):
    try:
        ord = int(order)
        #получили  № зааказа
    except ValueError:
        raise Http404()
    Order.objects.filter(id=ord).update(issuance=True)
    return HttpResponseRedirect("/storekeeper/")

def choseForm(type,param=None):    
    if type!='':
        if type==u"Шкафы":        
            form=CupboardFormAdd(param)
        elif type==u"Кресла":
            form=ArmchairFormAdd(param)
        elif type==u"Стулья":
            form=ChairFormAdd(param)
        elif type==u"Полки":
            form=ShelfFormAdd(param)
        return form
    return ''

def storeget(request):    
    global completedform, doesError 
    if completedform!='': 
        types=completedform.__type__
        if 'Action'in request.POST and request.POST['Action']==u'Добавить':
            form=ProduserFormAdd(request.POST)    
            instances=form.save()
        form=completedform
        if doesError:
            print (u'сделана ошибка')
            form=form.as_table
        else:
            form=form.as_tale
        completedform=''
    else:
        types=request.POST['Action']    
        if types=='':
           return HttpResponseRedirect("/storekeeper/")    
        form=ArmchairFormAdd()    
        form=choseForm(types)
        form=form.as_table	
    return render_to_response('storeAddForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':form,
							  'Type':types},
                               context_instance=RequestContext(request))


def storeadd(request):
    act=request.POST['Action']
    type=request.POST['Type']    
    global completedform, doesError
    completedform=choseForm(type,request.POST)    
    if act=='':
        return HttpResponseRedirect("/storekeeper/")
    if act==u'Добавить товар':
       form=choseForm(type,request.POST)
       if form.is_valid():     
           instances=form.save()       
           return HttpResponseRedirect("/storekeeper/")
       else: 
           doesError=True
           return HttpResponseRedirect("/storekeeper/get")		   
    if act==u'Добавить производителя':        
        form=ProduserFormAdd()
        return render_to_response('storeAddProdForm.html', {'title':'Добавление производителя',
                              'nameform':'gуеs', 'form':form.as_table,
							  'Type':type},
                               context_instance=RequestContext(request))
    if act==u'Назад':
        
        return storeget(request)					   