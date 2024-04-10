import json 
# importujemy modul pozwalajacy na wysylanie requestow HTTP
import requests
 
# Rdzen kazdego url, z ktorego pozniej za pomoca f-strings mozemy budowac urle dynamicznie
URL_ROOT = 'https://www.dnd5eapi.co'
 
# Funkcja pozwalajaca na wyslanie requesta HTTP typu GET
# w celu pobrania WSZYSTKICH obiektow obecnych w module
# wymienionym w dokumentacji tego API - https://5e-bits.github.io/docs/api/
# jako argument przekazemy module
def fetch_all_from_module(module):
    """fetch all objects of certain module
 
    Args:
        module (str): name of the module to fetch objects from
    """
    # definiujemy URL na ktory wyslany zostanie request,
    #jest to formatted string, przekazujemy argument z modulem do stringa
    url = f'https://www.dnd5eapi.co/api/{module}'
    # definiujemy odpowiedz, ktora bedzie rowna temu co zwroci wyslanie requestu GET,
    #pod w/w url, timeout to ile sekund ma czekac na odpowiedz zanim rzuci wyjatek
    response = requests.get(url, timeout=10)
    # odpowiedz przychodzi w formacie nie obslugiwanym przez pythona (JSON string),
    # wiec zamieniamy JSON -> Python Dictionary
    response = response.json()
    # wywalamy sobie do terminala calosc zeby podejrzec dane
    # (json.dumps(<odpowiedz jako python-dict>,indent=<int>))
    # gdzie indent to liczba spacji formatujacych dane
    print(json.dumps(response, indent=2))
    # zwroc odpowiedz jesli zostala poprawnie pobrana i istnieje
    if response:
        return response
    # jesli nie zwroc None (cos jak nullptr lub NULL w c++)
    else:
        return None
 
 
def find_class_url_in_response(response, class_name):
    """find particular class in response from fetch_all_from_module()
 
    Args:
        response (dict): response to GET request parsed from JSON to Python Dictionary object
        class_name (str): name of the class you want to find URL suffix for 
    """
    # odnoszę się do struktury 'results' w odpowiedzi
    results = response['results']
    # rzucam fora po każdej zagnieżdżonej w requests strukturze
    for class_info in results:
        # odnoszę się do klucza 'name' w kazdej z zagniezdzonych struktur
        # by sprawdzic czy jest to akurat ta ktorej szukam
        # dodatkowo porownywana nazwe klasy oraz wartosc z odpowiedzi
        # zamieniamy na twardo na male litery, zeby nie bylo nieporozumien
        if class_name.lower() in class_info['name'].lower():
            # jesli znajdziesz nazwe klasy w polu 'name' zwroc pole 'url' z suffixem URL
            return class_info['url']
        else:
            # jesli nie znajdziesz to kontynuuj przegladanie
            continue
    # jesli for sie skonczy i nie zostanie znaleziona klasa, zwroc None
    return None
 
# tutaj w podgladzie odpowiedzi zobacze nastepujace dane:
"""
{
  "count": 12,
  "results": [
    {
      "index": "barbarian",
      "name": "Barbarian",
      "url": "/api/classes/barbarian"
    },
    ....
    ....
    ....
    {
      "index": "wizard",
      "name": "Wizard",
      "url": "/api/classes/wizard"
    }
  ]
}
"""
 
 
def get_class_info(url_suffix):
    # z naszego korzenia URL oraz uzyskanego suffixu klasy budujemy URL do skorzystania z API
    # w tym przypadku
    # URL_ROOT = 'https://www.dnd5eapi.co'
    # url_suffix = '/api/classes/wizard'
    url = f'{URL_ROOT}{url_suffix}'
    # analogicznie wykonujemy zadanie w celu uzyskania odpowiedzi
    response = requests.get(url, timeout=10)
    response = response.json()
    print(json.dumps(response, indent=2))
    # analogiczna walidacja tego co zwracamy - obsluga wyjatku 
    if response:
        return response
    else:
        return None
 
# standardowa funkcja glowna kazdego programu w pythoniew
def main():
    """main function
    """
    # wykorzystujemy wyzej zdefiniowana funkcje do pobrania i wyswietlenia wszystkich klas,
    # jako modul podajemy string - 'classes'
    classes_info = fetch_all_from_module('classes')
    wizard_url_suffix = find_class_url_in_response(classes_info, 'Wizard')
    wizard_class_info = get_class_info(wizard_url_suffix)
    
    
    # teraz pobiore informacje na temat klasy wizard,
    
 
# wykonaj main, tylko jesli ponizszy plik zostanie wywolany bezposrednio
# w terminalu 'python <ten_plik.py>'
if __name__ == '__main__':
    main()