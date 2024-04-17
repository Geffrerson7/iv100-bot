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
    moves_dict = {
        1: "Thunder Shock",
        2: "Quick Attack",
        3: "Scratch",
        4: "Ember",
        5: "Vine Whip",
        6: "Tackle",
        7: "Razor Leaf",
        8: "Take Down",
        9: "Water Gun",
        10: "Bite",
        11: "Pound",
        12: "Double Slap",
        13: "Wrap",
        14: "Hyper Beam",
        15: "Lick",
        16: "Dark Pulse",
        17: "Smog",
        18: "Sludge",
        19: "Metal Claw",
        20: "Vice Grip",
        21: "Flame Wheel",
        22: "Megahorn",
        23: "Wing Attack",
        24: "Flamethrower",
        25: "Sucker Punch",
        26: "Dig",
        27: "Low Kick",
        28: "Cross Chop",
        29: "Psycho Cut",
        30: "Psybeam",
        31: "Earthquake",
        32: "Stone Edge",
        33: "Ice Punch",
        34: "Heart Stamp",
        35: "Discharge",
        36: "Flash Cannon",
        37: "Peck",
        38: "Drill Peck",
        39: "Ice Beam",
        40: "Blizzard",
        41: "Air Slash",
        42: "Heat Wave",
        43: "Twineedle",
        44: "Poison Jab",
        45: "Aerial Ace",
        46: "Drill Run",
        47: "Petal Blizzard",
        48: "Mega Drain",
        49: "Bug Buzz",
        50: "Poison Fang",
        51: "Night Slash",
        52: "Slash",
        53: "Bubble Beam",
        54: "Submission",
        55: "Karate Chop",
        56: "Low Sweep",
        57: "Aqua Jet",
        58: "Aqua Tail",
        59: "Seed Bomb",
        60: "Psyshock",
        61: "Rock Throw",
        62: "Ancient Power",
        63: "Rock Tomb",
        64: "Rock Slide",
        65: "Power Gem",
        66: "Shadow Sneak",
        67: "Shadow Punch",
        68: "Shadow Claw",
        69: "Ominous Wind",
        70: "Shadow Ball",
        71: "Bullet Punch",
        72: "Magnet Bomb",
        73: "Steel Wing",
        74: "Iron Head",
        75: "Parabolic Charge",
        76: "Spark",
        77: "Thunder Punch",
        78: "Thunder",
        79: "Thunderbolt",
        80: "Twister",
        81: "Dragon Breath",
        82: "Dragon Pulse",
        83: "Dragon Claw",
        84: "Disarming Voice",
        85: "Draining Kiss",
        86: "Dazzling Gleam",
        87: "Moonblast",
        88: "Play Rough",
        89: "Cross Poison",
        90: "Sludge Bomb",
        91: "Sludge Wave",
        92: "Gunk Shot",
        93: "Mud Shot",
        94: "Bone Club",
        95: "Bulldoze",
        96: "Mud Bomb",
        97: "Fury Cutter",
        98: "Bug Bite",
        99: "Signal Beam",
        100: "X Scissor",
        101: "Flame Charge",
        102: "Flame Burst",
        103: "Fire Blast",
        104: "Brine",
        105: "Water Pulse",
        106: "Scald",
        107: "Hydro Pump",
        108: "Psychic",
        109: "Psystrike",
        110: "Ice Shard",
        111: "Icy Wind",
        112: "Frost Breath",
        113: "Absorb",
        114: "Giga Drain",
        115: "Fire Punch",
        116: "Solar Beam",
        117: "Leaf Blade",
        118: "Power Whip",
        119: "Splash",
        120: "Acid",
        121: "Air Cutter",
        122: "Hurricane",
        123: "Brick Break",
        124: "Cut",
        125: "Swift",
        126: "Horn Attack",
        127: "Stomp",
        128: "Headbutt",
        129: "Hyper Fang",
        130: "Slam",
        131: "Body Slam",
        132: "Rest",
        133: "Struggle",
        134: "Scald",
        135: "Hydro Pump",
        136: "Wrap Green",
        137: "Wrap Pink",
        200: "Fury Cutter",
        201: "Bug Bite",
        202: "Bite",
        203: "Sucker Punch",
        204: "Dragon Breath",
        205: "Thunder Shock",
        206: "Spark",
        207: "Low Kick",
        208: "Karate Chop",
        209: "Ember",
        210: "Wing Attack",
        211: "Peck",
        212: "Lick",
        213: "Shadow Claw",
        214: "Vine Whip",
        215: "Razor Leaf",
        216: "Mud Shot",
        217: "Ice Shard",
        218: "Frost Breath",
        219: "Quick Attack",
        220: "Scratch",
        221: "Tackle",
        222: "Pound",
        223: "Cut",
        224: "Poison Jab",
        225: "Acid",
        226: "Psycho Cut",
        227: "Rock Throw",
        228: "Metal Claw",
        229: "Bullet Punch",
        230: "Water Gun",
        231: "Splash",
        232: "Water Gun",
        233: "Mud Slap",
        234: "Zen Headbutt",
        235: "Confusion",
        236: "Poison Sting",
        237: "Bubble",
        238: "Feint Attack",
        239: "Steel Wing",
        240: "Fire Fang",
        241: "Rock Smash",
        242: "Transform",
        243: "Counter",
        244: "Powder Snow",
        245: "Close Combat",
        246: "Dynamic Punch",
        247: "Focus Blast",
        248: "Aurora Beam",
        249: "Charge Beam",
        250: "Volt Switch",
        251: "Wild Charge",
        252: "Zap Cannon",
        253: "Dragon Tail",
        254: "Avalanche",
        255: "Air Slash",
        256: "Brave Bird",
        257: "Sky Attack",
        258: "Sand Tomb",
        259: "Rock Blast",
        260: "Infestation",
        261: "Struggle Bug",
        262: "Silver Wind",
        263: "Astonish",
        264: "Hex",
        265: "Night Shade",
        266: "Iron Tail",
        267: "Gyro Ball",
        268: "Heavy Slam",
        269: "Fire Spin",
        270: "Overheat",
        271: "Bullet Seed",
        272: "Grass Knot",
        273: "Energy Ball",
        274: "Extrasensory",
        275: "Futuresight",
        276: "Mirror Coat",
        277: "Outrage",
        278: "Snarl",
        279: "Crunch",
        280: "Foul Play",
        281: "Hidden Power",
        282: "Take Down",
        283: "Waterfall",
        284: "Surf",
        285: "Draco Meteor",
        286: "Doom Desire",
        287: "Yawn",
        288: "Psycho Boost",
        289: "Origin Pulse",
        290: "Precipice Blades",
        291: "Present",
        292: "Weather Ball Fire",
        293: "Weather Ball Ice",
        294: "Weather Ball Rock",
        295: "Weather Ball Water",
        296: "Frenzy Plant",
        297: "Smack Down",
        298: "Blast Burn",
        299: "Hydro Cannon",
        300: "Last Resort",
        301: "Meteor Mash",
        302: "Skull Bash",
        303: "Acid Spray",
        304: "Earth Power",
        305: "Crabhammer",
        306: "Lunge",
        307: "Crush Claw",
        308: "Octazooka",
        309: "Mirror Shot",
        310: "Super Power",
        311: "Fell Stinger",
        312: "Leaf Tornado",
        313: "Leech Life",
        314: "Drain Punch",
        315: "Shadow Bone",
        316: "Muddy Water",
        317: "Blaze Kick",
        318: "Razor Shell",
        319: "Power Up Punch",
        320: "Charm",
        321: "Giga Impact",
        322: "Frustration",
        323: "Return",
        324: "Synchronoise",
        325: "Lock On",
        326: "Thunder Fang",
        327: "Ice Fang",
        328: "Horn Drill",
        329: "Fissure",
        330: "Sacred Sword",
        331: "Flying Press",
        332: "Aura Sphere",
        333: "Payback",
        334: "Rock Wrecker",
        335: "Aeroblast",
        336: "Techno Blast Normal",
        337: "Techno Blast Burn",
        338: "Techno Blast Chill",
        339: "Techno Blast Water",
        340: "Techno Blast Shock",
        341: "Fly",
        342: "V Create",
        343: "Leaf Storm",
        344: "Tri Attack",
        345: "Gust",
        346: "Incinerate",
        347: "Dark Void",
        348: "Feather Dance",
        349: "Fiery Dance",
        350: "Fairy Wind",
        351: "Relic Song",
        352: "Weather Ball",
    }

    try:
        move_name = moves_dict.get(pokemon_move_id)
        if move_name:
            move_name = move_name.lower().replace(" ", "-")
            pokeapi_url = f"https://pokeapi.co/api/v2/move/{move_name}"
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
