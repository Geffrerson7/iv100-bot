import logging, requests, logging, time, json, datetime, re


def fetch_pokemon_data(iv):
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
        "minIV": str(iv),
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
        except requests.exceptions.RequestException as e:
            logging.warning(f"Failed to fetch data from {url}: {e}")
            return None
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response from {url}: {e}")
            return None 
    total_data.sort(key=lambda x: x["despawn"], reverse=True)
    return total_data


def retrieve_pokemon_name(pokemon_id):
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


def calculate_remaining_time(despawn, delay):
    """Obtains the despawn time and calculates the remaining time until then."""
    try:
        if despawn is None:
            return None
        else:
            end_time_24h = datetime.datetime.fromtimestamp(despawn)
            current_time = datetime.datetime.now()
            remaining_time = end_time_24h - current_time
            seconds = round(remaining_time.total_seconds() - delay)
            minutes, seconds = divmod(seconds, 60)
            if minutes < 0 or seconds < 0:
                return None
            formatted_dsp = f"{minutes}:{seconds:02}"
            return formatted_dsp
    except Exception as e:
        logging.error(f"Error calculating despawn time: {e}")

    return None


def retrieve_move_icon(move_type):
    """Returns an emoji representing the type of a Pokémon move."""
    if move_type == "steel":
        return "⚙️"
    elif move_type == "water":
        return "💧"
    elif move_type == "bug":
        return "🐞"
    elif move_type == "dragon":
        return "🐲"
    elif move_type == "electric":
        return "⚡"
    elif move_type == "ghost":
        return "👻"
    elif move_type == "fire":
        return "🔥"
    elif move_type == "ice":
        return "❄️"
    elif move_type == "fairy":
        return "🌸"
    elif move_type == "fighting":
        return "🥊"
    elif move_type == "normal":
        return "🔘"
    elif move_type == "grass":
        return "🍃"
    elif move_type == "psychic":
        return "🔮"
    elif move_type == "rock":
        return "🪨"
    elif move_type == "dark":
        return "☯️"
    elif move_type == "ground":
        return "⛰️"
    elif move_type == "poison":
        return "☠️"
    elif move_type == "flying":
        return "🪽"
    else:
        return ""


def retrieve_pokemon_move(pokemon_move_id):
    """Gets the move name of a Pokemon based on the move ID using the PokeAPI."""
    try:
        pokeapi_url = f"https://pokeapi.co/api/v2/move/{pokemon_move_id}"
        response = requests.get(pokeapi_url)
        response.raise_for_status()

        data = response.json()
        name = data["names"][5]["name"]
        move_type = data["type"]["name"]
        icon = retrieve_move_icon(move_type)
        return {"name": name, "icon": icon}
    except requests.exceptions.RequestException as e:
        logging.warning(
            f"Error fetching Pokemon move name for ID {pokemon_move_id}: {e}"
        )
    except ValueError as e:
        logging.error(f"Error decoding JSON response from PokeAPI: {e}")

    return None


def coordinates_waiting_time(coordinates_list_size):
    """Obtains the excecution time of fetch_pokemon_data() function"""
    return 1.0969 * coordinates_list_size + 4.0994


def retrieve_pokemon_iv(iv_number):
    """Obtains the iv in telegram message format"""
    if iv_number == 100:
        return "💯"
    elif iv_number == 90:
        return "90"


def escape_string(input_string):
    """Reemplaza los caracteres '-' por '\-', y los caracteres '.' por '\. '"""
    return re.sub(r"[-.]", lambda x: "\\" + x.group(), input_string)


def signature(iv):
    if iv == 100:
        return "*🌀☄️Tᴏᴘ💯Gᴀʟᴀxʏ☄️🌀*\n"
    elif iv == 90:
        return "*🌀☄️Tᴏᴘ `90` Gᴀʟᴀxʏ☄️🌀*\n"
    else:
        return "*🌀☄️Tᴏᴘ Gᴀʟᴀxʏ☄️🌀*\n"


def generate_pokemon_messages(iv):
    """Retrieves Pokemon data, formats it into messages, and returns a list of formatted messages ready to be sent."""
    try:
        total_message = []
        total_data = fetch_pokemon_data(iv)

        if total_data != []:
            message_delay = 3 if len(total_data) > 20 else 2
            for pokemon_data in total_data:
                delay = (
                    1
                    + coordinates_waiting_time(len(total_data))
                    + message_delay * total_data.index(pokemon_data)
                )
                dsp = calculate_remaining_time(pokemon_data.get("despawn"), delay)

                if dsp:
                    level = pokemon_data.get("level")
                    cp = pokemon_data.get("cp")
                    name = escape_string(
                        retrieve_pokemon_name(pokemon_data["pokemon_id"]).title()
                    )
                    latitude = pokemon_data.get("lat")
                    longitude = pokemon_data.get("lng")
                    gender_icon = "♂️" if pokemon_data.get("gender") == 1 else "♀️"
                    shiny_icon = "✨" if pokemon_data.get("shiny") == 0 else ""
                    move1 = escape_string(
                        retrieve_pokemon_move(pokemon_data.get("move1"))["name"]
                    )
                    move2 = escape_string(
                        retrieve_pokemon_move(pokemon_data.get("move2"))["name"]
                    )
                    move1_icon = retrieve_pokemon_move(pokemon_data.get("move1"))[
                        "icon"
                    ]
                    move2_icon = retrieve_pokemon_move(pokemon_data.get("move2"))[
                        "icon"
                    ]
                    iv_number = retrieve_pokemon_iv(iv)
                    message_signature = signature(iv)
                    message = (
                        f"*🄰* *{name}* {shiny_icon}{gender_icon}\n"
                        f"*🄴* IV:{iv_number} ᴄᴘ:{cp} LV:{level}\n"
                        f"{move1_icon}{move1} \| {move2_icon}{move2}\n"
                        f"{message_signature}"
                        f"⌚ᴅsᴘ {dsp}\n"
                        f"`{latitude},{longitude}`"
                    )
                    total_message.append(message)
        else:
            logging.error("Pokemons not found")
    except Exception as e:
        logging.error(f"Error sending Pokemon data: {e}")
        return None
    return total_message