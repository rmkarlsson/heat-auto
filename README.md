# IndoorTempCtrl – AppDaemon Heating Controller

## 🔧 Översikt
IndoorTempCtrl är ett AppDaemon‑baserat styrsystem för vattenburen värme.  
Systemet beräknar önskad framledningstemperatur baserat på utomhustemperatur och styr en shuntmotor via två reläutgångar (upp/ner).

Systemet består av tre huvudkomponenter:

1. **HeatingCurve** – omvandlar utetemperatur → målfamledningstemperatur via tabell + interpolation  
2. **Shunt** – styr shuntmotor via två reläer, med spärr på max 75 steg i samma riktning  
3. **IndoorTempCtrl** – AppDaemon‑appen som kopplar ihop allt och kör styrlogiken varje sekund  

Projektet är byggt för att vara:
- deterministiskt  
- lätt att testa  
- modulärt  
- robust mot sensorfel  
- enkelt att vidareutveckla  

---

## 📁 Filstruktur
