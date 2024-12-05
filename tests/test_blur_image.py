import pytest
from PIL import Image, ImageFilter
from io import BytesIO
from scripts.blur_image import blur_single_image, blur_image

@pytest.fixture
def sample_image():
    # Create a simple red image for testing
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))
    with BytesIO() as img_byte_array:
        image.save(img_byte_array, format='PNG')
        return img_byte_array.getvalue()

def test_blur_single_image(sample_image, mocker):
    # Create a mock image object to return from the filter method
    mock_image = Image.new("RGBA", (100, 100))
    
    # Mock the filter method to return the mock image
    mock_filter = mocker.patch.object(Image.Image, 'filter', return_value=mock_image)
    
    blur_level = 5
    blurred_image = blur_single_image(sample_image, blur_level)
    
    # Assert that filter is called with the correct GaussianBlur type, not instance
    mock_filter.assert_called_once_with(mocker.ANY)  # Check if the argument is of any type
    
    # Check that the filter was called with an instance of GaussianBlur
    args, _ = mock_filter.call_args
    assert isinstance(args[0], ImageFilter.GaussianBlur)
    assert args[0].radius == blur_level  # Ensure the correct blur level is set
    
    # Ensure the returned image is a valid PNG image
    with Image.open(BytesIO(blurred_image)) as img:
        assert img.format == 'PNG'
        assert img.size == (100, 100)  # Check the image size remains the same

def test_blur_image(sample_image, mocker):
    # Mock blur_single_image to avoid actual image processing
    mock_blur_single_image = mocker.patch('scripts.blur_image.blur_single_image', return_value=b'blurred_data')
    
    blur_levels = [1, 2, 3]
    result = blur_image(blur_levels=blur_levels, image=sample_image)
    
    # Assert blur_single_image was called with the correct parameters
    assert mock_blur_single_image.call_count == len(blur_levels)
    for i, blur_level in enumerate(blur_levels):
        mock_blur_single_image.assert_any_call(sample_image, blur_level)
    
    # Ensure the result contains the mocked data
    assert result == [b'blurred_data'] * len(blur_levels)
