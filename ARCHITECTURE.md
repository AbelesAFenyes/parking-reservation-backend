# Rendszerterv (Architecture)

## Technológiai Stack
* **Nyelv:** Python 3.10+
* **Keretrendszer:** FastAPI (Gyors, aszinkron, beépített OpenAPI támogatással)
* **Adatbázis:** PostgreSQL (Relációs, ACID-konform tranzakciókezeléssel az átfedések elkerülése végett)
* **ORM:** SQLAlchemy (Adatbázis absztrakció)
* **Validáció:** Pydantic V2 (Szigorú adatellenőrzés és típusbiztonság)
* **Tesztelés:** Pytest (Unit és Integrációs tesztek)
* **Konténerizáció:** Docker & Docker Compose

## Komponens Architektúra
A kódbázis modulárisan, a felelősségi körök szigorú szétválasztásával (Separation of Concerns) épül fel:
1. `app/api/`: Csak a HTTP kérések fogadásáért (Routing) és a válaszok formázásáért felel.
2. `app/services/`: Itt található a "Brain", azaz az üzleti logika (pl. időpontok átfedésének matematikai vizsgálata és a jogosultságok ellenőrzése).
3. `app/models/`: Az adatbázis táblák (Entities) reprezentációja SQLAlchemy segítségével.
4. `app/schemas/`: A Pydantic DTO (Data Transfer Object) osztályok, amelyek a validációt végzik mielőtt az adat a logikába érne.
5. `app/db/`: Az adatbázis kapcsolatért és a kezdeti tesztadatok idempotens feltöltéséért (Seeding) felelős komponensek.

## Teljesítmény és Bug-mentesség Megfontolások
* **Tranzakciókezelés:** A relációs adatbázis (PostgreSQL) és a szigorú lekérdezési feltételek használata megakadályozza a race-condition bugokat, így két azonos pillanatban beérkező kérés nem tudja ugyanazt a helyet lefoglalni.
* **Típusbiztonság:** A FastAPI és a Pydantic automatikusan kiszűri a rossz formátumú (pl. hiányzó mezők, rossz dátumformátum) kéréseket, még mielőtt azok az adatbázis rétegig eljutnának.
* **Automatikus Tesztelés:** A rendszer rendelkezik integrációs tesztekkel (`pytest`), amelyek a legkritikusabb edge-case forgatókönyveket (pl. időpont-átfedések, hibás járműtípus) automatizáltan vizsgálják.