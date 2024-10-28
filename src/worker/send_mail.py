from src.core.config import settings
from src.core.logger import logger
from src.worker.celery_app import celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@celery.task(name="send_email")
def send_email(
    subject: str,
    text: str,
    to_email: str,
    html_str: str | None = None,
) -> None:
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_str,
        plain_text_content=text,
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Error sending email: %s", str(e))
