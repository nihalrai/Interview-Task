import json
import requests
import traceback
import multiprocessing

from bs4 import BeautifulSoup


def send_request(url):
    try:
        response = requests.get(url, allow_redirects=False, timeout=20)
        if not response.status_code in range(200, 300):
            return None

        return response.text
    except:
        return None


def default_output():
    return '{               \
            "title": "",    \
            "location": "", \
            "description": [], \
            "qualification": [], \
            "posted-by": "" \
            }'


def parse_html(html):
    return BeautifulSoup(html, "html.parser")


def parse_smart(link):
    try:
        output = json.loads(default_output())
        soup = parse_html(send_request(link))

        bsoup = soup.find("h1", {"class": "job-title"})
        output["title"] = bsoup.text

        bsoup = soup.find("div", {"itemprop": "responsibilities"})
        if not bsoup or type(bsoup) == None:
            output["description"] = None
        else:
            bsoup = bsoup.findAll("li")
            bsoup = [str(i.text).strip("<li>").strip("</li>") for i in bsoup]
            output["description"] = bsoup

        bsoup = soup.find("span", {"itemprop": "address", "class": "job-detail"})
        if not bsoup or type(bsoup) == None:
            output["location"] = None
        else:
            output["location"] = bsoup.text

        bsoup = soup.find("h3", {"class": "details-title"})
        if not bsoup or type(bsoup) == None:
            output["posted-by"] = None
        else:
            output["posted-by"] = bsoup.text

        bsoup = soup.find("div", {"itemprop": "qualifications"})
        if not bsoup or type(bsoup) == None:
            output["qualification"] = None
        else:
            bsoup = bsoup.findAll("li")
            bsoup = [str(i.text).strip("<li>").strip("</li>") for i in bsoup]
            output["qualification"] = bsoup

        return output

    except:
        traceback.print_exc()
        return None


def get_links(soup):
    try:
        bsoup = soup.find_all("div", {"class": "tab-pane"})
        data = {}
        for dept in bsoup:
            row       = dept.findAll("div", {"class": "clickable-row"})
            dept_name = dept.find("h4", {"class": "tab-title"})
            data[dept_name.text] = [i.find("a")["href"] for i in row]

        return data
    except:
        return None


def parser(html, pool_size):
    soup = parse_html(html)

    # Get Links of all jobs of each department
    smart_links = get_links(soup)

    if not smart_links:
        return None

    # parse each smartrecruiter link to get data like
    # description, qualification etc.
    result = {}

    for dept, links in smart_links.items():
        result[dept] = []
        with multiprocessing.Pool(pool_size) as p:
            try:
                result[dept] = p.map(parse_smart, links)
            except:
                traceback.print_exc()
        p.terminate()
        p.join()

    return result
