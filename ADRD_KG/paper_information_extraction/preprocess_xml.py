from bs4 import BeautifulSoup
import os

def clean_pmc_xml(xml_path):
    """
    Extracts and cleans relevant text from a PMC full-text XML file.
    
    Args:
        xml_path (str): Path to the XML file.
    
    Returns:
        str: Cleaned, structured text suitable for LLM input.
    """
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"File not found: {xml_path}")

    with open(xml_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), "lxml-xml")

    # Sections to skip (usually not useful for dataset extraction)
    skip_titles = ["references", "acknowledgements", "funding", "conflict of interest"]

    # Collect text from abstract and sections
    text_parts = []

    # Abstract
    abstract = soup.find("abstract")
    if abstract:
        abstract_text = abstract.get_text(separator=" ", strip=True)
        text_parts.append("=== ABSTRACT ===\n" + abstract_text)

    # Sections
    for sec in soup.find_all("sec"):
        title_tag = sec.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "SECTION"
        if title.lower() in skip_titles:
            continue
        body_text = sec.get_text(separator=" ", strip=True)
        text_parts.append(f"\n=== {title.upper()} ===\n{body_text}")

    return "\n".join(text_parts)

# Test block
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_file', type=str, required=True, help='Path to the .xml file to process')
    parser.add_argument('--output_txt', type=str, default=None, help='Optional path to save the cleaned text')
    args = parser.parse_args()

    cleaned_text = clean_pmc_xml(args.xml_file)

    if args.output_txt:
        with open(args.output_txt, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        print(f"✅ Cleaned text saved to {args.output_txt}")
    else:
        print("✅ Preview of cleaned content:\n")
        print(cleaned_text[:3000])  # Print preview
