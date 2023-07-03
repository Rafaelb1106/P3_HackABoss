from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as playwright:
        #browser = playwright.chromium.launch(headless=True)
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        # Navegar a la página de Google
        page.goto("https://www.google.com")

        # Esperar a que se cargue la página
        page.wait_for_load_state("networkidle")

        # Buscar una palabra en Google
        search_query = "automatización de tareas"
        search_input = page.wait_for_selector('input[name="q"]')
        search_input.fill(search_query)
        search_input.press("Enter")

        # Esperar a que se carguen los resultados de búsqueda
        page.wait_for_load_state("networkidle")

        # Capturar los títulos de los resultados de búsqueda
        result_titles = page.query_selector_all('div[id="search"] h3')
        titles = [title.inner_text() for title in result_titles]

        # Imprimir los títulos de los resultados
        print("Resultados de búsqueda:")
        for title in titles:
            print("- " + title)

        browser.close()

if __name__ == '__main__':
    main()
