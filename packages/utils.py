import numpy as np


def distance(*args):
    return np.sqrt(sum(arg**2 for arg in args))


def pol_to_cart(r, incl, azim):
    x = r * np.sin(np.radians(incl)) * np.cos(np.radians(azim))
    y = r * np.sin(np.radians(incl)) * np.sin(np.radians(azim))
    z = r * np.cos(np.radians(incl))
    return x, y, z


def cart_to_pol(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    incl = np.degrees(np.arccos(z / r))
    azim = np.degrees(np.arctan2(y, x))
    return [r, incl, azim]


def flatten(*args):
    result = []
    for arg in args:
        if isinstance(arg, list) or isinstance(arg, tuple):
            result.extend(flatten(*arg))
        else:
            result.append(arg)
    return result

def import_images_from_folder(img_folder_path, pixel_height, pixel_width): # Change params as needed, add whatever set size you'd like
    images = []
    
    # Get list of image files in the folder
    image_files = [f for f in os.listdir(img_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for image_file in image_files:
        image_path = os.path.join(img_folder_path, image_file)
        
        # Open the image using PIL
        pil_img = Image.open(image_path)
        
        # Resize the image
        resized_img = scale_to(pil_img, pixel_height, pixel_width)
        
        images.append(resized_img)
    
    return images

def scale_to(img, pixel_height, pixel_width):
    # Open the image using PIL
    pil_img = Image.fromarray(img)  # Assuming img is a NumPy array? Don't know how else you'd be doing it
    
    # Resize the image
    resized_img = pil_img.resize((pixel_width, pixel_height))
    
    return np.array(resized_img)  # Convert back to NumPy array

