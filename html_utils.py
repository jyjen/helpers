import general_utils as gu
import os

from selenium import webdriver

def write_html(content: str,
               html_fname: str):

    """Generates a HTML file.

    Arguments:
        content {str} -- HTML content to save
        html_fname {str} -- Name of HTML save file

    Returns:
        None
    """

    with open(html_fname, 'w') as f:
        f.write(content)

    print ("HTML file has been saved to '{}'".format(html_fname))

def read_html(html_fname: str):

    """Reads HTML from specified HTML file

    Arguments:
        html_fname {str} -- Name of HTML file

    Returns:
        content {str} -- Contents of the HTML file
    """

    gu.path_checker(path = html_fname,
                    check_type = 'file',
                    to_raise = True)

    # TODO: fix encoding issues when opening files (BOM)
    # TODO: error - 'test/rip_table.html'

    with open(html_fname, 'r') as f:
        content = f.read()

    return content

def display_html(html_fname: str,
                 chrome_driver: str = "reference_files/chromedriver.exe"):

    """Opens a specified HTML file on the default web browser.

    Arguments:
        html_fname {str} -- Path to HTML file to open
        chrome_driver {str} -- Path to ChromeDriver .exe file

    Returns:
        None
    """

    gu.path_checker(path = html_fname,
                    check_type = 'file',
                    to_raise = True)

    full_path = '{}/{}'.format(os.getcwd(), html_fname)
    browser = webdriver.Chrome(executable_path=chrome_driver)
    browser.get(full_path)

def display_in_notebook(html_fname: str):

    """Opens a specified HTML file on the default web browser.

    Arguments:
        html_fname {str} -- Path to HTML file to display"""

    from IPython.core.display import display, HTML

    html_sauce = read_html(html_fname)

    display(HTML(html_sauce))
