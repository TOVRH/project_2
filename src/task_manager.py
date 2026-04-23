import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv(".env")


@contextmanager
def cursor_manager(pripojeni):
    """
    Spravuje databázový kurzor pomocí context manageru.

    Automaticky otevře a zavře kurzor po použití.
    """
    cursor = pripojeni.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def pripojeni_db():
    """
    Připojí se k MySQL databázi.

    Returns:
        connection nebo None: Připojení k databázi nebo None při chybě.
    """
    try:
        pripojeni = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
)
        
        print("Připojeno k databázi.")
        return pripojeni
    except Error as e:
        print(f"Chyba při připojování k databázi: {e}")
        return None


def vytvoreni_tabulky(pripojeni):
    """
    Vytvoří tabulku ukoly, pokud neexistuje.

    Args:
        pripojeni: Aktivní databázové připojení.
    """
    try:
        with cursor_manager(pripojeni) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ukoly (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nazev VARCHAR(50) NOT NULL,
                    popis VARCHAR(255) NOT NULL,
                    stav ENUM('nezahájeno', 'hotovo', 'probíhá') DEFAULT 'nezahájeno',
                    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        print("Tabulka 'ukoly' je připravena.")
    
    except Error as e:
        print(f"Chyba při vytváření tabulky: {e}")


def hlavni_menu() -> str:
    """
    Zobrazí hlavní menu a vrátí zvolenou možnost uživatele.

    Returns:
        str: Zvolená možnost (1-5).
    """
    while True:
        print("\nSprávce úkolů - hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Konec programu")

        volba = input("Vyberte možnost (1-5): ").strip()

        if volba in ("1", "2", "3", "4", "5"):
            return volba
        else:
            print("Neplatná volba, zkuste to prosím znovu.")


def pridat_ukol(pripojeni):
    if not pripojeni:
        print("Chyba: Nepodařilo se připojit k databázi.")
        return None

    while True:
        nazev = input("Zadejte název úkolu: ").strip()
        if not nazev:
            print("Název úkolu nesmí být prázdný.")
        else:
            break

    while True:
        popis = input("Zadejte popis úkolu: ").strip()
        if not popis:
            print("Popis úkolu nesmí být prázdný.")
        else:
            break

    try:
        with cursor_manager(pripojeni) as cursor:
            cursor.execute(
                "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
                (nazev, popis)
            )
            pripojeni.commit()

            ukol_id = cursor.lastrowid
            print(f"Úkol '{nazev}' byl přidán (ID {ukol_id}).")

            return ukol_id

    except Error as e:
        print(f"Chyba při přidávání úkolu: {e}")
        return None


def zobrazit_ukoly(pripojeni, jen_aktivni = True):
    """
    jen_aktivní = True: zobrazí jen 'nezahájeno' a 'probíhá'

    jen_aktivní = False: Zobrazí všechny úkoly (pro mazání)

    Pokud nejsou žádné úkoly, informuje uživatele.
    """
    if not pripojeni:
        print("Chyba: Nepodařilo se připojit k databázi.")
        return

    try:
        with cursor_manager(pripojeni) as cursor:
            if jen_aktivni:
                cursor.execute("SELECT * FROM ukoly WHERE stav IN('nezahájeno', 'probíhá')")
            else:
                cursor.execute("SELECT * FROM ukoly")
            ukoly = cursor.fetchall()

        if not ukoly:
            print("\nSeznam úkolů je prázdný.")
            return

        print("\nSeznam úkolů:")
        for ukol in ukoly:
            print(f"{ukol[0]}. {ukol[1]} - {ukol[2]} (Stav: {ukol[3]})")

    except Error as e:
        print(f"Chyba při zobrazení úkolů: {e}")


def aktualizovat_ukol(pripojeni):
    """
    Aktualizuje stav existujícího úkolu.

    Uživatel:
    - vidí seznam úkolů,
    - vybírá ID (dokud nezadá existující),
    - vybírá nový stav pomocí nabídky (probíhá / hotovo).
    """
    if not pripojeni:
        print("Chyba: Nepodařilo se připojit k databázi.")
        return

    zobrazit_ukoly(pripojeni)

    try:
        with cursor_manager(pripojeni) as cursor:

            # výběr validního ID
            while True:
                try:
                    id_ukolu = int(input("\nZadejte ID úkolu, který chcete aktualizovat: "))

                    cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
                    if cursor.fetchone():
                        break
                    else:
                        print("Zadané ID neexistuje, zkuste to znovu.")

                except ValueError:
                    print("Zadejte platné číslo.")

            
            # výběr nového stavu (uživatelské menu)
            while True:
                print("\nVyberte nový stav:")
                print("1. probíhá")
                print("2. hotovo")

                volba = input("Zadejte volbu (1-2): ").strip()

                if volba == "1":
                    novy_stav = "probíhá"
                    break
                elif volba == "2":
                    novy_stav = "hotovo"
                    break
                else:
                    print("Neplatná volba, zkuste to znovu.")

            # update v DB
            cursor.execute(
                "UPDATE ukoly SET stav = %s WHERE id = %s",
                (novy_stav, id_ukolu)
            )
            pripojeni.commit()

            print(f"Úkol s ID {id_ukolu} byl aktualizován na stav '{novy_stav}'.")

    except Error as e:
        print(f"Chyba při aktualizaci úkolu: {e}")
        

def odstranit_ukol(pripojeni):
    """
    Odstraní úkol z databáze podle jeho ID.

    Uživatel zadá ID úkolu, který chce odstranit.
    """
    if not pripojeni:
        print("Chyba: Nepodařilo se připojit k databázi.")
        return

    zobrazit_ukoly(pripojeni, jen_aktivni= False)

    try:
        with cursor_manager(pripojeni) as cursor:

            # OPAKOVÁNÍ DOKUD NENÍ ZADÁNO EXISTUJÍCÍ ID
            while True:
                try:
                    id_ukolu = int(input("\nZadejte ID úkolu, který chcete odstranit: "))

                    cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
                    existuje = cursor.fetchone()

                    if existuje:
                        break
                    else:
                        print("Zadané ID neexistuje, zkuste to znovu.")

                except ValueError:
                    print("Zadejte platné číslo.")

            # odstranění úkolu
            cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
            pripojeni.commit()

            print(f"Úkol s ID {id_ukolu} byl odstraněn.")

    except Error as e:
        print(f"Chyba při odstraňování úkolu: {e}")


def main() -> None:
    """
    Hlavní funkce programu, která řídí celý chod aplikace.
    """
    pripojeni = pripojeni_db()

    if pripojeni:
        vytvoreni_tabulky(pripojeni)

    while True:
        volba = hlavni_menu()

        if volba == "1":
            pridat_ukol(pripojeni)
        elif volba == "2":
            zobrazit_ukoly(pripojeni)
        elif volba == "3":
            aktualizovat_ukol(pripojeni)
        elif volba == "4":
            odstranit_ukol(pripojeni)
        elif volba == "5":
            print("Konec programu.")
            break

    if pripojeni:
        pripojeni.close()


if __name__ == "__main__":
    main()