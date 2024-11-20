from PIL import Image, ImageFilter
from scripts.blur_image import blur_image


def test_blur_image(mocker):
    # Mock the Image.open method
    mock_image = mocker.MagicMock(spec=Image.Image)
    mock_image.filter = mocker.MagicMock(
        side_effect=lambda f: f"blurred_with_{round(f.radius, 1)}"
    )
    mock_image_open = mocker.patch("PIL.Image.open", return_value=mock_image)

    # Call the function under test
    mock_path = "dummy_path"
    blurred_images = blur_image(mock_path)

    # Assertions
    mock_image_open.assert_called_once_with(
        mock_path
    )  # Ensure Image.open was called with the path
    assert mock_image.filter.call_count == 9  # Ensure filter was called 9 times

    # Validate the blur levels applied
    expected_radii = [i * 1.0 for i in range(1, 10)]
    for i, expected_radius in enumerate(expected_radii):
        applied_filter = mock_image.filter.call_args_list[i][0][0]
        assert isinstance(applied_filter, ImageFilter.GaussianBlur)
        assert round(applied_filter.radius, 1) == round(expected_radius, 1)
        assert blurred_images[i] == f"blurred_with_{expected_radius}"
