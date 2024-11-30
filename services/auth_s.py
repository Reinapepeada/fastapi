from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Create an instance of CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TRAIGO LAS VARIABLES DE ENTORNO
from dotenv import load_dotenv

load_dotenv()
# Configuración del secreto y algoritmo para JWT
SECRET_KEY = os.getenv("SECRET_KEY")  # Cambia esto por una clave secreta segura
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# Función para verificar permisos del usuario que hace la petición
def get_current_user(token: str = None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise JWTError
        return email, role
    except JWTError:
        return None, None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# enviar email forgot password with token
def send_email_forgot_password(email: str):
    sender_email = os.getenv("EMAIL_HOST_USER")
    sender_password = os.getenv("EMAIL_HOST_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    # Create the email content
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender_email
    message["To"] = email

    # Create the token
    token = create_access_token(data={"sub": email}, expires_delta=timedelta(hours=24))

    # Create the email content
    reset_link = f"http://teamcelular.com/reset-password?token={token}"
    text = f"""\
    Hi,
    Please click the link below to reset your password:
    {reset_link}
    """
    html = f"""\
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Recuperación de Contraseña</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 0; color: #2d3748;">
            <div style="max-width: 600px; margin: 50px auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); border: 1px solid #e2e8f0;">
                <div style="background-color: #1a202c; color: #ffffff; text-align: center; padding: 20px;">
                    <h1 style="font-size: 22px; margin: 0;">Team Celular</h1>
                </div>
                <div style="padding: 30px 20px; text-align: center;">
                    <h2 style="font-size: 20px; margin-bottom: 10px; color: #4a5568;">Recupera tu contraseña</h2>
                    <p style="font-size: 16px; line-height: 1.6; color: #718096; margin-bottom: 20px;">
                        Hemos recibido una solicitud para restablecer tu contraseña. Haz clic en el botón de abajo para continuar con el proceso.
                    </p>
                    <a href="https://teamcelular.com/reset-password?{token}" style="display: inline-block; padding: 12px 30px; font-size: 16px; color: #ffffff; background-color: #2b6cb0; text-decoration: none; border-radius: 5px; margin-bottom: 20px;">
                        Restablecer Contraseña
                    </a>
                    <p style="font-size: 16px; line-height: 1.6; color: #718096;">
                        Si no solicitaste este cambio, puedes ignorar este correo de manera segura.
                    </p>
                </div>
                <div style="text-align: center; padding: 15px; font-size: 14px; background-color: #f7fafc; color: #a0aec0;">
                    <p>&copy; 2024 Team Celular. Todos los derechos reservados.</p>
                    <p>
                        <a href="https://teamcelular.com/contacto" style="color: #2b6cb0; text-decoration: none;">Contáctanos</a> |
                        <a href="https://teamcelular.com/terms" style="color: #2b6cb0; text-decoration: none;">Términos y condiciones</a>
                    </p>
                </div>
            </div>
        </body>
    </html>
    """

    # Attach the plain and HTML versions of the email content
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
