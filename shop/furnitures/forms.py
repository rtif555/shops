from django.forms import *
from shop.furnitures.models import *
from shop.furnitures.widgets import DatePickerWidget
from django.forms.widgets import DateInput
from django.db.models.query import QuerySet
import re



class FindForm(Form):  
    type=TypedChoiceField(label = u"Тип")
    model=TypedChoiceField(label = u"Модель")             
    color=ModelChoiceField(label = u"Цвет", queryset = Color.objects.all(), empty_label = '---------')	
    manufacturer=ModelChoiceField(label = u"Производитель", queryset = Producer.objects.none(), empty_label = '---------')

    def __init__(self,*args, **kwargs):
        super(FindForm, self).__init__(*args, **kwargs)

    def __init__(self, objects,*args, **kwargs):
        super(FindForm, self).__init__(*args, **kwargs)
        substitution=PieceOfFurniture.objects.all()
        for item in self.fields.keys():  #формируем select(-------,[выборка из базы])
            if item!='manufacturer' and item!='color':
                if item!='type':
                    substitution=objects
                else:
                    substitution.query.group_by = [item]
                self.fields[item].choices=substitution.values_list(item,item)
                self.fields[item].choices.insert(0,('---------','---------'))
        self.fields['manufacturer'].queryset=Producer.objects.filter(id__in=objects.values_list("manufacturer"))

    def as_table(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)

class ArmchairFormFind(Form):
    material=ModelChoiceField(label = u"Материал", queryset = Material.objects.none(), empty_label = '---------')
    has_gazopatron=BooleanField(label=u"Газопатрон")
  
    def as_table(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<th class="arm">%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)			
        

class CupboardFormFind(Form):    
    quantity_of_doors=TypedChoiceField(label=u"Количество дверей")
    has_lock=BooleanField(label=u"Наличие замка")
	
    def __init__(self, objects,*args, **kwargs):        
        super(CupboardFormFind, self).__init__(*args, **kwargs)		
        substitution=Cupboard.objects.all()
        substitution.query.group_by = ["quantity_of_doors"]
        self.fields["quantity_of_doors"].choices=substitution.values_list("quantity_of_doors","quantity_of_doors")
        self.fields["quantity_of_doors"].choices.insert(0,('---------','---------')) 

    def as_table(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<th class="cup">%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)			

class ChairFormFind(Form):
    quantity_of_legs=TypedChoiceField(label = u"Количество ножек ")
    height_spin=TypedChoiceField(label=u"Высота спинки")
	
    def __init__(self, objects,*args, **kwargs):        
        super(ChairFormFind, self).__init__(*args, **kwargs)		
        substitution=Chair.objects.all()
        for item in self.fields.keys():  #формируем select(-------,[выборка из базы])
            #if item!='type':
                #substitution=objects
            #else:
            substitution.query.group_by = [item]
            self.fields[item].choices=substitution.values_list(item,item)
            self.fields[item].choices.insert(0,('---------','---------'))

    def as_table(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<th class="chr">%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)
			
class ShelfFind(Form):
    max_weight=TypedChoiceField(label=u"Максимальная масса содержимого")#

    def __init__(self, objects,*args, **kwargs):        
        super(ShelfFind, self).__init__(*args, **kwargs)		
        substitution=Shelf.objects.all()
        for item in self.fields.keys():  #формируем select(-------,[выборка из базы])
            #if item!='type':
                #substitution=objects
            #else:
            substitution.query.group_by = [item]
            self.fields[item].choices=substitution.values_list(item,item)
            self.fields[item].choices.insert(0,('---------','---------'))
			
    def as_table(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<th class="shelf">%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)
				
class ArmchairFormAdd(ModelForm):
    class Meta:
        model = Armchair
        exclude = ('statys',)

    def clean_dimensions(self):
        data = self.cleaned_data['dimensions']
        pattern_number0=u'^[0-9]{1,3}'
        pattern_number1=u'[0-9]{1,3}'
        pattern_x=u'[x|х]'
        pattern=pattern_number0+pattern_x+pattern_number1+pattern_x+pattern_number1+'$'
        if re.match(pattern, data) is None:
            raise forms.ValidationError(u"Габариты должны быть формате(пример):55х55х55")        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
		
    def as_tale(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<tr><th>%(label)s</th><td>%(field)s%(help_text)s</td></tr>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)

