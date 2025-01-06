import json
import os
import re
import requests
import time
from typing import Callable
from dotenv import load_dotenv
from urllib.parse import urlencode, urlparse, urlunparse
from bs4 import BeautifulSoup, Comment
from bs4.element import Tag
from utils.utils import (
    extract_data, save_json_data, string_to_int, zip_csv_files
)


def get_area_name_and_id(url: str) -> tuple[str, str]:
    """
    Returns the area's name and id based on provided url
    Args:
        url: the area's url
    """
    url_parts = url.split('/')
    return url_parts[-1].replace('-', ' ').title(), url_parts[-2]


def get_navbar_anchor_tags(
    url: str, *, soup: BeautifulSoup = None, include_num_routes: bool = False
) -> list[Tag] | list[tuple[Tag, int]]:
    """
    Returns a list of tags in the URL's navbar
    Args:
        url: the area's url
        html: the parsed html if site has already been requested
    """
    load_dotenv()
    navbar_link_class = os.getenv('NAVBAR_LINK_CLASS')
    val_id = os.getenv('VAL_ID')

    if not soup:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    navbar_links = soup.find_all(class_=navbar_link_class)

    tags = []
    for navbar_link in navbar_links:
        link = navbar_link.find('a')
        val = navbar_link.select_one(f'{val_id}')
        if link and val and string_to_int(val.get_text()) > 50:
            tags.append((link, string_to_int(val.get_text())))

    if include_num_routes:
        return tags
    return [
        anchor for anchor, val in sorted([t for t in tags], key=lambda t: t[1])
    ]


def get_main_area_urls() -> list[tuple[Tag, int]]:
    """Returns the main areas per the source URL's homepage"""
    load_dotenv()
    url = os.getenv('URL')
    table_id = os.getenv('TABLE_ID')
    num_routes = os.getenv('NUMBER_OF_ROUTES')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_regions = []
    for num in soup.find(id=table_id).select(num_routes):
        region = num.find_next_sibling()
        main_regions.append((region, string_to_int(num.get_text())))
    return main_regions


def create_country_map(states: list[Tag]) -> None:
    """
    Returns a dictionary populated with usa states and their ID and total
    number of routes

    Args:
        states: list of tags to the state's info page
    """
    regions = {}
    for link, num_routes in states:
        area_name, area_id = get_area_name_and_id(link.get("href"))
        if area_name == 'International' or area_name == 'In Progress':
            continue
        regions[area_name] = {'id': area_id, 'routes': num_routes}
    return regions


def add_international_countries(url: str, countries: dict[str, int]) -> None:
    """
    Adds countries with over 50 routes and their corresponding ID's to
    the given dictionary.
    Args:
        url: URL that contains continents in the navbar
        countries: dictionary that maps countries and their ID's
    """
    continents = get_navbar_anchor_tags(url)
    for continent in continents:
        country_tags = get_navbar_anchor_tags(
            continent.get('href'), include_num_routes=True
        )
        for country_tag, routes in country_tags:
            area_name, area_id = get_area_name_and_id(country_tag.get('href'))
            countries[area_name] = {'id': area_id, 'routes': routes}


def save_area_ids() -> None:
    """
    Saves a dictionary with regions and their ID's
    """
    area_urls = get_main_area_urls()
    area_urls.pop()
    regions = create_country_map(area_urls[:-1])

    international_url = area_urls[-1][0].get('href')
    add_international_countries(international_url, regions)
    fp = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'data', 'area_map.json'
    )
    save_json_data(fp, regions)


def generate_area_url(area_id: str, area_name: str) -> str:
    """Generates the area's url based on the id and name"""
    load_dotenv()
    base_url = os.getenv('AREA_URL')
    return '/'.join([base_url, area_id, area_name.lower().replace(' ', '-')])


def get_route_distribution(html: BeautifulSoup) -> dict[str, int] | None:
    """
    Returns the route grade distribution
    Args:
        html: parsed html of area's page
    """

    load_dotenv()
    container_id = os.getenv('AREA_STATS_CONTAINER')
    element_type = os.getenv('AREA_STATS_ELEMENT')
    regex_pattern = os.getenv('AREA_STATS_REGEX')

    container = html.find(id=container_id)
    elements = container.find_all(element_type)

    for element in elements:
        data = re.search(regex_pattern, element.get_text())
        if data:
            return clean_data(json.loads(data.group(1)))


def clean_data(data: dict[str, list[str | int]]) -> dict[str, int]:
    """Cleans the input data"""
    rows = data['rock']
    clean_data = {}
    for row in rows:
        grade = row[0]
        if grade == '<5.6':
            grade = '5.6'
        elif grade == '>=5.13':
            grade = '5.13'
        clean_data[grade] = int(row[1])
    return clean_data


def is_manageable(data: dict[str, int]) -> bool:
    """
    Returns true if area is small enough to be downloaded.
    Args:
        data: dictionary with grades and their counts
    """
    grades = ['5.6', '5.7', '5.8', '5.9']
    return all([(data[grade] <= 1000) for grade in grades])


