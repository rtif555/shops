from django.forms import *
from shop.furnitures.models import *
from django.forms.widgets import SelectMultiple, Select
from django.db.models.query import QuerySet
import re

class FindForm(Form):  
    type=TypedChoiceField(label = u"Тип")
    model=TypedChoiceField(label = u"Модель")             
    color=TypedChoiceField(label = u"Цвет")
    manufacturer=ModelChoiceField(label = u"Производитель", queryset = Producer.objects.none(), empty_label = '---------')	 
    
    def __init__(self,*args, **kwargs):        
        super(FindForm, self).__init__(*args, **kwargs)
        	
    def __init__(self, objects,*args, **kwargs):        
        super(FindForm, self).__init__(*args, **kwargs)		
        substitution=PieceOfFurniture.objects.all()
        for item in self.fields.keys():  #формируем select(-------,[выборка из базы])
            if item!='manufacturer':
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
    material=TypedChoiceField(label=u"Материал")
    has_gazopatron=TypedChoiceField(label=u"Газоптрон")
	
    def __init__(self, objects,*args, **kwargs):        
        super(ArmchairFormFind, self).__init__(*args, **kwargs)		
        substitution=Armchair.objects.all()
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
            normal_row = u'<th class="arm">%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = False)			
        

class CupboardFormFind(Form):    
    quantity_of_doors=TypedChoiceField(label=u"Количество дверей")
    has_lock=TypedChoiceField(label=u"Наличие замка")
	
    def __init__(self, objects,*args, **kwargs):        
        super(CupboardFormFind, self).__init__(*args, **kwargs)		
        substitution=Cupboard.objects.all()
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