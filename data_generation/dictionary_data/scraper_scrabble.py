#import libraries
import requests
from bs4 import BeautifulSoup

class Scraper():

    def __init__(self, url, output_file_name):
        self.url = url
        self.file_name = output_file_name

    def get_soup(self):

        print("Requesting web content...")
        webpage_response = requests.get(self.url)
        webpage_content = webpage_response.content
        self.soup = BeautifulSoup(webpage_content, "html.parser")
        print("Web content recieved.")

    def get_words(self):

        print("Generating word list...")

        word_sections = self.soup.find_all(attrs={'class':'wres_ul'}) #THIS WORKS, type = <class 'bs4.element.Tag'>
        word_sections = [tag.get_text().strip() for tag in word_sections]
        word_list = [word_string.splitlines(keepends = False) for word_string in word_sections]
        word_list = [word for sublist in word_list for word in sublist] #flatten
        self.word_list = [word for word in word_list if word != ""]

        print("Word list generated")

    def save_words_to_file(self):

        print("Saving word list...")
        with open(self.file_name, "w") as file:
            for word in self.word_list:
                file.write("%s\n" % word)
            file.close()

        print("Word list saved.")

    def run(self):
        self.get_soup()
        self.get_words()
        self.save_words_to_file()

if __name__ == "__main__":
    place_names_scraper = Scraper("https://scrabble.merriam.com/acceptable-place-names", "scrabble_acceptable_place_names.txt")
    place_names_scraper.run()

    proper_names_scraper = Scraper("https://scrabble.merriam.com/acceptable-proper-names", "scrabble_proper_names.txt")
    proper_names_scraper.run()

    words_without_vowels_scraper = Scraper("https://scrabble.merriam.com/words-without-vowels", "scrabble_words_without_vowels.txt")
    words_without_vowels_scraper.run()

    monetary_units_scraper = Scraper("https://scrabble.merriam.com/monetary-units", "scrabble_monetary_units.txt")
    monetary_units_scraper.run()

    words_that_surprised_scraper = Scraper("https://scrabble.merriam.com/words-that-surprised-you", "scrabble_words_that_surprised_you.txt")
    words_that_surprised_scraper.run()
