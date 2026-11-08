"""Retsepti soovitaja (alfaversioon)

Projekti teema: retseptide soovitaja, mis aitab kasutajal otsustada, mida süüa teha. 
Kasutaja saab otsida retsepte või sisestada kodus olemasolevad toiduained, 
mille põhjal programm pakub sobivaid retsepte. 
Programm näitab ka retseptide valmistamiseks vajalikke koostisosi ja valmistamisjuhiseid.

Autorid: Naomi Maria Šamber ja Diana Veiman

Tööjaotus:
1. Diana - retseptide andmebaas, koostisosade valimine, retseptide otsimine koostisosade 
   järgi ja testimine.

2. Naomi - graafiline kasutajaliides, retseptikaardid, retseptide otsimine nime järgi, 
   koodi täiustamine ja dokumenteerimine.

Tehisaru kasutamine:
Projekti koostamisel kasutati ChatGPT abi Pythoni koodi
selgitamiseks, vigade leidmiseks ja parandamiseks.

Kasutatud allikad: 
1. https://docs.python.org/3/
2. https://www.w3schools.com/python/default.asp
3. https://www.geeksforgeeks.org/python/python-programming-language-tutorial/
4. https://www.pythontutorial.net/tkinter/tkinter-command/
5. Retseptide allikad on esitatud README.md failis.
...

Andmed loetakse failist Retseptid.json, mis peab asuma programmiga samas kaustas.
"""

import json
import tkinter as tk

tausta_värv = "#FFF5F3"
kastide_taust = "#BC827D"
aktsent = "#E65555"

font_pealkiri = ("Arial", 20, "bold")
font_alapealkiri = ("Arial", 12, "bold")
font_tavaline = ("Arial", 11)


def loe_retseptid(failinimi="Retseptid.json"):
    """Loeb retseptid JSON-failist ja tagastab need listina.

    Kui faili ei leitud, tagastab tühja listi."""

    try:
        with open(failinimi, "r", encoding="utf-8") as fail:
            return json.load(fail)
    except FileNotFoundError:
        return []


