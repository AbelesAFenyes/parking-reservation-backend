# API Leírás

A rendszer teljes, interaktív és naprakész OpenAPI (Swagger) dokumentációval rendelkezik, amelyet a FastAPI automatikusan generál. 

Az alkalmazás elindítása után az API teljes specifikációja, a modellek felépítése és a hibakódok (HTTP 400, 404, 409) részletes leírása az alábbi URL-en érhető el:
**http://127.0.0.1:8000/docs**

## Főbb Végpontok (Endpoints)

### Parkolóhelyek (Parking Spots)
* `GET /api/v1/spots`: Lekérdezi az összes létező parkolóhelyet és azok típusát (Regular, Electric, Disabled).
* `GET /api/v1/spots/{spot_id}/reservations`: Lekérdezi egy adott parkolóhelyhez tartozó összes aktív foglalást.

### Foglalások (Reservations)
* `POST /api/v1/reservations`: Új foglalás létrehozása. Elvárja a gépjármű rendszámát, a kezdő és végdátumot, valamint a jogosultságokat (elektromos/mozgáskorlátozott). Átfedés esetén `409 Conflict` hibát dob.
* `DELETE /api/v1/reservations/{reservation_id}`: Egy meglévő foglalás azonnali törlése/lemondása (`204 No Content` státuszkóddal tér vissza sikeres esetben).