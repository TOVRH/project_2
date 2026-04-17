import pytest
from src.task_manager import pridat_ukol
from unittest.mock import patch

@pytest.mark.positive
def test_pridat_ukol_novy(test_db_pripojeni):
    # Simulujeme platný vstup uživatele
    with patch('builtins.input', side_effect=['Úkol 1', 'Popis 1']):
        pridat_ukol(test_db_pripojeni)

    # Ověřujeme, že úkol byl přidán po zadání platného vstupu
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ukoly")
        count = cursor.fetchone()[0]
    
    assert count == 1

@pytest.mark.negative
def test_pridat_ukol_prazdny_nazev(test_db_pripojeni, capsys):
    # Simulujeme vstup uživatele: prázdný název, poté platný název a popis
    with patch('builtins.input', side_effect=['', 'Úkol 1', 'Popis 1']):
        pridat_ukol(test_db_pripojeni)

    # Ověřujeme, že se zobrazila chybová zpráva pro prázdný název
    captured = capsys.readouterr()
    assert "Název úkolu nesmí být prázdný." in captured.out

    # Ověřujeme, že úkol byl přidán až po zadání platného názvu
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ukoly")
        count = cursor.fetchone()[0]
    assert count == 1