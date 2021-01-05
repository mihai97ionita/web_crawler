from time import sleep

from crawler.concurrency.FutureCollector import FutureCollector
from crawler.factory.chrome_driver_factory import create_web_driver
from crawler.factory.executors_factory import get_thread_executor

prefix = '//*[@id="mainArea"]/router-view/ma-serp/div/div'


def futures_to_results(futures):
    try:
        iter(futures)
        return [f._result for f in futures if f._result]
    except TypeError as te:
        return futures._result


def future_of_functions(driver, function, start, end):
    return [get_thread_executor().submit(function, driver, item) for item in range(start, end)]


def future_of_function(driver, function):
    return get_thread_executor().submit(function, driver)


def find_university(driver):
    xpath = '{}[3]/div/compose/div/ma-card/div/compose/div/div/div[1]/div/ma-call-to-action/a'.format(prefix)
    university = driver.find_element_by_xpath(xpath)
    return university.text


def find_citations(driver):
    xpath = '{}[3]/div/compose/div/ma-card/div/compose/div/div/div[2]/ma-call-to-action[2]/a'.format(prefix)
    citations = driver.find_element_by_xpath(xpath)
    return citations.text


def find_publications(driver):
    xpath = '{}[3]/div/compose/div/ma-card/div/compose/div/div/div[2]/ma-call-to-action[1]/a'.format(prefix)
    publications = driver.find_element_by_xpath(xpath)
    return publications.text


def find_topics(web_driver, index):
    xpathElement = '//*[@id="mainArea"]/router-view/ma-serp/div/div[1]/div/compose/div/div[2]/section[' \
                   '2]/ma-topics-filter/compose/div/div[{}]/ma-data-bar/div/div[2]/div[1]/div'.format(index)
    topTopic = web_driver.find_element_by_xpath(xpathElement)
    return topTopic.text


def find_publications_type(web_driver, i):
    xpath = '{}[1]/div/compose/div/div[2]/section[3]/ma-publication-type-filter/compose/div/div[{' \
            '}]/ma-data-bar/div/div[2]/div[1]/div'.format(prefix, i)
    publicationType = web_driver.find_element_by_xpath(xpath)
    return publicationType.text


def find_journals(web_driver, i):
    xpath = '{}[1]/div/compose/div/div[2]/section[5]/ma-journal-filter/compose/div/div[{}]/ma-data-bar/div/div[' \
            '2]/div[1]/div'.format(prefix, i)
    journal = web_driver.find_element_by_xpath(xpath)
    return journal.text


def find_articles(web_driver, x):
    article_prefix = '//*[@id="mainArea"]/router-view/ma-serp/div/div[2]/div/compose/div/div[2]/ma-card[{' \
                     '}]/div/compose/div/div'.format(x)
    xpath = '{}/a[1]/span'.format(article_prefix)
    title = web_driver.find_element_by_xpath(xpath)

    xpath = '{}/div[3]/ma-author-string-collection/div/div/div'.format(article_prefix)
    numOfContributors = len(web_driver.find_elements_by_xpath(xpath))
    contributors = []
    for y in range(1, numOfContributors + 1):
        xpath = '{}/div[3]/ma-author-string-collection/div/div/div[{}]/a[1]'.format(article_prefix, y)
        contributor = web_driver.find_element_by_xpath(xpath)
        contributors.append(contributor.text.replace(".", ""))

    xpath = '{}/a[2]/span[1]'.format(article_prefix)
    publicationYear = web_driver.find_element_by_xpath(xpath)

    xpath = '{}/a[2]/span[2]'.format(article_prefix)
    publicationName = web_driver.find_element_by_xpath(xpath)

    xpath = '{}/div[3]/ma-tag-mesh-cloud[1]/div/ma-tag-mesh[1]/a/div[2]'.format(article_prefix)
    firstCategory = web_driver.find_element_by_xpath(xpath)
    xpath = '{}/div[3]/ma-tag-mesh-cloud[1]/div/ma-tag-mesh[2]/a/div[2]'.format(article_prefix)
    secondCategory = web_driver.find_element_by_xpath(xpath)
    mainCategories = [firstCategory.text, secondCategory.text]

    xpath = '{}/div[1]/div/a/span'.format(article_prefix)
    numberOfCitations = web_driver.find_element_by_xpath(xpath)

    xpath = '{}/div[3]/ma-expandable-text/div/div/span/span[2]/i'.format(article_prefix)
    fullAbstract = web_driver.find_element_by_xpath(xpath)
    fullAbstract.click()
    sleep(1)
    xpath = '{}/div[3]/ma-expandable-text/div/div/span/span[1]'.format(article_prefix)
    intro = web_driver.find_element_by_xpath(xpath)

    article = dict(title=title.text,
                   contributors=contributors,
                   publicationYear=publicationYear.text,
                   publicationName=publicationName.text,
                   mainCategories=mainCategories,
                   intro=intro.text,
                   numberOfCitations=numberOfCitations.text)
    return article


def parse_page_by_url(url):
    driver = create_web_driver(url)

    futureCollector = FutureCollector()

    futureUniversity = future_of_function(driver, find_university)
    futureCollector.collect(futureUniversity)

    futureCitations = future_of_function(driver, find_citations)
    futureCollector.collect(futureCitations)

    futurePublications = future_of_function(driver, find_publications)
    futureCollector.collect(futurePublications)

    futuresTopTopics = future_of_functions(driver, find_topics, 2, 12)
    futureCollector.collect(futuresTopTopics)

    futuresPublicationTypes = future_of_functions(driver, find_publications_type, 2, 9)
    futureCollector.collect(futuresPublicationTypes)

    topJournalsFutures = future_of_functions(driver, find_journals, 2, 9)
    futureCollector.collect(topJournalsFutures)

    futuresArticles = future_of_functions(driver, find_articles, 1, 11)
    futureCollector.collect(futuresArticles)

    futureCollector.wait_all()

    return dict(university=futures_to_results(futureUniversity),
                number_of_citations=futures_to_results(futureCitations),
                number_of_publications=futures_to_results(futurePublications),
                topics=futures_to_results(futuresTopTopics),
                publication_type=futures_to_results(futuresPublicationTypes),
                journals=futures_to_results(topJournalsFutures),
                articles=futures_to_results(futuresArticles))
