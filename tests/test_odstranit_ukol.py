import pytest
from src.task_manager import odstranit_ukol
from unittest.mock import patch

@pytest.mark.positive
def test_odstranit_ukol(test_db_pripojeni, priprav_test_data):
    """
    Ověří, že je úkol správně odstraněný z databáze
    """

    # ID = 1 -> smazání úkolu
    with patch('builtins.input', side_effect=['1']):
        odstranit_ukol(test_db_pripojeni)

    # Ověříme, že úkol zmizel
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ukoly WHERE id = 1")
        count = cursor.fetchone()[0]

    assert count == 0

@pytest.mark.negative
def test_odstranit_ukol_neexistujici_id(test_db_pripojeni, priprav_test_data, capsys):
    """
    Ověří reakci programu na neexistující ID
    """

    # 999 → neexistuje -> poté správné ID
    with patch('builtins.input', side_effect=['999', '1']):
        odstranit_ukol(test_db_pripojeni)

    # Ověříme hlášku
    captured = capsys.readouterr()
    assert "Zadané ID neexistuje" in captured.out