from django.core.management.base import *
from optparse import make_option
from shop.furnitures.models import *
import datetime

class Command(BaseCommand):
    help = 'Prints model names for given application and optional object count.'
    args = '[appname ...]'

    def handle(self, *args, **options):
        date1=datetime.date.today()+datetime.timedelta(days=-10)
        ord=Order.objects.filter(date_orders__lt=date1).filter(issuance=False).filter(emploeer=None)
        print(ord)
        iord=InternetOrders.objects.filter(id_orders__in=ord.values_list('id'))
        ords=Order.objects.filter(id__in=iord.values_list('id_orders'))
        for order in ords:
            fino=FurnitureInOrders.objects.filter(id_orders=order.id)
            PieceOfFurniture.objects.filter(id__in=fino.values_list('id_furniture')).update(statys=False)
            fino.delete()
        ords.delete()
        iord.delete()
        return " "