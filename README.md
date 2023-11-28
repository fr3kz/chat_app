# chat_app [Developing]

Aplikacja backendowa do prostego czatu, napisana w Django, Django Rest Framework i Django Channels. Umożliwia użytkownikom tworzenie kont, logowanie, wybieranie kanałów, pisanie wiadomości tekstowych, wysyłanie zdjęć, filmów oraz dodawanie znajomych.

## Wymagania

- Python 3.x
- Django
- Django Rest Framework
- Django Channels

## API

### Logowanie
- **Endpoint:** `/users/login/`
- **Metoda:** `POST`
- Używane do logowania użytkowników.
- Przykładowe ciało żądania (w formie JSON):

   ```json
   {
     "username": "example_user",
     "password": "example_password"
   }

### Rejestrowanie
- **Endpoint:** `/users/register/`
- **Metoda:** `POST`
- Używane do rejestrowania użytkowników.
- Przykładowe ciało żądania (w formie JSON):

   ```json
   {
     "username": "example_user",
     "password": "example_password"
   }

### Pobranie kodu CSRF
- **Endpoint:** `/users/csrf/`
- **Metoda:** `GET`
- Używane do pobierania kodu CSRF dla zabezpieczenia żądań HTTP.

### Utworzenie lobby chatu
- **Endpoint:** `/create/`
- **Metoda:** `POST`
- Używane do tworzenia nowych lobby chatu.
- Przykładowe ciało żądania (w formie JSON):

   ```json
   {
     "title": "Nowe Lobby"
   }
### WebSocket Chat
- **Endpoint:** `ws://127.0.0.1:8000/ws/chat/<int:lobby_id>/<int:user_id>/`
- Używane do interakcji w czasie rzeczywistym w ramach chatu.
- Wiadomości przesyłane w formie JSON z atrybutami:

   ```json
   {
     
     "message": "Tresc wiadomosci"
   }
   
