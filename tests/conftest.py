import pytest
import mysql.connector
from mysql.connector import Error
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(".env.test")

# Přidáme cestu k adresáři src
sys.path.append(str(Path(__file__).parent.parent))

def pytest_configure(config):
    """
    Definuje vlastní pytest markery pro rozlišení testů.
    """

    config.addinivalue_line(
        "markers",
        "positive: označí testy jako pozitivní"
    )
    config.addinivalue_line(
        "markers",
        "negative: označí testy jako negativní"
    )

@pytest.fixture
def test_db_pripojeni():
    """
    Vytvoří připojení k testovací databázi a připraví tabulku.

    Po testu automaticky smaže data a uzavře připojení.
    """

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
)
    

    with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ukoly (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nazev VARCHAR(50) NOT NULL,
                    popis VARCHAR(255) NOT NULL,
                    stav ENUM('nezahájeno', 'hotovo', 'probíhá') DEFAULT 'nezahájeno',
                    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()

    yield connection

    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE ukoly")
        connection.commit()

    connection.close()

@pytest.fixture
def priprav_test_data(test_db_pripojeni):
    """
    Vloží základní testovací data pro testy,
    které potřebují existující záznamy v databázi.
    """
    with test_db_pripojeni.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ukoly (nazev, popis, stav)
            VALUES
                ('Úkol 1', 'Popis 1', 'nezahájeno'),
                ('Úkol 2', 'Popis 2', 'probíhá')
        """)
    test_db_pripojeni.commit()

    yield