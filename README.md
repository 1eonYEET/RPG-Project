# ⚔️ Console RPG – Turn-Based Adventure in Python

Ein kleines **konsolenbasiertes RPG** in Python, das bewusst nach **SOLID-Prinzipien** entworfen ist.

---

## 🎮 Features

- **5 Klassen** zur Auswahl:
  - 🛡️ **Tank** – viel Leben, viel Rüstung, weniger Schaden, besseres Heilen  
  - 🗡️ **Assassin** – hoher Schaden, Crit & Dodge, wenig Leben  
  - 🔮 **Mage** – mehr Mana, mächtige Zauber
  - 🧛 **Vampire** - Lifesteal skalierend mit Schaden
  - ⚔️ **Knight** – ausgewogener Allrounder

- **3 Companions** zur Auswahl:
  - 💚 **Heilender Sprite** – Heilt dich vor jedem Kampf um 10 HP  
  - 💰 **Gold-Gremlin** – Gibt dir nach jedem Kampf 20% Bonus-Gold zusätzlich zum normalen Gewinn  
  - 🛡️ **Opfergeist** – Rettet dich einmal pro Kampf vor dem sicheren Tod (du überlebst mit 1 HP und verlierst dabei keine HP) 

- **Kampfsystem**:
  - Rundenbasiert mit Skills & Heiltränken  
  - Gegner können kritisch treffen oder ausweichen  
  - Bosse mit Portraits & Drops alle 5 Wellen  
  - Nach Bosskämpfen werden HP und Mana vollständig regeneriert  

- **Fähigkeiten**:
  - Klassenspezifische Skills und **Ultimative Fähigkeiten** (einmal pro Kampf einsetzbar)  
  - Skills haben klare Beschreibungen & Manakosten  
  - Beispiele: `Feuerball`, `Heilen`, `Durchdringender Schlag`, Ultis wie `Unzerstörbar` oder `Arkaner Sturm`

- **Progression**:
  - XP & Level-Ups  
  - **Skilltree** mit passiven Boni und neuen Fähigkeiten (Vorher→Nachher-Vorschau)  
  - Ultimative Fähigkeiten werden über den Skilltree freigeschaltet  
  - Items & Ausrüstung im **Shop** (stackende Effekte, Vorher→Nachher-Vorschau)  
  - Gold-Belohnungen + Boss-Drops  

- **Schwierigkeitskurve**:
  - Gegner werden nur stärker, wenn ein Boss besiegt wurde (globale Buffs)  
  - Kein Auto-Heal zwischen Wellen → nur Mana wird regeneriert  
  - Alle 10 Wellen zusätzliche Gegner-Buffs für härtere Kämpfe  

- **Inventar & Items**:
  - Passive Items wirken automatisch (stackend)  
  - Heiltränke als Verbrauchsgegenstand (Start: 3 Stück, im Shop nachkaufbar)  
  - Inventar lässt sich jederzeit einsehen, ohne den Zug zu verbrauchen  

- **Run-Tracking & Leaderboard**:
  - Jeder Run wird gespeichert (`data/runs.jsonl`)  
  - Leaderboard nach Kills, **gesamtem gesammelten Gold**, Level oder Klasse sortierbar  
  - Bereits beim Klassenauswahl-Screen kann das Leaderboard eingesehen werden  

---

## ▶️ Starten

1. **Repo klonen / Dateien bereitstellen**
```sh
   git clone <repo-url>
   cd <repo>
   ```
2. **Python 10.3+ installieren**

  - keine externen Libraries nötig - nur Standardbibliothek

3. **Spiel starten**
  ```sh
   python main.py
   ```

## 🧑‍💻 Steuerung (Konsole)

- Eingaben über Nummern-Menüs (`1`, `2` …)
- **Im Kampf:**
  - Normaler Angriff
  - Skills einsetzen
  - Heiltrank benutzen
  - Inventar ansehen (verbraucht keinen Zug)
- **Im Shop:**
  - Items kaufen (stacken automatisch)
  - Heiltränke nachkaufen
  - Inventar prüfen

---

## 🏆 Leaderboard

Nach jedem Run wird ein Datensatz gespeichert:

- 👤 Spielername  
- 🏷️ Klasse  
- 💰 **Gesamtes Gold** im Run  
- 🎯 Level  
- ☠️ Kills  
- 📅 Datum

## 🌳 Skilltree – Übersicht

### 🧾 Generisch (für alle Klassen verfügbar)
- **Level 2**
  - ⚔️ *Klingenhieb I* – +2 ATK  
  - 🛡️ *Zähigkeit I* – +10 HP, +3% Armor  
  - 🧪 *Alchemist I* – Heiltränke +20% wirksamer  
- **Level 6**
  - ⚔️ *Klingenhieb II* – +3 ATK *(requires Klingenhieb I)*  
  - 🛡️ *Zähigkeit II* – +10 HP, +2 DEF *(requires Zähigkeit I)*  
  - 📖 *Taktiker* – +5 Mana, +10% Spellpower *(requires Alchemist I)*  