class ChairFormAdd(ModelForm):
    quantity_of_legs=IntegerField(label=u"Количество ножек",
	                              max_value=10, 
                                  min_value=1)#
    height_spin=IntegerField(label=u"Высота спинки",
	                               max_value=150, 
                                   min_value=1)#
	
    class Meta:
        model = Chair
        exclude = ('statys',)

    def clean_dimensions(self):
        data = self.cleaned_data['dimensions']
        pattern_number0=u'^[0-9]{1,3}'
        pattern_number1=u'[0-9]{1,3}'
        pattern_x=u'[x|х]'
        pattern=pattern_number0+pattern_x+pattern_number1+pattern_x+pattern_number1+'$'
        if re.match(pattern, data) is None:
            raise forms.ValidationError(u"Габариты должны быть формате(пример):55х55х55")        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
		
    def as_tale(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<tr><th>%(label)s</th><td>%(field)s%(help_text)s</td></tr>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)

class CupboardFormAdd(ModelForm):
    quantity_of_doors=IntegerField(max_value=10, 
                                   min_value=1,label=u"Количество дверей")
    class Meta:
        model = Cupboard
        exclude = ('statys',)
    
    def as_tale(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<tr><th>%(label)s</th><td>%(field)s%(help_text)s</td></tr>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)

    def clean_dimensions(self):
        data = self.cleaned_data['dimensions']
        pattern_number0=u'^[0-9]{1,3}'
        pattern_number1=u'[0-9]{1,3}'
        pattern_x=u'[x|х]'
        pattern=pattern_number0+pattern_x+pattern_number1+pattern_x+pattern_number1+'$'
        if re.match(pattern, data) is None:
            raise forms.ValidationError(u"Габариты должны быть формате(пример):55х55х55")        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
		
    def __type__(self):
        return u'Шкафы'

		
class ShelfFormAdd(ModelForm):
    max_weight=IntegerField(max_value=350,
               label=u"Максимальная масса содержимого",
               min_value=1)
    class Meta:
        model = Shelf
        exclude = ('statys',)

    def clean_dimensions(self):
        data = self.cleaned_data['dimensions']
        pattern_number0=u'^[0-9]{1,3}'
        pattern_number1=u'[0-9]{1,3}'
        pattern_x=u'[x|х]'
        pattern=pattern_number0+pattern_x+pattern_number1+pattern_x+pattern_number1+'$'
        if re.match(pattern, data) is None:
            raise forms.ValidationError(u"Габариты должны быть формате(пример):55х55х55")        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def as_tale(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<tr><th>%(label)s</th><td>%(field)s%(help_text)s</td></tr>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)

			
class ProduserForm(Form):
    manufacturer=ModelChoiceField(label = u"Производитель", queryset = Producer.objects.all(), empty_label = '---------')	
    def as_tale(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<th>%(label)s</th><td>%(field)s%(help_text)s</td>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)
			
			
class ProduserFormAdd(ModelForm):
    class Meta:
        model = Producer
    
    def clean_phone(self):
        data = self.cleaned_data['phone']
        pattern=u'^(\d|[pw+]){4,}$'
        if re.match(pattern, data) is None:
            raise forms.ValidationError(u"Номер телефона числа  должен быть более 4 знаков")        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
		
class ColorFormAdd(ModelForm):
    class Meta:
        model = Color
		
class TypeForm(Form):
    piece=TypedChoiceField(label = u"Тип")
    def __init__(self,*args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)
        self.fields['piece'].choices=[('Кресло',u'Кресло'),('Стул',u'Стул'),('Шкаф',u'Шкаф'),('Полка',u'Полка')]
		
    def as_tale(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<th>%(label)s</th><td>%(field)s%(help_text)s</td>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)	
			
class MaterialFormAdd(ModelForm):
    class Meta:
        model = Material

class DataOrders(Form):
    date_with=DateField(label="C:",widget=DatePickerWidget(params="dateFormat: 'dd.mm.yy', changeYear: true,  yearRange: 'c-15:c+15'" ,attrs={'class': 'datepicker',}))
    date_by=DateField(label=" По:",widget=DatePickerWidget(params="dateFormat: 'dd.mm.yy', changeYear: true,  yearRange: 'c-15:c+15'" ,attrs={'class': 'datepicker',}))
    
    def clean_date_by(self):
        data = self.cleaned_data['date_with']
        print(data)
        data2 = self.cleaned_data['date_by']
        print(data2)
        if data>data2:
            raise forms.ValidationError(u"Первая дата должна быть меньше чем вторая дата")        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def as_tale(self):
        "Returns this form rendered as HTML <t>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<tr><th>%(label)s</th><td>%(field)s%(help_text)s</td></tr>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)