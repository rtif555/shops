# -*- coding: utf-8 -*- 
from django import forms 
from django.conf import settings 
from django.utils.safestring import mark_safe 
 
class DatePickerWidget(forms.DateInput): 
    class Media: 
        css = { 
            'all': (settings.MEDIA_URL+"jquery-ui-1.8.20.custom.css",) 
        } 
        js = ( 
            settings.MEDIA_URL+"js/jquery-1.7.2.min.js", 
            settings.MEDIA_URL+"js/jquery-ui-1.8.20.custom.min.js", 
            settings.MEDIA_URL+"js/jquery.ui.datepicker-ru.js", 
        ) 
 
    def __init__(self, params='', attrs=None): 
        self.params = params 
        super(DatePickerWidget, self).__init__(attrs=attrs) 
 
    def render(self, name, value, attrs=None): 
        rendered = super(DatePickerWidget, self).render(name, value, attrs=attrs) 
        return rendered + mark_safe(u'''<script type="text/javascript"> 
            $('#id_%s').datepicker({%s}); 
            </script>'''%(name, self.params,)) 
