from rest_framework import serializers
from ..models import Layout, Html, Component, Attribute
from htmlSerializers import HtmlSerializers
from componentSerializers import ComponentSerializers
from attributeSerializers import AttributeSerializers


class LayoutSerializers(serializers.ModelSerializer):
   
    html = HtmlSerializers(many=False)
    component = ComponentSerializers(many=False)
    attribute = AttributeSerializers(many=False)
    
    def create(self, validated_data):
        html = Html.objects.create(**validated_data['html'])
        component = Component.objects.create(**validated_data['component'])
        attribute = Attribute.objects.create(**validated_data['attribute'])
        layout = Layout.objects.create(html=html, component=component, attribute=attribute)
        return layout

    class Meta:
        model = Layout
        fields = (
                    'html',
                    'component', 
                    'attribute',
                )
        
      