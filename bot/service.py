import logging, requests, logging, time, json, datetime


def get_data():
    """ Obtains Pokémon data from multiple sources and returns a combined list of Pokémon with a 100% IV. """
    total_data = []
    urls = [
        "https://vanpokemap.com/query2.php",
        "https://nycpokemap.com/query2.php",
        "https://londonpogomap.com/query2.php",
        "https://sgpokemap.com/query2.php",
        "https://sydneypogomap.com/query2.php",
    ]

    headers = {
        "https://vanpokemap.com/query2.php": {"Referer": "https://vanpokemap.com/"},
        "https://nycpokemap.com/query2.php": {"Referer": "https://nycpokemap.com/"},
        "https://londonpogomap.com/query2.php": {
            "Referer": "https://londonpogomap.com/"
        },
        "https://sgpokemap.com/query2.php": {"Referer": "https://sgpokemap.com/"},
        "https://sydneypogomap.com/query2.php": {
            "Referer": "https://sydneypogomap.com/"
        },
    }

    params = {
        "mons": ",".join(str(i) for i in range(999)),
        "minIV": "100",
        "time": int(time.time()),
        "since": 0,
    }

    try:
        for url in urls:
            headers_for_url = headers.get(
                url, {}
            )  
            response = requests.get(url, params=params, headers=headers_for_url)
            if response.ok:
                data = response.json()
                for pokemon in data["pokemons"]:
                    total_data.append(pokemon)
            else:
                logging.warning(
                    f"Failed to fetch data from {url}. Status code: {response.status_code}"
                )
    except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as e:
        logging.error("Error fetching data: %s", e)
        raise  

    return total_data


def get_name(pokemon_id):
    """ Gets the name of a Pokémon based on its ID using the PokeAPI. """
    try:
        pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        request = requests.get(pokeapi_url)
        if request.ok:
            response = request.json()
            return response["name"]
    except Exception as e:
        logging.error(f"Error getting Pokemon name: {e}")
    return None


def get_dsp(despawn):
    """ Obtains the despawn time and calculates the remaining time until then. """
    if despawn is None:
        return "N/A"
    else:

        end_time_24h = datetime.datetime.fromtimestamp(despawn)

        dsp = end_time_24h - datetime.datetime.now()

        seconds = round(dsp.total_seconds())

        minutes, seconds = divmod(seconds, 60)

        formatted_dsp = f"{minutes:02}:{seconds:02}"

        return formatted_dsp


def send_pokemon_data():
    """ Retrieves Pokemon data, formats it into messages, and returns a list of formatted messages ready to be sent. """
    try:
        total_message = []
        total_data = get_data()

        if total_data != []:

            for pokemon_data in total_data:
                name = get_name(pokemon_data["pokemon_id"]).title()
                if name:
                    level = pokemon_data.get("level")
                    cp = pokemon_data.get("cp")
                    dsp = get_dsp(pokemon_data.get("despawn"))
                    latitude = pokemon_data.get("lat")
                    longitude = pokemon_data.get("lng")

                    if pokemon_data.get("gender") == 1:
                        gender_icon = "♂️"
                    else:
                        gender_icon = "♀️"

                    if pokemon_data.get("shiny") == 0:
                        shiny_icon = "✨"
                    else:
                        shiny_icon = ""

                    message = f"🅐 {name} {gender_icon}{shiny_icon} 💯\n🅔L{level} CP {cp}\n🌀☄️Tᴏᴘ💯Gᴀʟᴀxʏ☄️🌀\n⌚ᴅsᴘ {dsp}\n{latitude},{longitude}"
                    total_message.append(message)
        else:
            logging.error("Pokemons not found")
    except Exception as e:
        logging.error(f"Error sending Pokemon data: {e}")
        return None

    return total_message
