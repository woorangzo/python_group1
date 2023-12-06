import mysql.connector
from django.core.paginator import Paginator
from django.shortcuts import render

mydb = mysql.connector.connect(
    host="localhost",
    user="woorangzo",
    passwd="1234",
    database="woorangzo"
)

mc = mydb.cursor(prepared=True)


def newsList(request):
    page = request.GET.get('page', '1')
    sql = "select news_title,news_date,news_content,news_id from news where news_type = 'flash' order by news_date desc "
    try:
        mc.execute(sql)
    except mysql.connector.Error as err:
        print("news_list Error:", err)
    news_li = mc.fetchall()
    paginator = Paginator(news_li, 5)
    page_obj = paginator.get_page(page)
    context = {'news_list': page_obj}

    return render(request, 'news.html', context=context)


def news_detail(request,news_id):
    sql = "select"
    return render(request, 'newsDetail.html')


