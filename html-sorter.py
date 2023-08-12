import sys
from bs4 import BeautifulSoup
import locale
import os

def sorting_key(locale_code):
    def sort_key(s):
        locale.setlocale(locale.LC_COLLATE, locale_code)
        return locale.strxfrm(s)
    return sort_key

def get_locale_code(country):
    country_locales = {
        "pl": "pl_PL.UTF-8",
        "hu": "hu_HU.UTF-8",
        "cz": "cs_CZ.UTF-8",
        # You can add new countries here
        # "de": "de_DE.UTF-8",
        # "fr": "fr_FR.UTF-8",
        # "es": "es_ES.UTF-8",
    }
    return country_locales.get(country, "C.UTF-8")  # Default to C.UTF-8

def perform_sorting(file_path, div_class, selected_country):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    div_tags = soup.find_all("div", class_=div_class)

    locale_code = get_locale_code(selected_country)

    for div_tag in div_tags:
        ul_tags = div_tag.find_all("ul")
        for ul_tag in ul_tags:
            li_tags = ul_tag.find_all("li")
            sorted_li_tags = sorted(li_tags, key=lambda tag: sorting_key(locale_code)(tag.text))
            for li_tag in li_tags:
                li_tag.extract()
            for sorted_li_tag in sorted_li_tags:
                ul_tag.append(sorted_li_tag)

    result_data = str(soup.prettify())
    
    # Create a "sorting_output" folder on the desktop
    desktop_path = os.path.expanduser("~/Desktop")
    output_folder = os.path.join(desktop_path, "sorting_output")
    os.makedirs(output_folder, exist_ok=True)

    # Create a new file name and path
    output_filename = "sorted_output.html"
    output_path = os.path.join(output_folder, output_filename)

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(result_data)
        print("Sorting complete. Result saved to", output_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python html_sorter.py <file_path> <div_class> <country>")
        sys.exit(1)

    file_path = sys.argv[1]
    div_class = sys.argv[2]
    selected_country = sys.argv[3]

    perform_sorting(file_path, div_class, selected_country)
