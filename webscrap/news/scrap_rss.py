import json

import feedparser


def main() -> None:
    good = 0
    tags = dict()
    total_tags = 2179
    url_template = "https://www.tec.ac.cr/hoyeneltec/taxonomy/term/{index}/feed"

    for i in range(1, total_tags):
        url = url_template.format(index=i)
        feed = feedparser.parse(url)
        if feed.status == 200:
            tags[i] = {
                'name': feed.feed.title.split(' - ')[1],
                'description': feed.feed.description,
                'link': feed.feed.link,
                'category': True if feed.feed.description != '' else False,
                'news': [
                    {
                        'title': article.title,
                        'pub_date': article.published,
                        'guid': article.id.split(' at ')[0],
                        'link': article.link,
                        'authors': [
                            {
                                'name': author.name
                            } for author in article.authors
                        ]
                    } for article in feed.entries
                ]

            }
            good += 1
        print(f'Tags scrapped: {good}', end='\r')
    print()
    json.dump(tags, open('scrapped_news.json', 'w'), indent=4)


if __name__ == '__main__':
    main()