class RetseptiRakendus:
    """Retsepti soovitaja peaaken koos otsingu ja koostisosade valikuga."""

    def __init__(self, root):
        """Loob põhiakna: päis, otsinguriba, koostisosade nupp ja kaartide vaade."""
        self.root = root
        self.root.title("Retsepti soovitaja")
        self.root.geometry("700x700")
        self.root.configure(bg=tausta_värv)

        self.retseptid = loe_retseptid()

        # --- Ülemine päis ---

        päis_frame = tk.Frame(root, bg=kastide_taust, height=70)
        päis_frame.pack(fill="x", padx=20, pady=20)
        päis_frame.pack_propagate(False)

        pealkirja_label = tk.Label(
            päis_frame, 
            text="Retsepti soovitaja", 
            fg="white", 
            bg=kastide_taust, 
            font=font_pealkiri)
        pealkirja_label.pack(side="left", padx=20)

        # --- Otsingu rida ja menüünupp ---

        otsing_frame = tk.Frame(root, bg=tausta_värv)
        otsing_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.otsing_entry = tk.Entry(
            otsing_frame, 
            fg="gray", 
            relief="solid", 
            insertbackground="black", 
            bd=1)
        
        self.otsing_entry.insert(0, "Otsi...")
        self.otsing_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.otsing_entry.bind("<FocusIn>", self.kustuta_placeholder)
        self.otsing_entry.bind("<KeyRelease>", self.otsi_retsepte)

        menüü_nupp = tk.Button(
            otsing_frame, 
            text="x", 
            fg="black", 
            bg=aktsent, 
            width=3, 
            relief="flat", 
            cursor="hand2", 
            command=self.ava_menüü)
        menüü_nupp.pack(side="right")
        
        # --- Koostisosade valimise nupp ---
    
        koostisosade_nupp = tk.Button(
            root,
            text="Vali koostisosad",
            bg=aktsent,
            fg="black",
            activeforeground="black",
            relief="flat",
            cursor="hand2",
            command=self.ava_koostisosade_aken
        )
        koostisosade_nupp.pack(pady=(0, 10))
    
        # --- Koostisosade paneel peaaknas ---
    
        self.koostisosade_paneel = tk.Frame(
            root,
            bg=tausta_värv
        )
        
        self.paneel_nahtav = False 

        # --- Keritav kaartide vaade ---

        kerimisriba_konteiner = tk.Frame(
            root, 
            bg=tausta_värv
        )
        kerimisriba_konteiner.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.vaadatav = tk.Canvas(
            kerimisriba_konteiner, 
            bg=tausta_värv, 
            highlightthickness=0
        )
        kerimisriba = tk.Scrollbar(
            kerimisriba_konteiner, 
            orient="vertical", 
            command=self.vaadatav.yview
        )
        self.keritav_kast = tk.Frame(
            self.vaadatav, 
            bg=tausta_värv
        )

        self.keritav_kast.bind(
            "<Configure>", 
            lambda e: self.vaadatav.configure(scrollregion=self.vaadatav.bbox("all"))
        )

        self.kaardi_aken = self.vaadatav.create_window(
            (0, 0),
            window=self.keritav_kast,
            anchor="nw"
        )
        self.vaadatav.bind(
            "<Configure>",
            lambda e: self.vaadatav.itemconfigure(
                self.kaardi_aken,
                width=e.width
            )
        )
        
        self.vaadatav.configure(yscrollcommand=kerimisriba.set)

        self.vaadatav.pack(side="left", fill="both", expand=True)
        kerimisriba.pack(side="right", fill="y")

        self.kuva_kaardid(self.retseptid)

    def kustuta_placeholder(self, event):
        """Kustutab otsinguväljalt vihjeteksti "Otsi...", kui kasutaja sellele klõpsab."""
        if self.otsing_entry.get() == "Otsi...":
            self.otsing_entry.delete(0, tk.END)
            self.otsing_entry.config(fg="black")

    def ava_menüü(self):
        """Tühjendab otsinguvälja ja kuvab uuesti kõik retseptid."""
        self.otsing_entry.delete(0, tk.END)
        self.kuva_kaardid(self.retseptid)
        
    def ava_koostisosade_aken(self):
        """Näitab või peidab koostisosade valiku paneeli.

        Esimesel avamisel luuakse paneel ning koostisosade ruudustik koos otsingunupuga."""
        
        if self.paneel_nahtav:
            self.koostisosade_paneel.pack_forget()
            self.paneel_nahtav = False
            return
        
        if self.koostisosade_paneel.winfo_children():
            self.koostisosade_paneel.pack(
                fill="x",
                padx=20,
                pady=(0, 10),
                before=self.vaadatav.master
            )
            self.paneel_nahtav = True
            return
        
        self.koostisosade_paneel.pack(
            fill="x",
            padx=20,
            pady=(0, 10),
            before=self.vaadatav.master
        )
        
        self.paneel_nahtav = True
            
        pealkiri = tk.Label(
            self.koostisosade_paneel,
            text="Vali kodus olemasolevad toiduained:",
            bg=tausta_värv,
            fg="black"
        )
        pealkiri.pack(pady=10)

        veergude_arv = 4

        ruudustik_raam = tk.Frame(self.koostisosade_paneel, bg=tausta_värv)
        ruudustik_raam.pack(fill="x", padx=10)

        for veerg in range(veergude_arv):
            ruudustik_raam.columnconfigure(
                veerg, 
                weight=1, 
                uniform="koostisosa"
            )

    """Kogume kõikide retseptide koostisosad ühte hulka."""

        koostisosad = set()

        for retsept in self.retseptid:
            for koostisosa in retsept["koostisosad"]:
                koostisosad.add(koostisosa["nimi"])

        koostisosad = sorted(koostisosad, key=str.lower)

        self.valitud_koostisosad = {}

        rida = 0
        veerg = 0

        for nimi in koostisosad:
            muutuja = tk.BooleanVar(value=False)
            self.valitud_koostisosad[nimi] = muutuja

            valik = tk.Checkbutton(
                ruudustik_raam,
                text=nimi,
                variable=muutuja,
                bg=tausta_värv,
                fg="black",
                activebackground=tausta_värv,
                activeforeground="black",
                anchor="w",
                font=font_tavaline
            )

            valik.grid(row=rida, column=veerg, sticky="w", padx=5, pady=2)

            veerg += 1

            if veerg == veergude_arv:
                veerg = 0
                rida += 1
        
        # Retseptide otsimise nupp 
        
        otsi_nupp = tk.Button(
            self.koostisosade_paneel,
            text="Otsi retsepte",
            fg="black",
            command=self.otsi_koostisosade_jargi
        )
        otsi_nupp.pack(pady=10)
    
    def leia_retseptid_koostisosade_jargi(self, valitud, lubatud_puudu=0):
        """Leiab retseptid, mille koostisosadest on puudu kuni lubatud_puudu ainet.

        valitud -- hulk koostisosade nimedega, mis kasutaja kodus on.
        lubatud_puudu -- mitu koostisosa tohib retseptist puududa
        Tagastab retseptide listi, kus vähem puuduvaid koostisosi tuleb esimesena."""

        leitud_paarid = []

        for retsept in self.retseptid:
            vajalikud = set()

            for koostisosa in retsept["koostisosad"]:
                vajalikud.add(koostisosa["nimi"])

            puuduvad = vajalikud.difference(valitud)

            if vajalikud.intersection(valitud) and len(puuduvad) <= lubatud_puudu:
                leitud_paarid.append((len(puuduvad), retsept))

        leitud_paarid.sort(key=self.puuduvate_arv)

        leitud_retseptid = []

        for puuduvate_arv, retsept in leitud_paarid:
            leitud_retseptid.append(retsept)

        return leitud_retseptid

    def puuduvate_arv(self, paar):
        """Tagastab paari (puuduvate arv, retsept) esimese elemendi sorteerimiseks."""
        return paar[0]
    
    def otsi_koostisosade_jargi(self):
        """Kogub valitud koostisosad märkeruutudest ja kuvab sobivad retseptid."""
        valitud = set()
        
        for nimi, muutuja in self.valitud_koostisosad.items():
            if muutuja.get():
                valitud.add(nimi)
        
        if not valitud:
            self.kuva_kaardid(self.retseptid)
            return
        
        leitud = self.leia_retseptid_koostisosade_jargi(valitud, lubatud_puudu=5)
        self.kuva_kaardid(leitud)
        
    def otsi_retsepte(self, event):
        """Filtreerib retsepte nime järgi vastavalt otsinguväljale."""
        otsitav = self.otsing_entry.get().strip().lower()
        if otsitav == "otsi..." or not otsitav:
            leitud = self.retseptid
        else:
            leitud = []
            for retsept in self.retseptid:
                retsepti_nimi = retsept.get('nimi', '').lower()

                if otsitav in retsepti_nimi:
                    leitud.append(retsept)
        self.kuva_kaardid(leitud)

    def kuva_kaardid(self, retseptid_list):
        """Kuvab antud retseptid klõpsatavate kaartidena."""
        for widget in self.keritav_kast.winfo_children():
            widget.destroy()

        if not retseptid_list:
            tk.Label(self.keritav_kast, text="Ühtegi retsepti ei leitud. Vali veel koostisosi ja proovi uuesti.", bg=tausta_värv, wraplength=400, fg="gray").pack(pady=20)
            return
        
        for retsept in retseptid_list:

            klõpsatav_kast = tk.Frame(
                self.keritav_kast, 
                bg=kastide_taust, 
                highlightbackground=aktsent, 
                highlightthickness=1, 
                cursor="hand2"
            )
            klõpsatav_kast.pack(fill="x", pady=8, ipadx=5, ipady=5)
            klõpsatav_kast.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

            # Pealkiri + lühikirjeldus
            vasak_pool = tk.Frame(klõpsatav_kast, bg=kastide_taust)
            vasak_pool.pack(side="left", fill="both", expand=True, padx=12, pady=12)
            vasak_pool.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

            retsepti_header = tk.Frame(vasak_pool, bg=aktsent)
            retsepti_header.pack(fill="x", pady=(0, 8))

            retsepti_nimi = tk.Label(
                retsepti_header, 
                text=retsept.get('nimi', 'Retsept'), 
                fg="white", 
                wraplength=250, 
                justify="left", 
                anchor="w", 
                bg=aktsent, 
                cursor="hand2", 
                font=font_alapealkiri
            )
            retsepti_nimi.pack(fill="x", padx=8, pady=6)
            retsepti_nimi.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

            # Lühike kirjeldus
            kirjelduse_tekst = retsept.get(
                'kirjeldus', f"Portsjonid: {retsept.get('portsioonid', 'Pole märgitud')}"
            )
            lbl_kirjeldus = tk.Label(
                vasak_pool, 
                text=kirjelduse_tekst, 
                bg=kastide_taust, 
                fg="white", 
                justify="left", 
                anchor="w", 
                wraplength=420, 
                cursor="hand2", 
                font=font_tavaline
            )
            lbl_kirjeldus.pack(fill="x")
            lbl_kirjeldus.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

            # Pildiala
            parem_pool = tk.Frame(
                klõpsatav_kast,
                bg=aktsent, 
                width=60, 
                height=60, 
                cursor="hand2"
            )
            parem_pool.pack(side="right", padx=12, pady=12)
            parem_pool.pack_propagate(False)
            parem_pool.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

            lbl_pilt = tk.Label(
                parem_pool, 
                text="*pilt*", 
                fg="white", 
                bg=aktsent, 
                cursor="hand2"
            )
            lbl_pilt.pack(expand=True)
            lbl_pilt.bind("<Button-1>", lambda e, r=retsept: self.ava_detailaken(r))

    def ava_detailaken(self, retsept):
        """Kuvab retsepti kirjelduse, koostisosad ja valmistamisjuhise."""
        for widget in self.keritav_kast.winfo_children():
            widget.destroy()
            
        tagasi_nupp = tk.Button(
            self.keritav_kast,
            text="Tagasi retseptide juurde",
            fg="black",
            command=lambda: self.kuva_kaardid(self.retseptid)
        )
        tagasi_nupp.pack(pady=10)
        
        # Retsepti pealkiri
        retsepti_pealkiri = tk.Label(
            self.keritav_kast,
            text=retsept["nimi"],
            bg=tausta_värv,
            fg="black",
            font=("Arial", 18, "bold"),
            wraplength=450
        )
        retsepti_pealkiri.pack(pady=15)

        # Sisu tekstiala
        sisu_frame = tk.Frame(
            self.keritav_kast, 
            bg=kastide_taust, 
            highlightbackground=aktsent, 
            highlightthickness=1
        )
        sisu_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tekstikast = tk.Text(
            sisu_frame, 
            wrap="word", 
            bg=kastide_taust, 
            bd=0, 
            padx=15, 
            pady=15
        )
        tekstikast.pack(fill="both", expand=True)

        # Erinevad tekstid
        tekstikast.tag_configure("pealkiri", font=font_alapealkiri)
        tekstikast.tag_configure("tavaline", font=font_tavaline)

        # Kirjeldus / Portsjonid
        tekstikast.insert(tk.END, "Kirjeldus / Info:\n", "pealkiri")
        kirjeldus = retsept.get(
            'kirjeldus', f"Portsjonid: {retsept.get('portsioonid', 'Määramata')}")
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


def main():
    """Käitab retsepti soovitaja rakenduse."""
    root = tk.Tk()
    app = RetseptiRakendus(root)
    root.mainloop()


if __name__ == "__main__":
    main()
