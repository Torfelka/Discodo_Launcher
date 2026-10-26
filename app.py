import json, os, queue, subprocess, sys, threading, urllib.request, webbrowser
from io import BytesIO
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None
from catalog import Catalog, POPULAR_GAMES
from launcher import launch_game

ROOT=Path(__file__).resolve().parent
CACHE=Path(os.getenv("LOCALAPPDATA") or os.getenv("XDG_CACHE_HOME") or Path.home())/"DiscodoLauncher"
COVERS=CACHE/"covers"; SETTINGS=CACHE/"settings.json"
BG="#0b0d12"; PANEL="#11151e"; PANEL2="#171c28"; PANEL3="#202738"; FG="#edf0fa"; MUTED="#909bb2"; ACCENT="#6255dc"
LANGS={"English":"en","Русский":"ru","Polski":"pl","Deutsch":"de","Українська":"uk"}
T={
"en":{"library":"LIBRARY","search":"Search 5,000+ games…","all":"All games","popular":"Popular","installed":"Installed","browse":"Browse…","play":"▶  PLAY GAME","steam":"OPEN STEAM PAGE","path":"GAME EXECUTABLE","none":"No executable selected","loading":"Loading Steam catalog…","ready":"Catalog ready","offline":"Steam catalog unavailable — cache retained","description":"Your searchable PC game library","choose":"Choose game executable","folder":"Open game folder","favorite":"★ Favorite","select":"Select a game from the library","results":"results","featured":"Featured game · Steam cover art"},
"ru":{"library":"БИБЛИОТЕКА","search":"Поиск среди 5 000+ игр…","all":"Все игры","popular":"Популярные","installed":"Установленные","browse":"Обзор…","play":"▶  ЗАПУСТИТЬ ИГРУ","steam":"ОТКРЫТЬ В STEAM","path":"ИСПОЛНЯЕМЫЙ ФАЙЛ ИГРЫ","none":"Файл игры не выбран","loading":"Загружаем каталог Steam…","ready":"Каталог загружен","offline":"Steam недоступен — используем сохранённый каталог","description":"Твоя библиотека игр для ПК с поиском","choose":"Выбрать исполняемый файл игры","folder":"Открыть папку игры","favorite":"★ В избранное","select":"Выбери игру в библиотеке","results":"результатов","featured":"Популярная игра · обложка Steam"},
"pl":{"library":"BIBLIOTEKA","search":"Szukaj wśród 5 000+ gier…","all":"Wszystkie","popular":"Popularne","installed":"Zainstalowane","browse":"Przeglądaj…","play":"▶  URUCHOM GRĘ","steam":"OTWÓRZ STEAM","path":"PLIK GRY","none":"Nie wybrano pliku","loading":"Ładowanie katalogu Steam…","ready":"Katalog gotowy","offline":"Steam niedostępny — cache zachowany","description":"Przeszukiwalna biblioteka gier PC","choose":"Wybierz plik gry","folder":"Otwórz folder gry","favorite":"★ Ulubione","select":"Wybierz grę z biblioteki","results":"wyników","featured":"Popularna gra · okładka Steam"},
"de":{"library":"BIBLIOTHEK","search":"5.000+ Spiele durchsuchen…","all":"Alle Spiele","popular":"Beliebt","installed":"Installiert","browse":"Durchsuchen…","play":"▶  SPIEL STARTEN","steam":"STEAM-SEITE","path":"SPIELDATEI","none":"Keine Datei ausgewählt","loading":"Steam-Katalog wird geladen…","ready":"Katalog bereit","offline":"Steam nicht verfügbar — Cache bleibt erhalten","description":"Durchsuchbare PC-Spielbibliothek","choose":"Spiel-Datei auswählen","folder":"Spielordner öffnen","favorite":"★ Favorit","select":"Wähle ein Spiel aus","results":"Ergebnisse","featured":"Beliebtes Spiel · Steam-Cover"},
"uk":{"library":"БІБЛІОТЕКА","search":"Пошук серед 5 000+ ігор…","all":"Усі ігри","popular":"Популярні","installed":"Установлені","browse":"Огляд…","play":"▶  ЗАПУСТИТИ ГРУ","steam":"СТОРІНКА STEAM","path":"ФАЙЛ ГРИ","none":"Файл не вибрано","loading":"Завантажуємо каталог Steam…","ready":"Каталог завантажено","offline":"Steam недоступний — кеш збережено","description":"Пошукова бібліотека ігор для ПК","choose":"Вибрати файл гри","folder":"Відкрити теку гри","favorite":"★ В обране","select":"Вибери гру з бібліотеки","results":"результатів","featured":"Популярна гра · обкладинка Steam"}}
class App(tk.Tk):
 def __init__(self):
  super().__init__(); self.title("Discodo Launcher"); self.geometry("1240x780"); self.minsize(950,600); self.configure(bg=BG)
  CACHE.mkdir(parents=True,exist_ok=True); COVERS.mkdir(parents=True,exist_ok=True)
  try:self.settings=json.loads(SETTINGS.read_text(encoding="utf-8"))
  except Exception:self.settings={"paths":{},"favorites":[],"language":"ru"}
  self.lang=self.settings.get("language","ru"); self.catalog=Catalog(CACHE/"steam_apps.json"); self.games=[]; self.filtered=[]; self.selected=None; self.photos={}; self.queue=queue.Queue(); self.mode="all"; self.search_var=tk.StringVar(); self.search_var.trace_add("write",lambda *_:self.refresh()); self.status=tk.StringVar(value=self.t("loading"))
  self.style(); self.build(); self.games=self.catalog.load_cached(); self.merge_popular(); self.refresh(); self.after(100,self.poll); threading.Thread(target=self.fetch,daemon=True).start()
 def t(self,k):return T.get(self.lang,T["en"]).get(k,T["en"].get(k,k))
 def save(self):SETTINGS.write_text(json.dumps(self.settings,ensure_ascii=False,indent=2),encoding="utf-8")
 def style(self):
  s=ttk.Style(self); s.theme_use("clam"); s.configure(".",font=("Segoe UI",10),background=BG,foreground=FG); s.configure("TFrame",background=BG); s.configure("TLabel",background=BG,foreground=FG); s.configure("TButton",padding=(11,9),background=PANEL3,foreground=FG,borderwidth=0); s.map("TButton",background=[("active",PANEL2)]); s.configure("Accent.TButton",padding=(14,12),background=ACCENT,foreground="white",font=("Segoe UI Semibold",10)); s.map("Accent.TButton",background=[("active","#887cff")]); s.configure("TCombobox",fieldbackground=PANEL2,background=PANEL2,foreground=FG,arrowcolor=FG); s.configure("Vertical.TScrollbar",background=PANEL,troughcolor=BG,arrowcolor=MUTED)
 def build(self):
  h=tk.Frame(self,bg=BG,padx=23,pady=16); h.pack(fill="x"); tk.Label(h,text="D",font=("Segoe UI Black",22),bg=ACCENT,fg="white",width=2,pady=2).pack(side="left",padx=(0,11)); tk.Label(h,text="Discodo",font=("Segoe UI Semibold",23),bg=BG,fg=FG).pack(side="left"); tk.Label(h,text="  LAUNCHER",font=("Segoe UI Semibold",9),bg=BG,fg=MUTED).pack(side="left",pady=(10,0))
  r=tk.Frame(h,bg=BG); r.pack(side="right"); self.count=tk.Label(r,text="Steam catalog",bg=BG,fg="#69d6a2",font=("Segoe UI Semibold",10)); self.count.pack(side="left",padx=12); self.langbox=ttk.Combobox(r,width=12,state="readonly",values=list(LANGS)); self.langbox.set(next((n for n,c in LANGS.items() if c==self.lang),"Русский")); self.langbox.pack(side="left"); self.langbox.bind("<<ComboboxSelected>>",self.change_lang); ttk.Button(r,text="↻",width=3,command=lambda:threading.Thread(target=self.fetch,daemon=True).start()).pack(side="left",padx=(7,0))
  body=tk.Frame(self,bg=BG); body.pack(fill="both",expand=True,padx=18,pady=(0,12)); side=tk.Frame(body,bg=PANEL,width=330,padx=14,pady=15); side.pack(side="left",fill="y"); side.pack_propagate(False); tk.Label(side,text=self.t("library"),bg=PANEL,fg=MUTED,font=("Segoe UI Semibold",10)).pack(anchor="w",pady=(0,10)); tk.Entry(side,textvariable=self.search_var,bg=PANEL2,fg=FG,insertbackground=FG,relief="flat",font=("Segoe UI",11)).pack(fill="x",ipady=10,pady=(0,12))
  f=tk.Frame(side,bg=PANEL); f.pack(fill="x",pady=(0,10))
  for label,mode in [(self.t("all"),"all"),(self.t("popular"),"popular"),(self.t("installed"),"installed")]:tk.Button(f,text=label,command=lambda m=mode:self.set_mode(m),bg=PANEL3 if mode=="all" else PANEL,fg=FG,activebackground=PANEL3,relief="flat",padx=8,pady=7,cursor="hand2").pack(side="left",padx=(0,4))
  lf=tk.Frame(side,bg=PANEL); lf.pack(fill="both",expand=True); self.list=tk.Listbox(lf,bg=PANEL,fg=FG,selectbackground=ACCENT,selectforeground="white",activestyle="none",relief="flat",borderwidth=0,highlightthickness=0,font=("Segoe UI",10),exportselection=False); sb=ttk.Scrollbar(lf,orient="vertical",command=self.list.yview); self.list.configure(yscrollcommand=sb.set); self.list.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y"); self.list.bind("<<ListboxSelect>>",self.select_game); self.listcount=tk.Label(side,text="Loading…",bg=PANEL,fg=MUTED,anchor="w"); self.listcount.pack(fill="x",pady=(9,0))
  main=tk.Frame(body,bg=BG,padx=22,pady=8); main.pack(side="left",fill="both",expand=True); tk.Label(main,text=self.t("description"),bg=BG,fg=MUTED).pack(anchor="w"); self.title_label=tk.Label(main,text=self.t("select"),bg=BG,fg=FG,font=("Segoe UI Semibold",26),wraplength=700,justify="left"); self.title_label.pack(anchor="w",pady=(9,2)); self.subtitle=tk.Label(main,text="",bg=BG,fg=MUTED); self.subtitle.pack(anchor="w")
  card=tk.Frame(main,bg=PANEL,padx=16,pady=16); card.pack(fill="x",pady=(22,16)); self.cover=tk.Label(card,text="DISCODO",width=20,height=12,bg=PANEL3,fg=MUTED,font=("Segoe UI Semibold",11)); self.cover.pack(side="left",anchor="n",padx=(0,18)); d=tk.Frame(card,bg=PANEL); d.pack(side="left",fill="both",expand=True); tk.Label(d,text="GAME DETAILS",bg=PANEL,fg=MUTED,font=("Segoe UI Semibold",9)).pack(anchor="w"); self.desc=tk.Label(d,text="",bg=PANEL,fg=FG,font=("Segoe UI",11),justify="left",anchor="nw",wraplength=500); self.desc.pack(fill="x",anchor="w",pady=(12,18)); self.appid=tk.Label(d,text="",bg=PANEL,fg=MUTED,font=("Consolas",10)); self.appid.pack(anchor="w"); self.covernote=tk.Label(d,text="",bg=PANEL,fg=MUTED,font=("Segoe UI",9)); self.covernote.pack(anchor="w",pady=(8,0))
  tk.Label(main,text=self.t("path"),bg=BG,fg=MUTED,font=("Segoe UI Semibold",10)).pack(anchor="w",pady=(6,8)); row=tk.Frame(main,bg=BG); row.pack(fill="x"); self.pathvar=tk.StringVar(value=self.t("none")); tk.Entry(row,textvariable=self.pathvar,bg=PANEL2,fg=FG,relief="flat",state="readonly",readonlybackground=PANEL2).pack(side="left",fill="x",expand=True,ipady=9); ttk.Button(row,text=self.t("browse"),command=self.browse).pack(side="left",padx=(8,0))
  a=tk.Frame(main,bg=BG); a.pack(fill="x",pady=(14,0)); self.playbtn=ttk.Button(a,text=self.t("play"),style="Accent.TButton",command=self.play); self.playbtn.pack(side="left"); ttk.Button(a,text=self.t("steam"),command=self.open_steam).pack(side="left",padx=8); ttk.Button(a,text=self.t("favorite"),command=self.favorite).pack(side="left"); ttk.Button(a,text=self.t("folder"),command=self.open_folder).pack(side="left",padx=8); tk.Label(self,textvariable=self.status,bg=PANEL,fg=MUTED,anchor="w",padx=17,pady=10,font=("Segoe UI",9)).pack(fill="x",side="bottom")
 def change_lang(self,_=None):self.lang=LANGS.get(self.langbox.get(),"en"); self.settings["language"]=self.lang; self.save(); self.refresh()
 def merge_popular(self):
  d={g.app_id:g for g in self.games}
  for aid,x in POPULAR_GAMES.items():d[aid]=type("GameEntry",(),{"app_id":aid,"name":x["name"],"popular":True,"genre":x["genre"],"description":x["description"]})()
  self.games=sorted(d.values(),key=lambda g:(not g.popular,g.name.casefold()))
 def fetch(self):
  try:self.queue.put(("catalog",self.catalog.fetch_steam_catalog()))
  except Exception as e:self.queue.put(("error",str(e)))
 def poll(self):
  try:
   while True:
    kind,data=self.queue.get_nowait()
    if kind=="catalog":self.games=data; self.merge_popular(); self.refresh(); self.count.config(text=f"{len(self.games):,} GAMES"); self.status.set(f"{len(self.games):,} {self.t('ready')}")
    elif kind=="cover":
     if self.selected and self.selected.app_id==data:self.show_cover(self.selected)
    elif kind=="cover-missing":
     if self.selected and self.selected.app_id==data:self.covernote.config(text="Cover unavailable from Steam CDN.")
    else:self.status.set(f"{self.t('offline')}: {str(data)[:130]}")
  except queue.Empty:pass
  self.after(120,self.poll)
 def set_mode(self,m):self.mode=m; self.refresh()
 def refresh(self):
  if not hasattr(self,"list"):return
  q=self.search_var.get().strip().casefold(); paths=self.settings.get("paths",{})
  items=[g for g in self.games if (self.mode!="popular" or g.popular) and (self.mode!="installed" or g.app_id in paths) and (not q or q in g.name.casefold() or q in g.app_id)]
  self.filtered=items[:3000]; cur=self.selected.app_id if self.selected else None; self.list.delete(0,"end"); fav=set(self.settings.get("favorites",[]))
  for g in self.filtered:self.list.insert("end",("★ " if g.app_id in fav else "◆ " if g.popular else "   ")+g.name)
  self.listcount.config(text=f"{len(items):,} {self.t('results')} · showing {len(self.filtered):,}")
  if cur:
   for i,g in enumerate(self.filtered):
    if g.app_id==cur:self.list.selection_set(i); self.list.see(i); break
  elif self.filtered:self.selected=self.filtered[0]; self.list.selection_set(0); self.render(self.selected)
 def select_game(self,_=None):
  s=self.list.curselection()
  if s and s[0]<len(self.filtered):self.selected=self.filtered[s[0]]; self.render(self.selected)
 def render(self,g):
  self.title_label.config(text=g.name); self.subtitle.config(text=("POPULAR  •  " if g.popular else "")+g.genre); self.desc.config(text=g.description if g.popular else "Steam catalog entry. Choose the actual executable installed on your PC to launch it."); self.appid.config(text=f"STEAM APP ID   {g.app_id}"); p=self.settings.get("paths",{}).get(g.app_id,""); self.pathvar.set(p or self.t("none")); self.playbtn.config(state="normal" if p else "disabled")
  if g.popular:self.load_cover(g)
  else:self.cover.config(image="",text="NO COVER\n\nCatalog entry",width=20,height=12); self.cover.image=None; self.covernote.config(text="Cover art is reserved for featured games.")
  self.status.set(f"{g.name} · Steam App ID {g.app_id}")
 def load_cover(self,g):
  p=COVERS/f"{g.app_id}.jpg"
  if p.exists() and Image:self.show_cover(g); return
  self.cover.config(image="",text="LOADING\nCOVER",width=20,height=12); self.cover.image=None; self.covernote.config(text=self.t("featured")); threading.Thread(target=self.download_cover,args=(g.app_id,),daemon=True).start()
 def download_cover(self,aid):
  if not Image:return
  try:
   req=urllib.request.Request(f"https://cdn.akamai.steamstatic.com/steam/apps/{aid}/library_600x900.jpg",headers={"User-Agent":"DiscodoLauncher/1.0"})
   with urllib.request.urlopen(req,timeout=12) as r:data=r.read()
   im=Image.open(BytesIO(data)).convert("RGB"); im.thumbnail((190,270)); im.save(COVERS/f"{aid}.jpg","JPEG",quality=88); self.queue.put(("cover",aid))
  except Exception:self.queue.put(("cover-missing",aid))
 def show_cover(self,g):
  if not Image:return
  try:
   im=Image.open(COVERS/f"{g.app_id}.jpg").convert("RGB"); im.thumbnail((190,270)); photo=ImageTk.PhotoImage(im); self.photos[g.app_id]=photo; self.cover.config(image=photo,text="",width=190,height=270); self.cover.image=photo; self.covernote.config(text="Cover cached locally")
  except Exception:pass
 def browse(self):
  if not self.selected:return
  p=filedialog.askopenfilename(title=self.t("choose"),filetypes=[("Executable","*.exe *.bat *.cmd" if os.name=="nt" else "*"),("All files","*.*")])
  if p:self.settings.setdefault("paths",{})[self.selected.app_id]=p; self.save(); self.pathvar.set(p); self.playbtn.config(state="normal"); self.status.set(f"Saved: {p}")
 def play(self):
  if not self.selected:return
  p=self.settings.get("paths",{}).get(self.selected.app_id)
  if not p:messagebox.showinfo("Discodo",self.t("choose")); return
  try:launch_game(p); self.status.set(f"Launched {self.selected.name}")
  except Exception as e:messagebox.showerror("Discodo",str(e)); self.status.set(f"Launch failed: {e}")
 def open_steam(self):
  if self.selected:webbrowser.open(f"https://store.steampowered.com/app/{self.selected.app_id}/")
 def favorite(self):
  if not self.selected:return
  f=set(self.settings.get("favorites",[])); aid=self.selected.app_id; f.remove(aid) if aid in f else f.add(aid); self.settings["favorites"]=sorted(f); self.save(); self.refresh()
 def open_folder(self):
  if not self.selected:return
  p=self.settings.get("paths",{}).get(self.selected.app_id)
  if not p:self.status.set(self.t("none")); return
  folder=str(Path(p).resolve().parent)
  try:os.startfile(folder) if os.name=="nt" else subprocess.Popen(["open" if sys.platform=="darwin" else "xdg-open",folder])
  except Exception as e:messagebox.showerror("Discodo",str(e))
if __name__=="__main__":
 if Image is None:print("Install Pillow for cover art: python -m pip install -r requirements.txt")
 App().mainloop()
