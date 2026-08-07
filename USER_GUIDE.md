# Felhasználói Kézikönyv (User Guide)

## Rendszerkövetelmények
A projekt futtatásához kizárólag a **Docker** és a **Docker Compose** megléte szükséges. Semmilyen lokális Python vagy adatbázis telepítés nem kell.

## Futtatás lépései
1. Nyiss egy terminált a projekt gyökerében (ahol a `docker-compose.yml` fájl található).
2. Add ki az alábbi parancsot:
   `docker-compose up --build`
3. Várj néhány másodpercet, amíg a PostgreSQL adatbázis és a FastAPI szerver elindul. A rendszer automatikusan feltölti az adatbázist 30 darab teszt parkolóhellyel.

## A Rendszer Használata (Swagger UI)
A backend API legkönnyebben a beépített, interaktív grafikus felületen tesztelhető.
Nyisd meg a böngésződben az alábbi címet:
👉 **http://127.0.0.1:8000/docs**

Itt megtalálod az összes elérhető végpontot (GET, POST, DELETE). A "Try it out" gombra kattintva azonnal küldhetsz teszt kéréseket, és láthatod a szerver JSON válaszait.

## Leállítás
A szerver leállításához a terminálban nyomd meg a `CTRL + C` billentyűkombinációt, majd a konténerek eltávolításához (opcionális) futtasd a `docker-compose down` parancsot.