from bs4 import BeautifulSoup
import requests  # 一種module
import pprint


def get_category_main_page_link(category_name):

    # 想爬的網頁
    r = requests.get(
        "https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant")
    # 取得回傳的DOM文字資料
    doc = r.text
    # 把doc(DOM tree)送給beautifulsoup class, 做物件assign給soup這個變數
    soup = BeautifulSoup(doc, 'html.parser')
    # print(soup.prettify())
    # print(soup.title)
    # print(soup.title.text)

    # 拿到國際新聞的頁面連結，並取得內容
    # 4-1.拿到所有element tag為"a"的DOM tree element, 並檢查是否有"href"和"aria-label"屬性
    elements_a = [element for element in soup.find_all('a') if element.get(
        "href") and element.get("aria-label")]  # aria-label 有文字對應
    # 4-2. 取出aria-label是"國際"的DOM tree
    category_news_href = ""
    for element in elements_a:
        if element.get("aria-label") == category_name:
            category_news_href = \
                'https://news.google.com' + element.get("href")[1:]
            break
    return category_news_href


def get_category_news_blocks(category_main_page_link):
    # 4-3.去request"國際"這個頁面
    # print(international_news_href)
    page_next = requests.get(category_main_page_link).text
    soup = BeautifulSoup(page_next, 'html.parser')

    # 5.分塊拿到國際新聞 :element tag=c-wiz(一個block包含各家媒體對一則新聞的報導), class=PO9Zff Ccj79 kUVvS
    blocks_elements = soup.find_all(
        'c-wiz', {'class': 'PO9Zff Ccj79 kUVvS'})
    return blocks_elements


def get_google_news(category_name):
    news_href = get_category_main_page_link("國際")

    news_blocks = get_category_news_blocks(news_href)\

    # 6.找到每個block內，所有的新聞標題與超連結
    blocks_news = dict()
    for block_index, block in enumerate(news_blocks):  # enumerate產生序數
        # 6-1.找標題
        titles = list()
        for title_element in block.find_all('h4', {'class': 'gPFEn'}):
            titles.append(title_element.string)

        # pprint.pprint(titles)

        # 6-2.找連結
        links = list()
        for link_element in block.find_all('a', {'class': 'WwrzSb'}):
            links.append('https://news.google.com' +
                         link_element.get("href")[1:])

        # 6-3.找媒體
        media = list()
        for media_element in block.find_all('div', {'class': 'vr1PYe'}):
            media.append(media_element.text)

        # 6-4.找時間
        time_stamp = list()
        for time_element in block.find_all("time", {'class': "hvbAAd"}):
            time_stamp.append(time_element.get('datetime'))

        result = list(zip(titles, links, media, time_stamp))

        if result:  # 若block內有東西
            blocks_news[block_index] = result

    return blocks_news


if __name__ == '__main__':

    news = get_google_news(category_name="國際")
    pprint.pprint(news[0])  # 也可改成其他序數，但是可能沒有這個key

    # pprint.pprint(block_news)
