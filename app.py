import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Functie om de afbeeldingen op te halen en weer te geven
def get_images_from_url(url):
    driver = None
    try:
        # Selenium WebDriver configureren met headless Chrome-opties
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")  # Voegt een debugging-poort toe
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Laad de pagina en haal de HTML op
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "image")))
        html_doc = driver.page_source
        driver.quit()

        # Parse de HTML en vind alle afbeeldingen
        soup = BeautifulSoup(html_doc, "html.parser")
        img_tags = soup.find_all('img', class_='image')  # Zoek alle <img> tags met class 'image'
        images = []

        # Verzamel de volledige URLs van de afbeeldingen
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                full_img_url = urljoin(url, img_url)
                images.append(full_img_url)

        return images

    except Exception as e:
        st.write(f"Fout bij het ophalen van afbeeldingen: {e}")
    finally:
        if driver is not None:
            driver.quit()

    return []


# ---------------- Page & UI/UX Components ------------------------
def main_sidebar():
    st.header("Afbeelding Downloader met Selenium op Streamlit")
    site_extraction_page()


def site_extraction_page():
    SAMPLE_URL = "https://configurator.volkswagen.nl/id.4/pure/df/exterieur/kleur?code=VWLNO4R"
    url = st.text_input(label="URL", placeholder="https://example.com", value=SAMPLE_URL)

    # Knop om het downloaden te starten
    clicked = st.button("Download afbeeldingen")
    if clicked:
        st.write("Afbeeldingen ophalen, een ogenblik geduld...")
        images = get_images_from_url(url)  # Haal de afbeeldingen op

        # Controleer of er afbeeldingen zijn gevonden en geef deze weer
        if images:
            st.write(f"Gevonden afbeeldingen: {len(images)}")
            for img_url in images:
                st.image(img_url, caption=img_url, use_column_width=True)
        else:
            st.write("Geen afbeeldingen gevonden op de opgegeven URL.")

if __name__ == "__main__":
    main_sidebar()
