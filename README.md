# HTML Sorting Tool

This Python script sorts `<ul>` lists and their `<li>` elements inside `<div>` tags of the specified HTML file. It sorts the lists based on the chosen country, automatically utilizing appropriate language settings for sorting. The sorted results are saved to a "sorting_output" directory on your desktop.

### Usage

You can run it in the terminal as follows:

```
python html_sorter.py <file_path> <div_class> <country_abbreviation>
```

- `<file_path>`: Path to the HTML file to perform sorting on.
- `<div_class>`: Class name of the `<div>` tags to sort.
- `<country_abbreviation>`: Abbreviation of the country (e.g., "pl" for Poland, "hu" for Hungary, "cz" for Czech Republic).

Sorting results will be saved in a folder named "sorting_output."

### Example Usage

```
python html_sorter.py test.html sorting-div pl
```

This command will sort the specified `div` elements and their nested `ul` elements in the `test.html` file. It will automatically select appropriate language settings for the "pl" country abbreviation, save the sorted output to a "sorting_output" directory on your desktop, and display the result in the terminal.