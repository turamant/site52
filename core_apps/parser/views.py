import io
from datetime import datetime
import json
import os

import requests
from django.core.files import File

from django.http import JsonResponse, FileResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect


from . import models
from .forms import CoinForm
from .models import Document
from .services import coin_rate, string_current_date_time, make_pdf_file,\
    make_csv_file, make_xlsx_file


URL = "https://api.coingecko.com/api/v3/simple/price/?ids=bitcoin,ethereum,ripple,cardano," \
      "litecoin,monero,dogecoin,tether,solana,polkadot&vs_currencies=usd,eur,gbp"


def response_api():
    """ответ на запрос от URL"""
    response = requests.get(URL)
    data = json.loads(response.content.decode("utf-8"))
    return data


def req_info(request):
    context = {"PATH": request.path, "BODY": request.body, "PATH_INFO": request.path_info,
               "SCHEME": request.scheme, "Method": request.method, "GET": request.GET,
               "POST": request.POST, "content-type": request.content_type,
               "content_params": request.content_params, "COOKIES": request.COOKIES,
               "HEADERS": request.headers,
               "Resolver match": request.resolver_match,
               "SESSION": request.session,
               "USER": request.user, "GET_HOST": request.get_host(), "GET_Port": request.get_port(),
               "GET_FULL_PATH": request.get_full_path(), "absoluteURI": request.build_absolute_uri(location=None)
               }
    print("......", context)
    return render(request, 'parser/request_info.html', context=context)


def my_file(request):
    with open("hello_file.txt", "w") as f:
        file = File(f)
        file.write("hello my baby to night")
        return HttpResponse(
            content_type='text/pline',
            headers={
                "Content-Disposition": f"attachment; filename={file}"
            })


def view_index_all(request):
    """показ котировок всех монет"""
    data = response_api()
    for k, v in data.items():
        coin_rate[k] = v
    return render(request, "parser/index-all.html", {"data": data, "currenttime": string_current_date_time})


def view_homepage(request):
    """показ главной страницы"""
    coin_rate.clear()
    return render(request, "parser/homepage.html")


def view_json(request):
    """показ api/json"""
    data = response_api()
    return JsonResponse(data)


def come_back_and_clear_dict(request):
    """очистить словарь и вернуться назад к форме"""
    coin_rate.clear()
    return redirect("form")


def select_coins_from_form(request):
    """выбрать монеты из формы"""
    data = response_api()
    select_keys = []
    form = CoinForm()
    if request.method == "POST":
        form = CoinForm(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value:
                    select_keys.append(key)
            for k, v in data.items():
                for i in select_keys:
                    if k == i:
                        coin_rate[k] = v

            return render(request, "parser/detail.html", {"data": coin_rate, "currenttime": string_current_date_time })
    context = {
        "form": form,
    }
    return render(request, "parser/form.html", context)


def export_to_csv(request):
    """экспортировать в csv"""
    file_name = '{}.csv'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    response = HttpResponse(
        content_type='text/csv',
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
    make_csv_file(response)
    return response


def export_to_pdf(request):
    """экспортировать в pdf"""
    filepath = make_pdf_file()
    response = FileResponse(open(filepath, "rb"), content_type="application/pdf")
    return response


def export_to_xlsx(request):
    """экспортировать в pdf"""
    file_name = "{}.xlsx".format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    response = HttpResponse(
        content_type="text/xlsx",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
    make_xlsx_file(response)
    return response





#===========================================  дополнительные ф-ции

def all_file_view(request):
    """Показать список всех файлов в БД"""
    documents = models.Document.objects.all()
    return render(request, "parser/all-file.html", context={
        "files": documents})


def pdf_file_view(request, id):
    """ Готово вывод на экран файла PDF"""
    obj = Document.objects.get(pk=id)
    file = str(obj.uploadedFile)
    filepath = os.path.join("media", file)
    return FileResponse(open(filepath, "rb"), content_type="application/pdf")


def uploadFile(request):
    """Загрузить в БД свои файлы"""
    if request.method == "POST":
        file_title = request.POST["fileTitle"]
        uploaded_file = request.FILES["uploadedFile"]
        document = models.Document(
            title=file_title,
            uploadedFile=uploaded_file
        )
        document.save()
    documents = models.Document.objects.all()

    return render(request, "parser/upload-file.html", context={
        "files": documents
    })

def export_to_pdf_PAC(request):
    """экспортировать в pdf"""
    file_name = "{}.pdf".format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    file_buf = io.BytesIO()
    c = canvas.Canvas(file_buf, pagesize=elevenSeventeen, bottomup=0)
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont("Helvetica", 12)

    lines = []

    for key, value in coin_rate.items():
        lines.append(str(key))
        lines.append("-----------------")
        for k, v in value.items():
            lines.append((str(k)))
            lines.append(str(v))
        lines.append("----------------------------------------------------------------")

    for line in lines:
        text_obj.textLine(line)

    c.drawString(20, 10, f'{string_current_date_time()}')
    c.drawString(300, 20, "Cryptocurrency rate 2022 (c) turamant")
    c.drawText(text_obj)
    c.showPage()
    c.save()
    file_buf.seek(0)
    response = FileResponse(file_buf, as_attachment=True, filename=file_name)
    return response

