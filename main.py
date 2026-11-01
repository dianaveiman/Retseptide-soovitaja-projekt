import json
import tkinter as tk
from tkinter import ttk

tausta_värv = "#FFF5F3"
kastide_taust = "#BC827D"
aktsent = "#E65555"

def loe_retseptid(failinimi="Retseptid.json"):
    try:
        with open(failinimi, "r", encoding="utf-8") as fail:
            return json.load(fail)
    except FileNotFoundError:
        return []

class RetseptiRakendus:
    def __init__(self, root):
        self.root = root
        self.root.title("Retsepti soovitaja")
        self.root.geometry("700x700")
        self.root.configure(bg=tausta_värv)

        self.retseptid = loe_retseptid()

    # --- Ülemine päis ---

        päis_frame = tk.Frame(root, bg=kastide_taust, height=70)
        päis_frame.pack(fill="x", padx=20, pady=20)
        päis_frame.pack_propagate(False)

        pealkirja_lable = tk.Label(päis_frame, text="Retsepti soovitaja", fg="white", bg=kastide_taust)
        pealkirja_lable.pack(side="left", padx=20)

    # --- Otsingu rida ja menüünupp ---

        otsing_frame = tk.Frame(root, bg=tausta_värv)
        otsing_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.otsing_entry = tk.Entry(otsing_frame, fg="gray", relief="solid", bd=1)
        self.otsing_entry.insert(0, "Otsi...")
        self.otsing_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.otsing_entry.bind("<FocusIn>", self.kustuta_placeholder)
        self.otsing_entry.bind("<KeyRelease>", self.otsi_retsepte)

        menüü_nupp = tk.Button(otsing_frame, text="x", fg="white", bg=aktsent, width=3, relief="flat", cursor="hand2", command=self.ava_menüü)
        menüü_nupp.pack(side="right")

    # --- Keritav kaartide vaade ---

        kerimisriba_konteiner = tk.Frame(root, bg=tausta_värv)
        kerimisriba_konteiner.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.vaadatav = tk.Canvas(kerimisriba_konteiner, bg=tausta_värv, highlightthickness=0)
        kerimisriba = tk.Scrollbar(kerimisriba_konteiner, orient="vertical", command=self.vaadatav.yview)
        self.keritav_kast = tk.Frame(self.vaadatav, bg=tausta_värv)

        self.keritav_kast.bind("<Configure>", lambda e: self.vaadatav.configure(scrollregion=self.vaadatav.bbox("all")))

        self.vaadatav.create_window((0,0), window=self.keritav_kast, anchor="nw")
        self.vaadatav.configure(yscrollcommand=kerimisriba.set)

        self.vaadatav.pack(side="left", fill="both", expand=True)
        kerimisriba.pack(side="right", fill="y")

        self.kuva_kaardid(self.retseptid)

    def kustuta_placeholder(self, event):
        if self.otsing_entry.get() == "Otsi...":
            self.otsing_entry.delete(0, tk.END)
            self.otsing_entry.config(fg="black")

    def ava_menüü(self):
        print("Menüü avati")

    def otsi_retsepte(self, event):
        otsitav = self.otsing_entry.get().strip().lower()
        if otsitav == "Otsi..." or not otsitav:
            leitud = self.retseptid
        else:
            leitud = [r for r in self.retseptid if otsitav in r.get('nimi', '').lower()]
        self.kuva_kaardid(leitud)

    def kuva_kaardid(self, retseptid_list):
        for widget in self.keritav_kast.winfo_children():
            widget.destroy()

        if not retseptid_list:
            tk.Label(self.keritav_kast, text="Ühtegi retsepti ei leitud.", bg=tausta_värv, fg="gray").pack(pady=20)
            return
        
        for retsept in retseptid_list:

            klõpsatav_kast = tk.Frame(self.keritav_kast, bg=kastide_taust, highlightbackground=aktsent, highlightthickness=1, cursor="hand2")
            klõpsatav_kast.pack(fill="x", pady=8, ipadx=5, ipady=5)
            klõpsatav_kast.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

            # Pealkiri + lühikirjeldus
            vasak_pool = tk.Frame(klõpsatav_kast, bg=kastide_taust)
            vasak_pool.pack(side="left", fill="both", expand=True, padx=12, pady=12)
            vasak_pool.bind("<Button-1>", lambda e, r=retsept : self.ava_detailaken(r))

            retsepti_header = tk.Frame(vasak_pool, bg=aktsent, height=32)
            retsepti_header.pack(fill="x", pady=(0, 8))
            retsepti_header.pack_propagate(False)
            retsepti_header.pack_propagate(False)

            retsepti_nimi = tk.Label(retsepti_header, text=retsept.get('nimi', 'Retsept'), fg="white", bg=aktsent, cursor="hand2")
            retsepti_nimi.pack(side="left", padx=8)
            retsepti_nimi.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

            #Lühike kirjeldus
            kirjelduse_tekst = retsept.get('kirjeldus', f"Portsjonid: {retsept.get('portsioonid', 'Pole märgitud')}")
            lbl_kirjeldus = tk.Label(vasak_pool, text=kirjelduse_tekst, bg=kastide_taust, fg="white", justify="left", anchor="w", wraplength=420, cursor="hand2")
            lbl_kirjeldus.pack(fill="x")
            lbl_kirjeldus.bind("<Button-1>", lambda e, r=retsept : self.ava_detailaken(r))

            #Pildiala
            parem_pool = tk.Frame(klõpsatav_kast, bg=aktsent, width=60, height=60, cursor="hand2")
            parem_pool.pack(side="right", padx=12, pady=12)
            parem_pool.pack_propagate(False)
            parem_pool.bind("<Button-1>", lambda e, r=retsept : self.ava_detailaken(r))

            lbl_pilt = tk.Label(parem_pool, text="*pilt*", fg="white", bg=aktsent, cursor="hand2")
            lbl_pilt.pack(expand=True)
            lbl_pilt.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

    def ava_detailaken(self, retsept):
        # Uus hüpikaken
        aken = tk.Toplevel(self, root)
        aken.title(retsept.get('nimi', 'Retsept'))
        aken.geometry("500x600")
        aken.configure(bg=tausta_värv)

        # Sisu tekstiala
        sisu_frame = tk.Frame(aken, bg=kastide_taust, highlightbackground=aktsent, highlightthickness=1)
        sisu_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tekstikast = tk.Text(sisu_frame, wrap="word", bg=kastide_taust, bd=0, padx=15, pady=15)
        tekstikast.pack(fill="both", expand=True)

        # Kirjeldus / Portsjonid
        tekstikast.insert(tk.END, "Kirjeldus / Info:\n", "pealkiri")
        kirjeldus = retsept.get('kirjeldus', f"Portsjonid: {retsept.get('portsioonid', 'Määramata')}")
        tekstikast.insert(tk.END, f"{kirjeldus}\n\n", "tavaline")

        # Koostisosad (kuna JSON-is on need objektidena: {"nimi": ..., "kogus": ..., "ühik": ...})
        tekstikast.insert(tk.END, "Koostisosad:\n", "pealkiri")
        for aine in retsept.get('koostisosad', []):
            nimi = aine.get('nimi', '')
            kogus = aine.get('kogus', '')
            ühik = aine.get('ühik', '')
            tekstikast.insert(tk.END, f" - {nimi}: {kogus} {ühik}\n", "tavaline")

        # Valmistamisjuhis (kuna JSON-is on see nimega 'valmistamine' ja kujul list ridadest)
        tekstikast.insert(tk.END, "\nValmistamisjuhis:\n", "pealkiri")
        juhised = retsept.get('valmistamine', [])
        if isinstance(juhised, list):
            for samm_nr, samm in enumerate(juhised, 1):
                tekstikast.insert(tk.END, f"{samm_nr}. {samm}\n", "tavaline")
        else:
            tekstikast.insert(tk.END, f"{juhised}\n", "tavaline")

        tekstikast.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = RetseptiRakendus(root)
    root.mainloop()