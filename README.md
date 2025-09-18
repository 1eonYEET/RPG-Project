# ⚔️ Console RPG – Turn-Based Adventure in Python

Ein kleines **konsolenbasiertes RPG** in Python, das bewusst nach **SOLID-Prinzipien** entworfen ist.

---

## 🎮 Features

- **4 Klassen** zur Auswahl:
  - 🛡️ Tank – viel Leben, viel Rüstung, weniger Schaden  
  - 🗡️ Assassin – hoher Schaden, Crit & Dodge, wenig Leben  
  - 🔮 Mage – mehr Mana, mächtige Zauber  
  - ⚔️ Knight – ausgewogener Allrounder  

- **Kampfsystem**:
  - Rundenbasiert mit Skills & Heiltränken  
  - Gegner können kritisch treffen oder ausweichen  
  - Bosse mit Portraits & Drops alle 5 Wellen  

- **Progression**:
  - XP & Level-Ups  
  - **Skilltree** mit passiven Boni und neuen Fähigkeiten (Vorher→Nachher-Vorschau)  
  - Items & Ausrüstung im **Shop** (stackende Effekte, Vorher→Nachher-Vorschau)  
  - Gold-Belohnungen + Boss-Drops  

- **Schwierigkeitskurve**:
  - Gegner werden nur stärker, wenn ein Boss besiegt wurde (globale Buffs)  
  - Kein Auto-Heal zwischen Wellen → nur Mana wird regeneriert  

- **Inventar & Items**:
  - Passive Items wirken automatisch (stackend)  
  - Heiltränke als Verbrauchsgegenstand (Start: 3 Stück, im Shop nachkaufbar)  

- **Run-Tracking & Leaderboard**:
  - Jeder Run wird gespeichert (`data/runs.jsonl`)  
  - Leaderboard nach Kills, Gold, Level oder Klasse sortierbar 
