import pytest
from src.task_manager import pridat_ukol
from unittest.mock import patch

@pytest.mark.positive
def test_pridat_ukol_novy(test_db_pripojeni):
    """
    Ověří, že se nový úkol uloží do databáze
    """
    with patch('builtins.input', side_effect=['Úkol 1', 'Popis 1']):
        pridat_ukol(test_db_pripojeni)

    # Ověřujeme, že úkol byl přidán po zadání platného vstupu
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ukoly")
        count = cursor.fetchone()[0]
    
    assert count == 1

@pytest.mark.negative
def test_pridat_ukol_prazdny_nazev(test_db_pripojeni, capsys):
    """
    Ověří, že systém odmítne prázdný název úkolu
    """

    # nejdřív prázdný vstup, potom správný 
    with patch('builtins.input', side_effect=['', 'Úkol 1', 'Popis 1']):
        pridat_ukol(test_db_pripojeni)

    captured = capsys.readouterr()
    assert "Název úkolu nesmí být prázdný." in captured.out