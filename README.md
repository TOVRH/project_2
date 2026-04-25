#  Task Manager (Python + MySQL)

Jednoduchý program pro správu úkolů napsaný v Pythonu s využitím MySQL databáze. Součástí projektu jsou automatické testy pomocí pytest.

---

##  Funkce

- Přidání úkolu (název a popis jsou povinné)
- Zobrazení úkolů (zobrazí pouze úkoly ve stavu `nezahájeno` nebo `probíhá`)
- Aktualizace stavu úkolu (umožnuje změnit stav úkolů na `probíhá` nebo `hotovo`)
- Odstranění úkolu (umožňuje smazat libovolný úkol z databáze)

---

##  Struktura projektu

src/task_manager.py  
tests/  
.env  
.env.test  
README.md  
requirements.txt

---

##  Požadavky

- Python 3.13.7
- MySQL

## Instalace

- Naklonujte repozitář nebo stáhněte projekt

- Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```  

---

##  Konfigurace  

## ⚙️ Konfigurace

Vytvoření databází v MySQL (spusťte před prvním spuštěním aplikace):

```SQL
CREATE DATABASE task_manager;
CREATE DATABASE tests_task_manager;  
```

.env 
``` 
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=1111
DB_NAME=task_manager
```  

.env.test
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=1111
DB_NAME=tests_task_manager
```  

##  Spuštění aplikace

python src/task_manager.py

---

##  Testování

Spuštění testů:

pytest

Testy obsahují:
- pozitivní scénáře (správné fungování)
- negativní scénáře (chybný vstup)

Použité nástroje:
- pytest fixtures (testovací databáze)
- unittest.mock (simulace vstupu)
- capsys (zachycení výstupu)

Testy používají samostatnou databázi a po každém testu se provádí TRUNCATE TABLE ukoly

---

##  Databáze

Tabulka `ukoly` obsahuje:
- id – primární klíč  
- nazev – název úkolu  
- popis – popis  
- stav – (nezahájeno, probíhá, hotovo)  
- datum_vytvoreni – přidá se automaticky

---

##  Poznámky

- Aplikace běží v terminálu
- Vyžaduje běžící MySQL server
- Testy používají oddělenou databázi