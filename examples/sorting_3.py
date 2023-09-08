import sys
import re

# Manual sort orders for specific locales
manual_sort_orders = {
    "pl": "AĄBCĆDEĘFGHIJKLŁMNOÓPQRSŚTUVWXYZZaąbcćdeęfghijklłmnoópqrsśtuvwxyz",
    "hu": "AÁBCDEÉFGHIÍJKLMNOÓÖŐPQRSTUÚÜŰVWXYZaábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz",
    "cz": "AÁBCČDĎEÉĚFGHIÍJKLMNŇOÓPQRŘSŠTŤUÚŮVWXYÝZŽaábcčdďeéeěfghiíjklmnňoópqrřsštťuúůvwxyýzž"
}

# Sorting key function
def custom_sort_key(locale_code, s):
    if locale_code in manual_sort_orders:
        sort_order = manual_sort_orders[locale_code]
        sorted_characters = []
        for c in s:
            if c in sort_order:
                sorted_characters.append(format(sort_order.index(c), '04x'))
            # Exclude specific characters to prevent errors
            #elif c not in '() ,':
            #    print(f"Ignored character '{c}' for locale '{locale_code}'")
            else:
                sorted_characters.append(format(ord(c), '04x'))
        return ''.join(sorted_characters)
    else:
        return s

# Function to perform sorting
def perform_sorting(file_path, selected_country, section_or_div, class_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if section_or_div == "div":
        # Regular expression pattern for matching <div> elements with the specified class
        used_pattern = r'<div\s+class="[^"]*\b{}\b[^"]*">(?:.*?)<ul>(.*?)<\/ul>'.format(re.escape(class_name))
    elif section_or_div == "section":
        # Regular expression pattern for matching <section> elements with the specified class
        used_pattern = r'<section\s+[^>]*\bclass="[^"]*\b{}\b[^"]*"[^>]*>(?:.*?)<ul>(.*?)<\/ul>'.format(re.escape(class_name))
    else:
        raise ValueError("Invalid value for section_or_div, you can write section or div")

    # Find and process all matching <div> or <section> elements
    for match in re.finditer(used_pattern, content, re.DOTALL):
        div_content = match.group(1)

        regex_pattern = r"^(\s*)(<li>)"

        matches = re.finditer(regex_pattern, div_content, re.MULTILINE)
        spaces_count = 0
        for iter in matches:
            spaces_count = len(iter.group(1))
            break

        tab_before_li = "\t" * (spaces_count - 1)
        tab_before_ul = "\t" * (spaces_count - 2)

        li_elements = re.findall(r'<li>(.*?)<\/li>', div_content)
        #li_elements = re.findall(r'<li[^>]*>([^<]*)<\/li>', div_content)
        

        li_elements.sort(key=lambda x: custom_sort_key(selected_country, x))

        sorted_li_tags = "\n".join([f'{tab_before_li}<li>{element}</li>' for element in li_elements])
        sorted_ul_content = f'\n{sorted_li_tags}\n{tab_before_ul}'

        updated_div_content = div_content.replace(match.group(1), sorted_ul_content)
        content = content.replace(div_content, updated_div_content)

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Sorting complete.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python html_sorter.py <file_path> <country> <section_or_div> <class_name>")
        sys.exit(1)

    file_path = sys.argv[1]
    selected_country = sys.argv[2]
    section_or_div = sys.argv[3]
    class_name = sys.argv[4]

    perform_sorting(file_path, selected_country, section_or_div, class_name)
