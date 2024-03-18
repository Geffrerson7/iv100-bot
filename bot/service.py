import logging, requests, logging, time, json, datetime


def get_data():
    """Obtains Pokémon data from multiple sources and returns a combined list of Pokémon with a 100% IV."""
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

    for url in urls:
        headers_for_url = headers.get(url, {})
        try:
            response = requests.get(url, params=params, headers=headers_for_url)
            response.raise_for_status()  # Si ocurre un error, lanzará una excepción
            data = response.json()
            for pokemon in data.get("pokemons", []):
                total_data.append(pokemon)
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            logging.warning(f"Failed to fetch data from {url}: {e}")
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response from {url}: {e}")

    return total_data


def get_name(pokemon_id):
    """Gets the name of a Pokémon based on its ID using the PokeAPI."""
    try:
        pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(pokeapi_url)
        response.raise_for_status()

        data = response.json()
        name = data.get("name")

        return name
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error fetching Pokémon name for ID {pokemon_id}: {e}")
    except ValueError as e:
        logging.error(f"Error decoding JSON response from PokeAPI: {e}")

    return None


def get_dsp(despawn):
    """Obtains the despawn time and calculates the remaining time until then."""
    try:
        if despawn is None:
            return "N/A"
        else:
            end_time_24h = datetime.datetime.fromtimestamp(despawn)
            current_time = datetime.datetime.now()
            remaining_time = end_time_24h - current_time

            seconds = round(remaining_time.total_seconds())
            minutes, seconds = divmod(seconds, 60)

            formatted_dsp = f"{minutes:02}:{seconds:02}"
            return formatted_dsp
    except Exception as e:
        logging.error(f"Error calculating despawn time: {e}")

    return "N/A"  # Return a default value in case of an error


def send_pokemon_data():
    """Retrieves Pokemon data, formats it into messages, and returns a list of formatted messages ready to be sent."""
    try:
        total_message = []
        total_data = get_data()

        if total_data != []:
            batch_size = 33  # Define el tamaño del lote

            for i in range(0, len(total_data), batch_size):
                batch_data = total_data[i : i + batch_size]

                for pokemon_data in batch_data:
                    name = get_name(pokemon_data["pokemon_id"]).title()
                    if name:
                        level = pokemon_data.get("level")
                        cp = pokemon_data.get("cp")
                        dsp = get_dsp(pokemon_data.get("despawn"))
                        latitude = pokemon_data.get("lat")
                        longitude = pokemon_data.get("lng")

                        gender_icon = "♂️" if pokemon_data.get("gender") == 1 else "♀️"
                        shiny_icon = "✨" if pokemon_data.get("shiny") == 0 else ""

                        message = f"🅐 {name} {gender_icon}{shiny_icon} 💯\n🅔L{level} CP {cp}\n🌀☄️Tᴏᴘ💯Gᴀʟᴀxʏ☄️🌀\n⌚ᴅsᴘ {dsp}\n{latitude},{longitude}"
                        total_message.append(message)
        else:
            logging.error("Pokemons not found")
    except Exception as e:
        logging.error(f"Error sending Pokemon data: {e}")
        return None

    return total_message