def url_generator(params: dict[str, str]) -> tuple[str, str]:
    """
    Returns two URLS's to extract routes and their number of reviews
    Args:
        params: dictionary with the query parameters
    """
    load_dotenv()
    route_url = urlparse(os.getenv('ROUTE_DATA_URL'))
    reviews_url = urlparse(os.getenv('ROUTE_REVIEWS_URL'))
    query_string = urlencode(params)
    return (
        urlunparse(route_url._replace(query=query_string)),
        urlunparse(reviews_url._replace(query=query_string))
    )


def get_reviews(url: str) -> None:
    """
    Saves the reviews by route
    Args:
        url: url of page with review data
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    load_dotenv()
    data = soup.find(
        os.getenv('REVIEW_ELEMENT'), class_=os.getenv('REVIEW_ELEMENT_CLASS')
    )
    if data is None:
        return

    key_word = os.getenv('REVIEW_KEYWORD')
    fp = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'parser', 'reviews.json'
    )
    reviews = extract_data(fp)

    comments = data.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if key_word in comment:
            reviews[comment.split("\\")[-1].split("-")[-1]] = (
                string_to_int(comment.find_next_sibling("span").get_text())
            )

    save_json_data(fp, reviews)
    return


def get_routes(url: str) -> None:
    """
    Saves the routes
    Args:
        url: url of page with route data
    """
    parent_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'parser', 'input_data'
    )
    file_name = f'input_file_{len(os.listdir(parent_dir))}.csv'
    fp = os.path.join(parent_dir, file_name)

    response = requests.get(url)
    response.raise_for_status()
    with open(fp, "wb") as file:
        file.write(response.content)
    return


def scrape_data(area_id: str, param_1_val: str, param_2_val: str) -> None:
    """TODO"""

    load_dotenv()
    variable_params = {
        os.getenv('ID_PARAM'): area_id,
        os.getenv('GRADE_PARAM_1'): param_1_val,
        os.getenv('GRADE_PARAM_2'): param_2_val,
    }
    constant_parameters = extract_data(
        os.path.join(os.path.dirname(__file__), 'constant_parameters.json')
    )
    params = constant_parameters | variable_params
    routes_url, reviews_url = url_generator(params)
    time.sleep(1)
    get_reviews(reviews_url)
    time.sleep(1)
    get_routes(routes_url)
    return


def download_area_helper(
    area_id: str, area_name: str, grade_distribution: dict[str, int],
    *, cache: list[int], callback: Callable[[int], None] = None
) -> None:
    """TODO"""
    grade_parameters = extract_data(
        os.path.join(os.path.dirname(__file__), 'grade_parameters.json')
    )
    num_routes, param_1_val, param_2_val = None, None, None
    grades = ['5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13']

    def reset_params() -> None:
        """
        Resets the number of routes, parameter 1 and parameter 2 and pops
        the first grade if the number of routes is less than 1000
        """
        nonlocal num_routes, param_1_val, param_2_val

        if len(cache) == 1:
            cache.append(0)
        else:
            cache[1] += num_routes
        if callback:
            callback(int(100 * cache[1] // cache[0]))

        num_routes = grade_distribution[grades[0]]
        param_1_val = grade_parameters[grades[0]][0]
        param_2_val = grade_parameters[grades[0]][1]
        if num_routes < 1000:
            grades.pop(0)
        return

    reset_params()
    while len(grades):
        if num_routes + grade_distribution[grades[0]] < 1000:
            num_routes += grade_distribution[grades[0]]
            param_2_val = grade_parameters[grades[0]][1]
            grades.pop(0)
        elif num_routes > 1000:
            for p_1, p_2 in grade_parameters[f'{grades[0]}-split']:
                scrape_data(area_id, p_1, p_2)
            grades.pop(0)
            reset_params()
        else:
            scrape_data(area_id, param_1_val, param_2_val)
            reset_params()
    scrape_data(area_id, param_1_val, param_2_val)
    return


def download_area(
    area_id: str, area_name: str, *, cache: list[int] = None,
    callback: Callable[[int], None] = None

) -> None:
    area_url = generate_area_url(area_id, area_name)
    response = requests.get(area_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    area_grade_distribution = get_route_distribution(soup)

    if cache is None:
        cache = [0]
        for grade in area_grade_distribution:
            cache[0] += area_grade_distribution[grade]

    if is_manageable(area_grade_distribution):
        download_area_helper(
            area_id, area_name, area_grade_distribution,
            cache=cache, callback=callback
        )

    else:
        sub_areas = get_navbar_anchor_tags(area_url, soup=soup)
        for sub_area in sub_areas:
            area_name, area_id = get_area_name_and_id(sub_area.get('href'))
            download_area(area_id, area_name, cache=cache, callback=callback)
        return


def download_and_merge_data(
    area_id: str, area_name: str,
    callback: Callable[[int], None] = None
) -> None:
    """
    Downloads the area's information & zips all of the resulting .csv files
    Args:
        area_id: the area's id
        area_name: the name of the area
    """
    download_area(area_id, area_name, callback=callback)
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    file_name = f"{area_name.replace(' ', '_').lower()}.csv"
    src = os.path.join(parent_dir, 'parser', 'input_data')
    dest = os.path.join(parent_dir, 'parser', 'crags_by_area', file_name)
    delete_input_files = True
    zip_csv_files(src, dest, delete_input_files)
    return
