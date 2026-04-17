import pytest
from src.task_manager import aktualizovat_ukol
from unittest.mock import patch

@pytest.mark.negative
def test_aktualizovat_neexistujici_ukol(pripojeni_db):
    with pripojeni_db.cursor() as cursor:
        with pytest.raises(Error):  # Očekáváme chybu
            cursor.execute("UPDATE ukoly SET stav = 'hotovo' WHERE id = 9999")  # Neexistující ID
        pripojeni_db.rollback()