import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import pdfkit
import qrcode
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ItemModel
from django.template.loader import render_to_string
from django.utils import timezone


class CashRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        
        items_id = request.data.get('items', [])
        
        
        check_items = ItemModel.objects.filter(id__in=items_id)
        if not check_items.exists():
            return Response(status=400, data={"error": "Товары не найдены"})

       
        amount = sum(i.price for i in check_items)

  
        context = {
            "items": check_items,
            "amount": amount,
            "time": timezone.localtime(timezone.now()).strftime('%d.%m.%Y %H:%M'),
        }

       
        html = render_to_string("check_template.html", context)
        config = pdfkit.configuration(wkhtmltopdf=r'C:/Users/Clavicus/Desktop/wkhtmltopdf/bin/wkhtmltopdf.exe')
    
        try:
            pdf = pdfkit.from_string(html, False, configuration=config)
        except Exception as e:
            return Response(status=500, data={"error": f"Ошибка при генерации PDF: {str(e)}"})


        media_dir = "media/"
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)


        file_name = f"receipt_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"
        file_path = os.path.join(media_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(pdf)


        qr = qrcode.make(f"{request.build_absolute_uri('/')}media/{file_name}")
        qr_path = os.path.join(media_dir, f"{file_name}_qr.png")
        qr.save(qr_path)


        return JsonResponse({
            'qr_code_url': f"{request.build_absolute_uri('/media')}/{file_name}_qr.png",  
            'pdf_url': f"{request.build_absolute_uri('/media')}/{file_name}",  
            })