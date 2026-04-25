import pytest
from src.task_manager import odstranit_ukol
from unittest.mock import patch

@pytest.mark.positive
def test_odstranit_ukol(test_db_pripojeni, priprav_test_data):
    """
    Ověří, že je úkol správně odstraněný z databáze
    """

    # získáme skutečné ID
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Úkol 1'")
        realne_id = cursor.fetchone()[0]

    # odstranění
    with patch('builtins.input', side_effect=[str(realne_id)]):
        odstranit_ukol(test_db_pripojeni)

    # Ověříme, že úkol zmizel
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ukoly WHERE id = %s", (realne_id,))
        count = cursor.fetchone()[0]

    assert count == 0

@pytest.mark.negative
def test_odstranit_ukol_neexistujici_id(test_db_pripojeni, priprav_test_data, capsys):
    """
    Ověří reakci programu na neexistující ID
    """
    # Získáme reálné ID, aby bylo možné test správně dokončit
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly ORDER BY id LIMIT 1")
        realne_id = cursor.fetchone()[0]
    
    # 999 → neexistuje -> poté správné ID
    with patch('builtins.input', side_effect=['999', str(realne_id)]):
        odstranit_ukol(test_db_pripojeni)

    # Ověříme hlášku
    captured = capsys.readouterr()
    assert "Zadané ID neexistuje" in captured.out