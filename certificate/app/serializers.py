from rest_framework import serializers
from .models import Layout, Html, Component, Attribute


class HtmlSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Html
        fields = '__all__'
      

class ComponentSeralizers(serializers.ModelSerializer):
    
    class Meta:
        model=Component
        fields='__all__'
        
        
class AttributeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Attribute
        fields = '__all__'
       

class LayoutSerializers(serializers.ModelSerializer):
   
    html = HtmlSerializers(many=False)
    component = ComponentSeralizers(many=False)
    attribute = AttributeSerializers(many=False)
    
    def create(self, validated_data):
        html  = Html.objects.create(**validated_data['html'])    
        component = Component.objects.create(**validated_data['component'])
        attribute = Attribute.objects.create(**validated_data['attribute'])
        layout = Layout.objects.create(html=html,component=component,attribute=attribute)
        return layout
       
  
    class Meta:
        model=Layout
        fields = (
                    'html',
                    'component', 
                    'attribute',
                )
        
      