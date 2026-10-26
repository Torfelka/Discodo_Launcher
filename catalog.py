import json, urllib.request
from dataclasses import dataclass
from pathlib import Path
STEAM_APP_LIST_URL="https://api.steampowered.com/ISteamApps/GetAppList/v2/"
STEAMSPY_TOP_URL="https://steamspy.com/api.php?request=top1000games"
MIN_CATALOG_SIZE=50000
FEATURED_LIMIT=500
@dataclass(slots=True)
class Game:
 app_id:str
 name:str
 popular:bool=False
 genre:str="PC game"
 description:str=""
POPULAR_GAMES={
"730":{"name":"Counter-Strike 2","genre":"Tactical Shooter","description":"Competitive tactical shooter built around precise gunplay and teamwork."},
"570":{"name":"Dota 2","genre":"MOBA","description":"A competitive strategy game with a huge roster of heroes."},
"440":{"name":"Team Fortress 2","genre":"Team Shooter","description":"A class-based team shooter with distinct characters and play styles."},
"578080":{"name":"PUBG: BATTLEGROUNDS","genre":"Battle Royale","description":"Drop into a large-scale battle royale and fight to be the last squad standing."},
"1172470":{"name":"Apex Legends","genre":"Battle Royale","description":"A squad-based hero shooter with distinctive Legends and fast movement."},
"271590":{"name":"Grand Theft Auto V","genre":"Action / Open World","description":"Explore Los Santos in a sprawling open-world crime adventure."},
"1091500":{"name":"Cyberpunk 2077","genre":"RPG","description":"Explore Night City in a story-rich open-world role-playing game."},
"292030":{"name":"The Witcher 3: Wild Hunt","genre":"Action RPG","description":"Follow Geralt through a vast fantasy world filled with stories and monsters."},
"1245620":{"name":"ELDEN RING","genre":"Action RPG","description":"Explore the Lands Between in a challenging dark-fantasy adventure."},
"1086940":{"name":"Baldur's Gate 3","genre":"RPG","description":"Gather a party and shape a story in the Forgotten Realms."},
"105600":{"name":"Terraria","genre":"Sandbox","description":"Dig, fight, explore, and build in a richly layered 2D sandbox."},
"413150":{"name":"Stardew Valley","genre":"Simulation / RPG","description":"Build a farm, meet a community, and make a life in the valley."},
"252490":{"name":"Rust","genre":"Survival","description":"Gather, craft, build, and survive in a multiplayer world."},
"236390":{"name":"War Thunder","genre":"Vehicle Combat","description":"Combined-arms vehicle battles featuring aircraft, tanks, and ships."},
"1551360":{"name":"Forza Horizon 5","genre":"Racing","description":"Race across a vibrant open-world version of Mexico."},
"739630":{"name":"Phasmophobia","genre":"Co-op Horror","description":"Investigate haunted locations with a team of paranormal investigators."},
"945360":{"name":"Among Us","genre":"Social Deduction","description":"Complete tasks and find the impostor before the crew is eliminated."},
"550":{"name":"Left 4 Dead 2","genre":"Co-op Shooter","description":"Fight through co-op campaigns packed with infected enemies."},
"275850":{"name":"No Man's Sky","genre":"Exploration / Survival","description":"Explore a practically endless universe of planets and star systems."},
"1623730":{"name":"Palworld","genre":"Survival / Crafting","description":"Collect creatures, craft equipment, and build bases in an open world."},
"381210":{"name":"Dead by Daylight","genre":"Asymmetric Horror","description":"Multiplayer horror built around one killer and four survivors."},
"553850":{"name":"HELLDIVERS 2","genre":"Co-op Shooter","description":"Join a squad in chaotic cooperative missions across hostile planets."},
"108600":{"name":"Project Zomboid","genre":"Survival","description":"A detailed open-ended zombie apocalypse simulation."},
"1145360":{"name":"Hades","genre":"Roguelike","description":"Battle out of the Underworld in a fast-paced action roguelike."},
"620":{"name":"Portal 2","genre":"Puzzle","description":"Solve inventive physics puzzles using a portal gun."},
"4000":{"name":"Garry's Mod","genre":"Sandbox","description":"A physics sandbox built around creativity, tools, and community content."},
"230410":{"name":"Warframe","genre":"Action","description":"Master agile combat and customize your Warframe in a sci-fi universe."},
"359550":{"name":"Rainbow Six Siege","genre":"Tactical Shooter","description":"A tactical team shooter focused on gadgets and destructible environments."},
"1085660":{"name":"Destiny 2","genre":"Action MMO","description":"Explore a sci-fi universe through cooperative and competitive combat."},
"1174180":{"name":"Red Dead Redemption 2","genre":"Action / Open World","description":"An expansive western adventure set in the American frontier."},
"377160":{"name":"Fallout 4","genre":"RPG","description":"Explore a post-apocalyptic wasteland and rebuild your future."},
"489830":{"name":"Skyrim Special Edition","genre":"RPG","description":"Explore a vast fantasy world filled with quests, dragons, and dungeons."},
"218620":{"name":"PAYDAY 2","genre":"Co-op Heist","description":"Plan and execute cooperative heists with a crew."},
"322330":{"name":"Don't Starve Together","genre":"Survival","description":"Survive a strange wilderness together in a challenging co-op game."},
"346110":{"name":"ARK: Survival Evolved","genre":"Survival","description":"Tame dinosaurs, craft, and survive on a mysterious island."},
"251570":{"name":"7 Days to Die","genre":"Survival / Crafting","description":"Scavenge and build defenses in a zombie survival sandbox."},
"8930":{"name":"Civilization V","genre":"Strategy","description":"Build a civilization and guide it from ancient times into the future."},
"289070":{"name":"Civilization VI","genre":"Strategy","description":"Develop an empire through exploration, diplomacy, and war."},
"255710":{"name":"Cities: Skylines","genre":"City Builder","description":"Design, build, and manage a living modern city."},
"990080":{"name":"Hogwarts Legacy","genre":"Action RPG","description":"Explore a magical open world set in the wizarding world."},
"526870":{"name":"Satisfactory","genre":"Factory Builder","description":"Build sprawling factories on an alien planet."},
"1966720":{"name":"Lethal Company","genre":"Co-op Horror","description":"Scavenge abandoned moons with friends for a mysterious company."},
"239140":{"name":"Dying Light","genre":"Action / Survival","description":"Explore a city overrun by infected in a parkour-focused survival game."},
"252950":{"name":"Rocket League","genre":"Sports","description":"High-speed car soccer with competitive multiplayer."},
"304930":{"name":"Unturned","genre":"Survival","description":"A free-to-play zombie survival sandbox."},
"440900":{"name":"Conan Exiles","genre":"Survival","description":"Survive, build, and explore a brutal open world."},
"1238810":{"name":"Battlefield V","genre":"FPS","description":"Large-scale World War II battles across multiple modes."},
"1097150":{"name":"Fall Guys","genre":"Party","description":"Compete in chaotic obstacle-course party rounds."}}
# Load the curated list from data when present; the embedded dictionary remains a safe fallback.
try:
    featured_file = Path(__file__).resolve().parent / "data" / "popular_games.json"
    featured_rows = json.loads(featured_file.read_text(encoding="utf-8"))
    for row in featured_rows:
        app_id = str(row["appid"])
        POPULAR_GAMES[app_id] = {
            "name": str(row["name"]),
            "genre": str(row.get("genre", "PC game")),
            "description": str(row.get("description", "Featured PC game.")),
        }
