# -*- coding: utf-8 -*-
import datetime

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.db.models import Sum

from shop.furnitures.forms import *

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
    order=Order.objects.exclude(statys=False,issuance=True,emploeer=None)
    furnitures=PieceOfFurniture.objects.filter(date_give=datetime.date.today())
    return render_to_response('storeForm.html', {'title':'Cклад',
                              'nameform':'add', 'orders':order, 
                              'pieceoffurnitures':furnitures},   
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

def choose_form(type,param=None):    
    if type!='':
        if type==u"Шкаф":        
            form=CupboardFormAdd(param)
        elif type==u"Кресло":
            form=ArmchairFormAdd(param)
        elif type==u"Стул":
            form=ChairFormAdd(param)
        elif type==u"Полка":
            form=ShelfFormAdd(param)
        return form
    return ''
	

def storeget(request): 
    act=''
    type=''	
    if 'Action'in request.POST:
        act=request.POST['Action']
    if 'Type'in request.POST:
        type=request.POST['Type']
    if act=='':
        return HttpResponseRedirect("/storekeeper/")
    if act==u'Назад':
        return HttpResponseRedirect("/storekeeper/")
    if act==u'Добавить производителя':        
        form=ProduserFormAdd()
        return render_to_response('storeAddProdForm.html', 
                              {'title':'Добавление производителя',
                              'nameform':'gуеs', 'form':form.as_table,
							  'Type':type},
                               context_instance=RequestContext(request))
    if act==u'Добавить товар':
        form=choose_form(type,request.POST)
        if form.is_valid():     
            instances=form.save()       
            return HttpResponseRedirect("/storekeeper/")
        else: 
            return render_to_response('storeAddForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':form.as_table,
                              'Type':type},
                              context_instance=RequestContext(request))
    if act==u'Добавить':
        form=ProduserFormAdd(request.POST)
        if form.is_valid():     
            form.save() 		
            forms=choose_form(type)
            return render_to_response('storeAddForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':forms.as_table,
                              'Type':type},
                              context_instance=RequestContext(request))
        else:
            return render_to_response('storeAddProdForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':form.as_table,
                              'Type':type},
                              context_instance=RequestContext(request))		
    form=ArmchairFormAdd()         
    form=choose_form(act)
    type=act
    return render_to_response('storeAddForm.html', {'title':'прием',
                              'nameform':'gуе', 'form':form.as_table,
                              'Type':type},
                              context_instance=RequestContext(request))	

def storeupdate(request, offset=''):
    if offset!='':
        try:
            id= int(offset)
           #получили  № зааказа
        except ValueError:
            raise Http404()
        piece=PieceOfFurniture.objects.get(id__exact=id)
        shelf=Shelf.objects.get(id__exact=id)
        print(piece)
        form=choose_form(piece.type,shelf)
        return render_to_response('storeUpdateForm.html', {'title':'Изменение',
                              'nameform':'piece', 'form':form.as_table},
                              context_instance=RequestContext(request))			