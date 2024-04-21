from PIL import Image


def check_green_border(image_path, coordinates):
    img = Image.open(image_path)
    img_rgb = img.convert("RGB")

    for number, coords in coordinates.items():
        left_up_pixel = coords[0]
        right_down_pixel = coords[1]
        count_ok = 0

        # top
        for x in range(left_up_pixel[0], right_down_pixel[0] + 1):
            if (
                not is_green(img_rgb.getpixel((x, left_up_pixel[1])))
                and not is_green(img_rgb.getpixel((x, left_up_pixel[1] + 1)))
                and not is_green(img_rgb.getpixel((x, left_up_pixel[1] + 2)))
                and not is_green(img_rgb.getpixel((x, left_up_pixel[1] + 3)))
                and not is_green(img_rgb.getpixel((x, left_up_pixel[1] + 4)))
            ):
                break
        else:
            count_ok += 1

        # bottom
        for x in range(left_up_pixel[0], right_down_pixel[0] + 1):
            if (
                not is_green(img_rgb.getpixel((x, right_down_pixel[1])))
                and not is_green(img_rgb.getpixel((x, right_down_pixel[1] + 1)))
                and not is_green(img_rgb.getpixel((x, right_down_pixel[1] + 2)))
                and not is_green(img_rgb.getpixel((x, right_down_pixel[1] + 3)))
                and not is_green(img_rgb.getpixel((x, right_down_pixel[1] + 4)))
            ):
                break
        else:
            count_ok += 1

        # left
        for y in range(left_up_pixel[1], right_down_pixel[1] + 1):
            if (
                not is_green(img_rgb.getpixel((left_up_pixel[0], y)))
                and not is_green(img_rgb.getpixel((left_up_pixel[0] + 1, y)))
                and not is_green(img_rgb.getpixel((left_up_pixel[0] + 2, y)))
                and not is_green(img_rgb.getpixel((left_up_pixel[0] + 3, y)))
                and not is_green(img_rgb.getpixel((left_up_pixel[0] + 4, y)))
            ):
                break
        else:
            count_ok += 1

        # right
        for y in range(left_up_pixel[1], right_down_pixel[1] + 1):
            if (
                not is_green(img_rgb.getpixel((right_down_pixel[0], y)))
                and not is_green(img_rgb.getpixel((right_down_pixel[0] + 1, y)))
                and not is_green(img_rgb.getpixel((right_down_pixel[0] + 2, y)))
                and not is_green(img_rgb.getpixel((right_down_pixel[0] + 3, y)))
                and not is_green(img_rgb.getpixel((right_down_pixel[0] + 4, y)))
            ):
                break
        else:
            count_ok += 1

        if count_ok >= 2:
            return number
        print(f"{number}: {count_ok}")


def is_green(pixel):
    r, g, b = pixel
    r, g, b = pixel
    if g > r and g > b:
        return True
    return False


# pic example 1
coordinates1 = {
    1: [(75, 88), (1465, 888)],
    2: [(1477, 100), (2859, 893)],
    3: [(2864, 94), (4255, 888)],
    4: [(4250, 102), (5662, 892)],
    5: [(87, 888), (1467, 1679)],
    6: [(1474, 888), (2871, 1679)],
    7: [(2865, 888), (4268, 1679)],
    8: [(4262, 888), (5659, 1679)],
    9: [(87, 1679), (1467, 2479)],
    10: [(1474, 1679), (2871, 2479)],
    11: [(2877, 1685), (4255, 2466)],
    12: [(4262, 1679), (5659, 2479)],
    13: [(1474, 2479), (2871, 3266)],
    14: [(2865, 2479), (4268, 3266)],
}

# pic example 2
coordinates2 = {
    1: [(22, 13), (291, 166)],
    2: [(291, 13), (559, 166)],
    3: [(559, 13), (827, 166)],
    4: [(22, 166), (291, 319)],
    5: [(291, 166), (559, 319)],
    6: [(559, 166), (827, 319)],
    7: [(22, 319), (291, 472)],
    8: [(291, 319), (558, 471)],
    9: [(559, 319), (827, 471)],
}

# pic example 3
coordinates3 = {
    1: [(30, 23), (372, 217)],
    2: [(372, 23), (715, 217)],
    3: [(30, 217), (372, 413)],
    4: [(372, 217), (715, 413)],
}

result = check_green_border("image1.png", coordinates1)
print(result)
