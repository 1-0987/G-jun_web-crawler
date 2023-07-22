from flask import Flask
from web_crawler_news import get_google_news
app = Flask(__name__)  # __name__ 代表目前執行的模組


@app.route("/")  # 函式的裝飾:以函式為基礎，提供附加的功能
def hellp_world():
    return "<p>Hello, world!</p>"


@app.route("/test")  # 代表我們要處理的網站路徑
def test():
    return "<p>Hello, gjun </p>"


@app.route("/google_news/<category_name>")  # <保留字> =>可變成參數
def crawl_google_news(category_name):
    news = get_google_news(category_name)
    html_result = ""
    for block_id in news:
        html_result += f"<h1>{block_id}</h1>"
        for block_news in news[block_id]:
            # print(block_news[0])
            html_result += f'<a href="{block_news[1]}">{block_news[0]}</a><br/>'
    return html_result

# cmd: flask --app web_flask run


if __name__ == '__main__':  # 如果以主程式執行
    app.run(debug=True)  # 立刻啟動伺服器
