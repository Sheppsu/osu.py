from osu import Client


client = Client()
news = client.get_news_listing()
news_post = news["news_posts"][0]
news_post = client.get_news_post(news_post.id, key="id")  # just to demonstrate the function
print(news_post.id, news_post.slug, news_post.author, news_post.title)
