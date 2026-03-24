import feedparser

def get_news():
    url = "https://feeds.reuters.com/reuters/businessNews"
    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:10]:
        news_list.append({
            "title": entry.title,
            "summary": entry.summary
        })

    return news_list


if __name__ == "__main__":
    news = get_news()
    for n in news:
        print(n["title"])