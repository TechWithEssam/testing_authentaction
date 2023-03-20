from django import forms
from .models import *

class ProductForm(forms.ModelForm) :
    class Meta :
        model = Product
        fields = (          
            "name",              
            "price" ,            
            "brand" ,            
            "category",        
            "gender",            
            "discound",        
            "inventory_quantity",
            "description" ,      
            "location"        
        )
        widgets = {
                'description': forms.Textarea(attrs=({"rows":"4","cols":"20"}))
            }
        
class ImageForm(forms.ModelForm) :
    class Meta :
        model = Images
        fields = (
            "image",
        )
        widgets = {
                'image': forms.ClearableFileInput(attrs={'multiple': True})
            }
        