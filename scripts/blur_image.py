from PIL import Image, ImageFilter
from io import BytesIO
import concurrent.futures

def blur_single_image(image: bytes, blur_level: float) -> bytes:
    image_serialized = Image.open(BytesIO(image))
    
    if image_serialized.mode == 'P':
        image_serialized = image_serialized.convert('RGBA')
    
    blurred_image = image_serialized.filter(ImageFilter.GaussianBlur(blur_level))
    
    with BytesIO() as blurred_image_bytes:
        blurred_image.save(blurred_image_bytes, format="PNG")
        blurred_image_bytes.seek(0)
        return blurred_image_bytes.getvalue()

def blur_image(*, blur_levels: list, image: bytes) -> list:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the function to the blur levels in parallel
        results = list(executor.map(lambda blur_level: blur_single_image(image, blur_level), blur_levels))
    return results
