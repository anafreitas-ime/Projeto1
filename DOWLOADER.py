import os
import requests


class Downloader:

    def __init__(self, server_url_format, destination_folder):
        self.server_url_format = server_url_format
        self.destination_folder = destination_folder
        os.makedirs(self.destination_folder, exist_ok=True)

    def download_file(self, name, progress_callback=None): 
        #mudou para aceitar um callback de progresso, que pode ser usado para atualizar uma barra de progresso na interface do usuário.
        url = self.server_url_format.format(name)
        response = requests.get(url, stream=True)
        file_Path = f'{self.destination_folder}/{name}.tif'

        if response.status_code == 200:
            tamanho_total = int(response.headers.get('content-length', 0))
            baixado = 0

            with open(file_Path, 'wb') as file:
                for pedaco in response.iter_content(chunk_size=8192):
                    file.write(pedaco)
                    baixado += len(pedaco)

                    if progress_callback and tamanho_total > 0:
                        percentual = int(baixado * 100 / tamanho_total)
                        progress_callback(percentual)

            print('File downloaded successfully')
            return file_Path
        else:
            print('Failed to download file')
            return None


def buscar_href_altitude(quadricula):
    """Consulta a API STAC e devolve o link direto (href) do arquivo ZN (Altitude)."""
    url = f"https://data.inpe.br/bdc/stac/v1/collections/topodata-1/items/{quadricula}"
    response = requests.get(url)
    item = response.json()
    return item["assets"]["ZN"]["href"]


if __name__ == "__main__":
    quadricula = "00S465"

    href = buscar_href_altitude(quadricula)
    print("Link encontrado:", href)

    obj_teste = Downloader(href, "C:/Users/anapm/Documents/SE6/PROG/Projeto1")
    obj_teste.download_file(quadricula + "ZN")