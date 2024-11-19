from PIL import Image, ImageFilter


def blur_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # List to store blurred images
    blurred_images = []

    # Apply blurs from 10% to 90%
    for i in range(1, 10):
        blur_level = i * 0.1  # Blur level as a percentage
        blurred_image = image.filter(
            ImageFilter.GaussianBlur(blur_level * 10)
        )  # Apply the blur
        blurred_images.append(blurred_image)

    return blurred_images
