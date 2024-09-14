import logging, requests, time, json, datetime, re, traceback


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
                pokemon["flag"] = retrieve_flag(url)
                total_data.append(pokemon)
        except requests.exceptions.RequestException as e:
            logging.warning(f"Failed to fetch data from {url}: {e}")
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response from {url}: {e}")
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
    if move_type == "Acero":
        return "⚙️"
    elif move_type == "Agua":
        return "💧"
    elif move_type == "Bicho":
        return "🐞"
    elif move_type == "Dragón":
        return "🐲"
    elif move_type == "Eléctrico":
        return "⚡"
    elif move_type == "Fantasma":
        return "👻"
    elif move_type == "Fuego":
        return "🔥"
    elif move_type == "Hielo":
        return "❄️"
    elif move_type == "Hada":
        return "🌸"
    elif move_type == "Lucha":
        return "🥊"
    elif move_type == "Normal":
        return "🔘"
    elif move_type == "Planta":
        return "🌿"
    elif move_type == "Psíquico":
        return "🔮"
    elif move_type == "Roca":
        return "🪨"
    elif move_type == "Siniestro":
        return "☯️"
    elif move_type == "Tierra":
        return "⛰️"
    elif move_type == "Veneno":
        return "☠️"
    elif move_type == "Volador":
        return "🪽"
    else:
        return ""


def retrieve_pokemon_move(pokemon_move_id, pokemon_name):
    """Gets the move name of a Pokemon based on the move ID using the PokeAPI."""

    with open("data/moves.json", "r") as file:
        moves_data = json.load(file)
    move = moves_data.get(str(pokemon_move_id))
    if move:
        move_name = move.get("name")
        move_type = move.get("type")
        icon = retrieve_move_icon(move_type)
        return {"name": move_name, "icon": icon}
    else:
        print(f"Pokemon:{pokemon_name}, move_id:{pokemon_move_id}")
        return {"name": "", "icon": ""}


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
    """Replaces characters '-' with '\-', and characters '.' with '\.'"""
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
            message_delay = 3 if len(total_data) > 18 else 2
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
                        retrieve_pokemon_move(pokemon_data.get("move1"), name)["name"]
                    )
                    move2 = escape_string(
                        retrieve_pokemon_move(pokemon_data.get("move2"), name)["name"]
                    )
                    move1_icon = retrieve_pokemon_move(pokemon_data.get("move1"), name)[
                        "icon"
                    ]
                    move2_icon = retrieve_pokemon_move(pokemon_data.get("move2"), name)[
                        "icon"
                    ]
                    iv_number = retrieve_pokemon_iv(iv)
                    message_signature = signature(iv)
                    flag = pokemon_data["flag"]
                    if pokemon_is_alolan(name, move1):
                        name += " de Alola"

                    if pokemon_is_galarian(name, move1, move2):
                        name += " de Galar"
                    message = (
                        f"*🄰* *{name}* {shiny_icon}{gender_icon}\n"
                        f"*🄴* IV:{iv_number} ᴄᴘ:{cp} LV:{level}\n"
                        f"{move1_icon}{move1} \| {move2_icon}{move2}\n"
                        f"{message_signature}"
                        f"⌚ᴅsᴘ {dsp}\n"
                        f"{flag}\n"
                        f"`{latitude},{longitude}`"
                    )
                    total_message.append(message)
        else:
            logging.error("Pokemons not found")
    except Exception as e:
        logging.error(f"Error sending Pokemon data: {e}")
        logging.error(traceback.format_exc())
        return None
    return total_message


def pokemon_is_galarian(
    pokemon_name: str, pokemon_move_1: str, pokemon_move_2: str
) -> bool:

    if pokemon_name == "Stunfisk" and pokemon_move_1 == "Garra Metal":
        return True
    if pokemon_name == "Meowth" and pokemon_move_1 == "Garra Metal":
        return True
    if pokemon_name == "Ponyta" and (
        pokemon_move_1 == "Patada Baja" or pokemon_move_1 == "Psicocorte"
    ):
        return True
    if pokemon_name == "Rapidash" and (
        pokemon_move_1 == "Psicocorte" or pokemon_move_1 == "Viento Feérico"
    ):
        return True
    if pokemon_name == "Slowpoke" and pokemon_move_1 == "Cola Férrea":
        return True
    if pokemon_name == "Slowbro" and pokemon_move_1 == "Puya Nociva":
        return True
    if pokemon_name == "Farfetch'd" and pokemon_move_1 == "Golpe Roca":
        return True
    if pokemon_name == "Weezing" and pokemon_move_1 == "Viento Feérico":
        return True
    if pokemon_name == "Mr-Mime" and (
        pokemon_move_2 == "Puño Hielo" or pokemon_move_2 == "Triple Axel"
    ):
        return True
    if pokemon_name == "Slowking" and (
        pokemon_move_1 == "Ácido" or pokemon_move_1 == "Infortunio"
    ):
        return True
    if pokemon_name == "Zigzagoon" and pokemon_move_1 == "Derribo":
        return True
    if pokemon_name == "Linoone" and (
        pokemon_move_1 == "Lengüetazo" or pokemon_move_1 == "Alarido"
    ):
        return True
    if pokemon_name == "Darumaka" and pokemon_move_1 == "Colmillo Hielo":
        return True
    if pokemon_name == "Darmitan" and pokemon_move_1 == "Colmillo Hielo":
        return True
    if pokemon_name == "Yamask" and (
        pokemon_move_2 == "Tumba Rocas" or pokemon_move_2 == "Tinieblas"
    ):
        return True

    return False


