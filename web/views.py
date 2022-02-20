from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from web.deblur import deblur
from web.deblur import format_image
from PIL import Image

#from .models import Pictures


def test(request):
    return render(request, 'app/join.html')

def loading(request):
    return request(request,'app/loading.html')

def upload(request):
    # 从请求当中　获取文件对象
    f1 = request.FILES.get('picture')
    # 把上传的图片写入到新建文件当中
    fname = settings.MEDIA_ROOT + '/own_images/' + f1.name
    with open(fname, 'wb') as pic:
        for c in f1.chunks():
            pic.write(c)
    deblur("web/generator.h5", "static/images/own_images", "static/images/results")
    blur, full = format_image('static/images/results/' + f1.name , size=256)

    im = Image.fromarray(full)
    im.save("static/images/ans/"+f1.name)
    return render(request, 'app/main.html',{'upimg':f1.name})


def show(f1):
    fname = settings.MEDIA_ROOT + '/ans/' + f1.name
    with open(fname, 'wb') as pic:
        for c in f1.chunks():
            pic.write(c)
    return