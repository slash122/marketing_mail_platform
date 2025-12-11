from rich import print
import threading
from src.mail_handler import MailHandler
from aiosmtpd.controller import Controller
from src.app_settings import app_settings

controller = Controller(MailHandler(), hostname=app_settings.SMTP_HOST, port=app_settings.SMTP_PORT)
print(controller.hostname, controller.port)

if __name__ == "__main__":
    print("STARTING")
    print(f"[blue]Main thread: {threading.get_ident()}[/blue]")
    controller.start()
    while True:
        pass