except (OSError, ValueError, TypeError, KeyError):
    pass

class Catalog:
 def __init__(self,cache_path:Path):self.cache_path=cache_path
 def load_cached(self):
  try:
   data=json.loads(self.cache_path.read_text(encoding="utf-8")); return [Game(str(x["appid"]),str(x["name"]),str(x["appid"]) in POPULAR_GAMES) for x in data if x.get("name")]
  except (OSError,ValueError,TypeError,KeyError):return []
 def fetch_steam_catalog(self):
  req=urllib.request.Request(STEAM_APP_LIST_URL,headers={"User-Agent":"DiscodoLauncher/1.0"})
  with urllib.request.urlopen(req,timeout=45) as r:payload=json.loads(r.read().decode("utf-8"))
  unique={}
  for x in payload.get("applist",{}).get("apps",[]):
   name=str(x.get("name","")).strip(); aid=x.get("appid")
   if name and aid is not None:unique[str(aid)]=name
  if len(unique)<MIN_CATALOG_SIZE:raise RuntimeError(f"Steam returned {len(unique):,} entries; expected at least {MIN_CATALOG_SIZE:,}.")
  data=[{"appid":k,"name":v} for k,v in unique.items()]; self.cache_path.parent.mkdir(parents=True,exist_ok=True); tmp=self.cache_path.with_suffix(".tmp"); tmp.write_text(json.dumps(data,ensure_ascii=False,separators=(",",":")),encoding="utf-8"); tmp.replace(self.cache_path)
  return [Game(k,v,k in POPULAR_GAMES) for k,v in unique.items()]
 def fetch_featured_games(self):
  """Fetch the most-owned SteamSpy titles and cache 500 featured entries."""
  cache=self.cache_path.with_name("steam_featured.json")
  req=urllib.request.Request(STEAMSPY_TOP_URL,headers={"User-Agent":"DiscodoLauncher/1.0"})
  try:
   with urllib.request.urlopen(req,timeout=25) as r:payload=json.loads(r.read().decode("utf-8"))
   rows=[]
   if isinstance(payload,dict):
    for aid,row in payload.items():
     if not isinstance(row,dict):continue
     name=str(row.get("name","")).strip()
     if name and str(aid).isdigit():
      rows.append({"appid":str(aid),"name":name,"genre":"Popular Steam game","description":f"{name} — featured Steam title."})
   rows=rows[:FEATURED_LIMIT]
   if len(rows)<400:raise RuntimeError(f"SteamSpy returned only {len(rows)} usable games.")
   cache.parent.mkdir(parents=True,exist_ok=True)
   tmp=cache.with_suffix(".tmp");tmp.write_text(json.dumps(rows,ensure_ascii=False,separators=(",",":")),encoding="utf-8");tmp.replace(cache)
   return {x["appid"]:{"name":x["name"],"genre":x["genre"],"description":x["description"]} for x in rows}
  except Exception:
   try:
    rows=json.loads(cache.read_text(encoding="utf-8"))
    return {str(x["appid"]):{"name":str(x["name"]),"genre":str(x.get("genre","Popular Steam game")),"description":str(x.get("description","Featured Steam title."))} for x in rows[:FEATURED_LIMIT]}
   except (OSError,ValueError,TypeError,KeyError):
    return {k:v for k,v in POPULAR_GAMES.items()}
