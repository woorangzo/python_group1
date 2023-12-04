from django.shortcuts import render
import pymysql

def stock_recommendation_view(request):
    # MySQL 연결
    conn = pymysql.connect(
        host='localhost',
        user='woorangzo',
        passwd='1234',
        db='woorangzo'
    )

    # 상위 5개의 등락률이 높은 주식 정보 가져오기
    cursor = conn.cursor()
    top_5_stocks_query = """
        SELECT stock_nm, stock_cd, last_actual_close, predicted_close, change_rate, last_actual_volume, graph_path
        FROM stock_predictions
        ORDER BY change_rate DESC
        LIMIT 5
    """
    cursor.execute(top_5_stocks_query)
    top_5_stocks_data = cursor.fetchall()
    # print(top_5_stocks_data)
    # MySQL 연결 종료
    conn.close()

    # 가져온 정보를 HTML 템플릿에 넘겨줍니다.
    context = {
        'top_5_stocks_data': top_5_stocks_data
    }
    print(top_5_stocks_data)
    return render(request, 'stockRecommend.html', context)
