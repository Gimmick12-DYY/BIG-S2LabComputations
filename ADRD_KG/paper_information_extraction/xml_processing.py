from lxml import etree
from xml.etree import ElementTree as ET
import stanza
from unidecode import unidecode

class XMLProcessor:
    def __init__(self):
        self.nlp = stanza.Pipeline(lang='en', processors='tokenize', logging_level="ERROR")

    def find_deepest_p(self, element):
        """
        Helper function, recursively find the deepest <p> tags under the given element.
        """
        # If the element is a <p> and has no child <p>, return it
        if element.tag == "p" and not element.findall(".//p"):
            return [element]
        
        # Otherwise, recurse into children
        deepest_p_tags = []
        for child in element:
            deepest_p_tags.extend(self.find_deepest_p(child))
        return deepest_p_tags 
    
    def extract_paragraph(self, filename):
        """
        Extract abstract from the raw XML file.
        """
        
        tree = ET.parse(filename)
        root = tree.getroot()

        # Find all <abstract> tags
        abstracts = root.findall(".//abstract")

        # Extract all <p> elements from each <abstract> and join them into a single paragraph
        all_text = []
        for abstract in abstracts:
            deepest_p_tags = self.find_deepest_p(abstract)
            paragraphs = [ET.tostring(p, encoding="unicode", method="text").strip() for p in deepest_p_tags]
            all_text.extend(paragraphs)

        # Combine all text into a single paragraph
        complete_paragraph = " ".join(all_text)

        return complete_paragraph

    def extract_sentence(self, abstract):
        """
        Removes all newline characters and leading blanks before sentences,
        and splits the text by periods.

        Args:
            text (str): The input text to process.

        Returns:
            list: A list of sentences, split by periods, with no leading blanks.
        """
        # Remove newline characters
        cleaned_text = abstract.replace("\n", " ")
        doc = self.nlp(cleaned_text)
        sentences = [unidecode(sentence.text) for sentence in doc.sentences] # transform Non ACSII chars
        return sentences, ' '.join(sentences)
