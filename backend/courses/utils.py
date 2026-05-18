import qrcode
import base64
from io import BytesIO

def generate_upi_qr(course):
    upi_id = "9848523594@ybl"
    name = "LMS Course Payment"
    amount = course.price

    upi_url = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

    qr = qrcode.make(upi_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    img_str = base64.b64encode(buffer.getvalue()).decode()

    return img_str