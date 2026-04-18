import pytest
from src.task_manager import aktualizovat_ukol
from unittest.mock import patch

@pytest.mark.positive
def test_aktualizovat_ukol(test_db_pripojeni, priprav_test_data):
    """
    Ověří, že se úkol správně aktualizuje na stav 'probíhá'
    """

    # ID = 1, stav = probíhá
    with patch('builtins.input', side_effect=['1', '1']):
        aktualizovat_ukol(test_db_pripojeni)

    # Ověříme změnu v DB
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("SELECT stav FROM ukoly WHERE id = 1")
        stav = cursor.fetchone()[0]

    assert stav == "probíhá"

@pytest.mark.negative
def test_aktualizovat_ukol_neciselne_id(test_db_pripojeni, capsys):
    """
    Ověří reakci programu na nečíselné ID
    """
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute(
            "INSERT INTO ukoly (nazev, popis) VALUES ('Test', 'Popis')"
        )
        test_db_pripojeni.commit()
    # 'abc' = neplatné ID -> program musí vypsat chybu a pokračovat
    with patch('builtins.input', side_effect=['abc', '1', '1']):
        aktualizovat_ukol(test_db_pripojeni)

    captured = capsys.readouterr()

    assert "Zadejte platné číslo." in captured.out
