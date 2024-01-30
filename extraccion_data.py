from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import csv

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

# URL de la primera página
url_base = 'https://www.airbnb.mx/s/Tepoztlán--Morelos--México/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-02-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&query=Tepoztlán%2C%20Mor.&place_id=ChIJdStY3WELzoURIItygPPXAAQ&date_picker_type=calendar&source=structured_search_input_header&search_type=user_map_move&price_filter_num_nights=5&ne_lat=19.08529926076838&ne_lng=-99.05652798634958&sw_lat=18.910118260544586&sw_lng=-99.11269072210865&zoom=13.113956313926673&zoom_level=13&search_by_map=true&federated_search_session_id=372d6562-b855-4bbc-a5be-1caf3beb4c41&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjowLCJ2ZXJzaW9uIjoxfQ%3D%3D'
driver.get(url_base)

# Crear listas para almacenar los datos
titulos = []
descripciones = []
rates = []
prices = []

# Navegación a través de páginas
for pagina in range(1, 15 + 1):  # Ajusta el número total de páginas
    try:
        # Realiza la extracción de datos en la página actual
        titulos_actuales = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
        descripciones_actuales = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-subtitle"]')
        rates_actuales = driver.find_elements(By.XPATH, '//span[@class="r1dxllyb atm_7l_18pqv07 atm_cp_1ts48j8 dir dir-ltr"]')
        prices_actuales = driver.find_elements(By.XPATH, '//span[@class="_14y1gc"]')

        for i in range(len(titulos_actuales)):
            titulos.append(titulos_actuales[i].text)
            if i < len(descripciones_actuales):
                descripciones.append(descripciones_actuales[i].text)
            else:
                descripciones.append("No hay descripción disponible para este título.")
            rates.append(rates_actuales[i].text)
            prices.append(prices_actuales[i].text)

        # Navega a la siguiente página si no estás en la última
        if pagina < 15:
            wait = WebDriverWait(driver, 10)
            enlace_siguiente = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Siguiente"]')))
            enlace_siguiente.click()
            sleep(5)
    except Exception as e:
        print(f"Error en la página {pagina}: {str(e)}")

# Cierra el navegador al finalizar
# Guardar los datos en un archivo CSV
with open('datos_airbnb.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Título', 'Descripción', 'Rate', 'Precio'])

    for i in range(len(titulos)):
        csv_writer.writerow([titulos[i], descripciones[i], rates[i], prices[i]])

# Imprimir la longitud de las listas
print(f"Longitud de titulos: {len(titulos)}")
print(f"Longitud de descripciones: {len(descripciones)}")
print(f"Longitud de rates: {len(rates)}")
print(f"Longitud de prices: {len(prices)}")

# Imprimir la cantidad de filas escritas en el archivo CSV
print(f"Cantidad de filas escritas en el archivo CSV: {len(titulos)}")
