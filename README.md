# ⚔️ Console RPG – Turn-Based Adventure in Python

Ein kleines **konsolenbasiertes RPG** in Python, das bewusst nach **SOLID-Prinzipien** entworfen ist.

---

## 🎮 Features

- **4 Klassen** zur Auswahl:
  - 🛡️ **Tank** – viel Leben, viel Rüstung, weniger Schaden, besseres Heilen  
  - 🗡️ **Assassin** – hoher Schaden, Crit & Dodge, wenig Leben  
  - 🔮 **Mage** – mehr Mana, mächtige Zauber  
  - ⚔️ **Knight** – ausgewogener Allrounder  

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
   git clone <repo-url>
   cd <repo>
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