- **Level 10**
  - ⚔️ *Klingenhieb III* – +4 ATK *(requires Klingenhieb II)*  
  - 🛡️ *Zähigkeit III* – +15 HP, +1 DEF *(requires Zähigkeit II)*  
  - 🧪 *Alchemist II* – Heiltränke +20% wirksamer *(requires Taktiker)*  
- **Level 12**
  - 🎯 *Präzision* – +4% Crit  
  - 💨 *Ausweichrolle* – +4% Dodge  
  - 🛡️ *Schutzkunde* – +3% Armor  
- **Level 15**
  - ⚔️ *Waffenkunde* – +3 ATK, +3% Crit  
  - 🛡️ *Kampferprobt* – +20 HP, +1 DEF  
  - 🔮 *Mystischer Fokus* – +6 Mana, +12% Spellpower  

---

### 🛡️ Tank
- **Level 4**
  - *Steinhaut* – +10% Armor  
  - *Vitalität* – +20 HP  
- **Level 6**
  - *Eiserner Wille* – +1 DEF, +5% Armor  
  - *Unbeugsam* – +15 HP, +5% Healpower  
- **Level 8**
  - *Wächter* – +2 DEF, +10% Healpower  
- **Level 10**
  - *Bollwerk* – +30 HP, +2 DEF  
  - *Gehärtete Platte* – +6% Armor  
- **Level 12**
  - *Unerschütterlich* – +7% Armor, +10 HP  
  - 🌟 *Ultimate: Unzerstörbar* – Heilt 40% HP, setzt Armor auf 80% (1× pro Kampf)  

---

### 🗡️ Assassin
- **Level 4**
  - *Kritische Präzision* – +7% Crit  
  - *Schattenbewegung* – +7% Dodge  
- **Level 6**
  - *Tödlicher Fokus* – +8% Crit *(requires Kritische Präzision)*  
  - *Leichtfüßig* – +8% Dodge *(requires Schattenbewegung)*  
- **Level 8**
  - *Durchdringender Schlag* – Fähigkeit: Ignoriert 25% DEF  
- **Level 10**
  - *Hinterhalt* – +4 ATK, +5% Crit  
  - *Schattentanz* – +6% Dodge, +2% Armor  
- **Level 12**
  - *Assassinenlist* – +3 ATK, +4% Crit, +3% Dodge  
  - 🌟 *Ultimate: Tödlicher Schlag* – Garantierter Crit +50% Bonusdmg (1× pro Kampf)  

---

### 🔮 Mage
- **Level 4**
  - *Arkaner Fokus* – +30% Spellpower, +5 Mana  
- **Level 6**
  - *Essenzanzapfung* – +8 Mana, +15% Spellpower  
  - *Schutzrunen* – +3% Armor, +5 HP  
- **Level 8**
  - *Manaschild* – +5% Armor, +10 HP  
- **Level 10**
  - *Gestärkte Zauber* – +25% Spellpower  
  - *Arkaner Fluss* – +6 Mana, +4% Crit  
- **Level 12**
  - *Arkane Meisterschaft* – +10 Mana, +20% Spellpower  
  - 🌟 *Ultimate: Arkaner Sturm* – Massiver Magieschaden, ignoriert DEF/Armor (1× pro Kampf)  

---

### 🧛 Vampire
- **Level 4**
  - *Lebensraub* – Deine Angriffe heilen dich um 10% des verursachten Schadens
  - *Blutdurst* – +6% Crit
- **Level 6**
  - *Blutexplosion* – Fähigkeit: Starker Angriff, Schaden steigt mit fehlender HP
  - *Schattenhaut* – +8% Dodge
- **Level 8**
  - *Blutschild* – Fähigkeit: Schild absorbiert 25% des nächsten erlittenen Schadens
- **Level 10**
  - *Nachtgestalt* – +5% Crit, +5% Dodge
  - *Dunkles Geschenk* – +3 ATK, +3% Crit
- **Level 12**
  - *Blutmeister* – +4 ATK, +5% Crit, +4% Dodge
  - 🌟 *Ultimate: Blutritual* – Einmal pro Kampf: Sofortige Heilung auf 50% HP, +25% Crit für diese Runde

---

### ⚔️ Knight
- **Level 4**
  - *Ausgewogenheit I* – +1 ATK, +1 DEF, +10 HP  
- **Level 6**
  - *Vielseitigkeit* – +2 ATK, +2 DEF  
  - *Schildausbildung* – +3% Armor, +5 HP  
- **Level 8**
  - *Kampfhaltung* – +3% Crit, +3% Armor  
- **Level 10**
  - *Taktiker* – +4% Crit, +4% Dodge  
  - *Geschärfte Klinge* – +3 ATK  
- **Level 12**
  - *Feldherr* – +20 HP, +4% Armor  
  - 🌟 *Ultimate: Heldenmut* – +20 ATK, +10 DEF Buff bis Kampelende (1× pro Kampf)  
