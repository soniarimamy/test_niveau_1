import time
import requests
from django.utils import timezone
from api_app.models import Test1Result
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Automatise le test en appelant l'API externe (register, login, create, confirm)."

    def handle(self, *args, **options):
        BASE_URL = "https://hire-game.pertimm.dev"
        REGISTER_URL = f"{BASE_URL}/api/v1.1/auth/register/"
        LOGIN_URL = f"{BASE_URL}/api/v1.1/auth/login/"
        JOB_APPLICATION_URL = f"{BASE_URL}/api/v1.1/job-application-request/"

        email = "rochel.soniarimamy@gmail.com"
        password = "abc123"
        first_name = "Rochel"
        last_name = "Soniarimamy"

        logs = []
        logs.append(f"Début du test à {timezone.now().isoformat()}")

        test_start = time.time()

        try:
            # 1) Register
            r = requests.post(REGISTER_URL, json={
                "email": email,
                "password1": password,
                "password2": password,
                "url_format": "http://example.com",
                "email_format": "test@example.com"
            }, timeout=5)
            if r.status_code in (200, 201):
                logs.append("Register OK")
            elif r.status_code == 400 and "already exists" in r.text.lower():
                logs.append("Utilisateur déjà existant, passage au login")
            else:
                logs.append(f"Register : code {r.status_code} - {r.text[:200]}")

            # 2) Login
            r = requests.post(LOGIN_URL, json={"email": email, "password": password}, timeout=5)
            if r.status_code != 200:
                logs.append(f"Login failed : {r.status_code} - {r.text[:200]}")
                self._save_result(email, "FAILED", logs)
                return

            token = r.json().get("token")
            if not token:
                logs.append("Login : token absent dans la réponse")
                self._save_result(email, "FAILED", logs)
                return

            headers = {"Authorization": f"Token {token}"}
            logs.append(f"Login OK, token obtenu : {token[:8]}...")

            # 3) Create job application
            payload = {"email": email, "first_name": first_name, "last_name": last_name}
            r = requests.post(JOB_APPLICATION_URL, json=payload, headers=headers, timeout=5)
            if r.status_code not in (200, 201):
                logs.append(f"Create application failed : {r.status_code} - {r.text[:200]}")
                self._save_result(email, "FAILED", logs)
                return

            app = r.json()
            app_url = app.get("url")
            confirmation_url = app.get("confirmation_url")
            if not app_url:
                logs.append("Create response: 'url' absent")
                self._save_result(email, "FAILED", logs)
                return
            logs.append(f"Application créée : {app_url}")

            # 4) Poll until COMPLETED
            while True:
                elapsed = time.time() - test_start
                if elapsed >= 30:
                    logs.append("Dépassement du délai 30s : statut non COMPLETED")
                    self._save_result(email, "TIMEOUT", logs)
                    return

                r = requests.get(app_url, headers=headers, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    status = data.get("status")
                    logs.append(f"Statut: {status} (t={int(elapsed)}s)")
                    if status == "COMPLETED":
                        confirmation_url = confirmation_url or app_url
                        logs.append("Status COMPLETED, confirmation_url définie")
                        break
                else:
                    logs.append(f"GET {app_url} => {r.status_code}")

                time.sleep(1)

            # 5) PATCH confirm (ignore 403 pour simpleuser)
            if confirmation_url:
                r = requests.patch(confirmation_url, json={"confirmed": True}, headers=headers, timeout=5)
                if r.status_code in (200, 204):
                    logs.append("Confirmation envoyée avec succès")
                elif r.status_code == 403:
                    logs.append("Permission refusée pour confirmation (simpleuser)")
                else:
                    logs.append(f"Erreur PATCH confirmation : {r.status_code} - {r.text[:200]}")

            self._save_result(email, "SUCCESS", logs)

        except Exception as e:
            logs.append(f"Exception levée : {str(e)}")
            self._save_result(email, "ERROR", logs)

    def _save_result(self, email, status, logs):
        try:
            Test1Result.objects.create(
                email=email,
                status=status,
                logs="\n".join(logs)
            )
        except Exception:
            pass
        for line in logs:
            self.stdout.write(line)
        self.stdout.write(self.style.SUCCESS(f"Résultat final : {status}"))
