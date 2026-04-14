def hlavni_menu() -> str:
    """
    Zobrazí hlavní menu a vrátí zvolenou možnost uživatele.

    Returns:
        str: Zvolená možnost (1-4).
    """
    while True:
        print("\nSprávce úkolů - hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Odstranit úkol")
        print("4. Konec programu")

        volba = input("Vyberte možnost (1-4): ").strip()

        if volba in ("1", "2", "3", "4"):
            return volba
        else:
            print("Neplatná volba, zkuste to prosím znovu.")

def pridat_ukol(ukoly: list[dict[str, str]]) -> None:
    """
    Přidá nový úkol do seznamu úkolů.
    Uživatel zadá název a popis úkolu.
    """
    while True:
        nazev = input("Zadejte název úkolu: ").strip()
        if nazev == "":
            print("Název úkolu nesmí být prázdný.")
        else:
            break
    while True:
        popis = input("Zadejte popis úkolu: ").strip()
        if popis == "":
            print("Popis úkolu nesmí být prázdný.")
        else:
            break

    ukol: dict[str, str] = {
        "nazev": nazev,
        "popis": popis
    }
    ukoly.append(ukol)

    print(f"Úkol '{nazev}' byl přidán.")

def zobrazit_ukoly(ukoly: list[dict[str, str]]) -> None:
    """
    Zobrazí všechny úkoly v seznamu.
    Pokud je seznam prázdný, informuje uživatele.
    """
    if not ukoly:
        print("\nSeznam úkolů je prázdný.")
        return
    print("\nSeznam úkolů:")

    for index, ukol in enumerate(ukoly, start=1):
        print(f"{index}. {ukol['nazev']} - {ukol['popis']}")

def odstranit_ukol(ukoly: list[dict[str, str]]) -> None:
    """
    Odstraní vybraný úkol ze seznamu.
    Uživatel zadá číslo úkolu, který chce odstranit.
    """
    if not ukoly:
        print("\nSeznam úkolů je prázdný.")
        return

    zobrazit_ukoly(ukoly)

    while True:
        try:
            volba = int(input("\nZadejte číslo úkolu, který chcete odstranit: "))

            if 1 <= volba <= len(ukoly):
                odstraneny = ukoly.pop(volba - 1)
                print(f"Úkol '{odstraneny['nazev']}' byl odstraněn.")
                break
            else:
                print("Zadané číslo úkolu neexistuje, zkuste to znovu.")

        except ValueError:
            print("Zadejte platné číslo.")

def main() -> None:
    """
    Hlavní funkce programu, která řídí chod aplikace.
    """
    ukoly: list[dict[str, str]] = []
    
    while True:
        volba = hlavni_menu()

        if volba == "1":
            pridat_ukol(ukoly)
        elif volba == "2":
            zobrazit_ukoly(ukoly)
        elif volba == "3":
            odstranit_ukol(ukoly)
        elif volba == "4":
            print("Konec programu.")
            break

if __name__ == "__main__":
    main()