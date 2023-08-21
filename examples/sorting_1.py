import tkinter as tk
import locale

# Function to create a sorting key for different countries
def sorting_key(locale_code):
    def sort_key(s):
        # Set locale settings based on the specified country code
        locale.setlocale(locale.LC_COLLATE, locale_code)
        # Convert the sorting key taking Unicode characters into account
        return locale.strxfrm(s)
    return sort_key

# Perform sorting process
def perform_alphabetical_sorting():
    # Retrieve data from the text box and split it into lines
    data = data_input.get("1.0", "end-1c").split("\n")
    # Get the name of the selected country
    selected_country = country_var.get()
    # Perform specialized sorting for the selected country
    if selected_country in country_locales:
        # Sort data using the sorting key corresponding to the language of the selected country
        sorted_data = sorted(data, key=sorting_key(country_locales[selected_country]))
        # Add sorted data to the result text box
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        for item in sorted_data:
            item = item.strip()
            if item:
                if not item.startswith("<li>"):
                    # Add <li> tags if they're not present at the beginning
                    item = f"<li>{item}</li>"
                # Add results to the text box
                result_text.insert(tk.END, f"{item}\n")
        result_text.config(state=tk.DISABLED)

# Function to copy results to clipboard
def copy_to_clipboard():
    # Retrieve data from the result text box
    result_data = result_text.get("1.0", tk.END).strip()
    # Copy data to the clipboard
    root.clipboard_clear()
    root.clipboard_append(result_data)

# Define country and locale data
country_locales = {
    "Poland": "pl_PL.UTF-8",
    "Hungary": "hu_HU.UTF-8",
    "Czech Republic": "cs_CZ.UTF-8",
    # You can add new countries here
    # "Germany": "de_DE.UTF-8",
    # "France": "fr_FR.UTF-8",
    # "Spain": "es_ES.UTF-8",
}

# Create the GUI
root = tk.Tk()
root.title("Alphabetical Sorting")

# Create label and text box for data input
data_label = tk.Label(root, text="Enter data (Separate each entry with Enter):")
data_label.pack()

data_input = tk.Text(root, height=4, width=50)
data_input.pack()

# Create sorting and copying buttons
button_frame = tk.Frame(root)
button_frame.pack()

sort_button = tk.Button(button_frame, text="Sort", command=perform_alphabetical_sorting)
sort_button.pack(side=tk.LEFT)

copy_button = tk.Button(button_frame, text="Copy", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=10)

# Create an option menu
country_var = tk.StringVar()
country_var.set("Poland")  # Default to selecting Poland

# Let's add country options for the dropdown menu
country_menu = tk.OptionMenu(root, country_var, *country_locales.keys())
country_menu.pack()

# Create label and text box to display sorted data
result_label = tk.Label(root, text="Sorted Data:")
result_label.pack()

result_text = tk.Text(root, height=15, width=50, state=tk.DISABLED)
result_text.pack()

# Run the GUI
root.mainloop()
