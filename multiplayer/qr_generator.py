import io
import base64
import qrcode
from PIL import Image


def generate_qr_code(data: str, size: int = 300) -> str:
    """
    Generate a QR code and return it as a base64-encoded PNG string
    
    Args:
        data: The data to encode in the QR code (e.g., join URL)
        size: Size of the QR code in pixels
    
    Returns:
        Base64-encoded PNG image string
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"


def generate_join_url(session_id: str, base_url: str = None) -> str:
    """
    Generate a join URL for a session
    
    Args:
        session_id: The session ID to join
        base_url: Base URL of the application (if None, uses relative path)
    
    Returns:
        Full join URL
    """
    if base_url:
        return f"{base_url}?mode=join&session={session_id}"
    return f"?mode=join&session={session_id}"
