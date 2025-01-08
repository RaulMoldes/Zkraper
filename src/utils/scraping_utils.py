from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse

def extract_domain(url):
    # Parse the base URL to extract the domain
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def extract_meta_data(soup: BeautifulSoup):
    meta_data = {}
    for meta_tag in soup.find_all("meta"):
        property_value = meta_tag.get("property") or meta_tag.get("name")
        content_value = meta_tag.get("content", None)
        if property_value and content_value:
            meta_data[property_value] = content_value
    print(f"Total meta tags found: {len(meta_data)}")
    return meta_data


def extract_images(soup: BeautifulSoup, base_url: str):
    images = []
    for img_tag in soup.find_all("img"):
        img_src = img_tag.get("src", None)
        if img_src:
            # Use urljoin to handle relative URLs properly
            full_img_url = urljoin(base_url, img_src)
            images.append({"src" : full_img_url})
        # Handle srcset if present
        elif img_tag.has_attr("srcset"):
            print("Detected srcset attribute in image.")

    print(f"Total images found: {len(images)}")
    return images

def extract_all_links(soup: BeautifulSoup, website_domain: str, base_url: str):
    categorized_links = {"telephone": [], "email": [], "internal": [], "external": []}
    for anchor_tag in soup.find_all("a"):
        href_value = anchor_tag.get("href", None)
        if href_value:
            cleaned_href = href_value.split("#")[0]  # Remove anchor portion
            if cleaned_href.startswith("mailto"):
                categorized_links["email"].append(cleaned_href)
            elif cleaned_href.startswith("tel"):
                categorized_links["telephone"].append(cleaned_href)
            else:
                # Use urljoin to handle relative URLs properly
                full_url = urljoin(base_url, cleaned_href)
                if website_domain in full_url:
                    categorized_links["internal"].append(full_url)
                else:
                    categorized_links["external"].append(full_url)

    # Remove duplicates by converting lists to sets and back to lists
    return {
        "base":base_url,
        "telephone": list(set(categorized_links["telephone"])),
        "email": list(set(categorized_links["email"])),
        "internal": list(set(categorized_links["internal"])),
        "external": list(set(categorized_links["external"])),
    }

def extract_all_text(soup: BeautifulSoup):
    """
    Extract all visible text content from the web page, removing unnecessary whitespace and tags.
    """
    # Get all text in the document
    text = soup.get_text(separator=" ", strip=True)

    # Optionally, clean up extra spaces or unwanted characters
    cleaned_text = " ".join(text.split())  # Removes extra spaces and newlines

    print(f"Total text content length: {len(cleaned_text)} characters")
    return {"text_content" : cleaned_text}

