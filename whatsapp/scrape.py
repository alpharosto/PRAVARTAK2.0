import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def open_whatsapp():
    try:
        driver.get("https://web.whatsapp.com")
        print(f"Opening WhatsApp Web... Current title: {driver.title}")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'app'))
        )
        print("WhatsApp Web is loaded.")
    except Exception as e:
        print(f"Error opening WhatsApp Web: {e}")
        driver.quit()

def scrape_data():
    input("Scan the QR code and press Enter to continue...")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'main'))
    )
    message_window = driver.find_element(By.ID, 'main')
    data = message_window.get_attribute('innerHTML')
    soup = BeautifulSoup(data, 'html.parser')
    messages = soup.find_all('span', {'class': 'selectable-text'})
    
    with open('whatsapp_scrape.html', 'w', encoding='utf-8') as f:
        f.write(data)
    
    print("Data scraped successfully and saved to whatsapp_scrape.html")
    return messages

def create_pdf(messages, pdf_filename='whatsapp_report.pdf'):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawString(100, 750, "WhatsApp Scraped Messages Report")
    c.setFont("Helvetica", 12)
    y = 730
    
    for message in messages:
        text = message.get_text()
        if len(text) > 100:
            text = text[:100] + '...'
        c.drawString(100, y, f"Message: {text}")
        y -= 20
        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            
            y = 750

    c.save()
    print(f"PDF report saved as {pdf_filename}")

if __name__ == '__main__':
    open_whatsapp()
    messages = scrape_data()
    create_pdf(messages)
    driver.quit()