def pokemon_is_alolan(pokemon_name: str, pokemon_move_1: str) -> bool:

    if pokemon_name == "Rattata" and (
        pokemon_move_1 == "Ataque Rápido" or pokemon_move_1 == "Placaje"
    ):
        return True
    if pokemon_name == "Raticate" and (
        pokemon_move_1 == "Mordisco" or pokemon_move_1 == "Ataque Rápido"
    ):
        return True
    if pokemon_name == "Raichu" and (
        pokemon_move_1 == "Impactrueno"
        or pokemon_move_1 == "Chispa"
        or pokemon_move_1 == "Voltiocambio"
    ):
        return True
    if pokemon_name == "Sandshrew" and (
        pokemon_move_1 == "Garra Metal" or pokemon_move_1 == "Nieve Polvo"
    ):
        return True
    if pokemon_name == "Sandslash" and (
        pokemon_move_1 == "Garra Metal"
        or pokemon_move_1 == "Nieve Polvo"
        or pokemon_move_1 == "Garra Umbría"
    ):
        return True
    if pokemon_name == "Vulpix" and (
        pokemon_move_1 == "Cabezazo Zen" or pokemon_move_1 == "Nieve Polvo"
    ):
        return True
    if pokemon_name == "Ninetales" and (
        pokemon_move_1 == "Finta"
        or pokemon_move_1 == "Nieve Polvo"
        or pokemon_move_1 == "Encanto"
    ):
        return True
    if pokemon_name == "Diglett" and (
        pokemon_move_1 == "Garra Metal"
        or pokemon_move_1 == "Bofetón Lodo"
        or pokemon_move_1 == "Ataque Arena"
    ):
        return True
    if pokemon_name == "Dugtrio" and (
        pokemon_move_1 == "Garra Metal"
        or pokemon_move_1 == "Bofetón Lodo"
        or pokemon_move_1 == "Ataque Arena"
    ):
        return True
    if pokemon_name == "Meowth" and (
        pokemon_move_1 == "Mordisco" or pokemon_move_1 == "Arañazo"
    ):
        return True
    if pokemon_name == "Persian" and (
        pokemon_move_1 == "Arañazo" or pokemon_move_1 == "Finta"
    ):
        return True
    if pokemon_name == "Geodude" and (
        pokemon_move_1 == "Lanzarrocas" or pokemon_move_1 == "Voltiocambio"
    ):
        return True
    if pokemon_name == "Graveler" and (
        pokemon_move_1 == "Disparo Lodo"
        or pokemon_move_1 == "Lanzarrocas"
        or pokemon_move_1 == "Bofetón Lodo"
    ):
        return True
    if pokemon_name == "Golem" and (
        pokemon_move_1 == "Disparo Lodo"
        or pokemon_move_1 == "Lanzarrocas"
        or pokemon_move_1 == "Bofetón Lodo"
    ):
        return True
    if pokemon_name == "Grimer" and pokemon_move_1 == "Mordisco":
        return True
    if pokemon_name == "Muk" and (
        pokemon_move_1 == "Mordisco"
        or pokemon_move_1 == "Puya Nociva"
        or pokemon_move_1 == "Alarido"
    ):
        return True
    if pokemon_name == "Exeggutor" and (
        pokemon_move_1 == "Cola Dragón" or pokemon_move_1 == "Semilladora"
    ):
        return True
    if pokemon_name == "Marowak" and (
        pokemon_move_1 == "Golpe Roca"
        or pokemon_move_1 == "Infortunio"
        or pokemon_move_1 == "Giro Fuego"
    ):
        return True
    return False

def retrieve_flag(url: str):
    if url == "https://vanpokemap.com/query2.php":
        return "🇨🇦Vancouver, Canadá"
    elif url == "https://nycpokemap.com/query2.php":
        return "🇺🇸Nueva York, Estados Unidos"
    elif url == "https://londonpogomap.com/query2.php":
        return "🇬🇧Londres, Reino Unido"
    elif url == "https://sgpokemap.com/query2.php":
        return "🇸🇬Singapur, Singapur"
    elif url == "https://sydneypogomap.com/query2.php":
        return "🇦🇺Sydney, Australia"