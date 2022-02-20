import os
import numpy as np
from PIL import Image

from django.conf import settings
from web.deblurgan.utils import load_images, write_log, deprocess_image, preprocess_image, load_image
from web.deblurgan.model import generator_model, discriminator_model, generator_containing_discriminator_multiple_outputs


def deblur(weight_path, input_dir, output_dir):
    g = generator_model()
    g.load_weights(weight_path)
    for image_name in os.listdir(input_dir):
        image = np.array([preprocess_image(load_image(os.path.join(input_dir, image_name)))])
        x_test = image
        generated_images = g.predict(x=x_test)
        generated = np.array([deprocess_image(img) for img in generated_images])
        x_test = deprocess_image(x_test)
        for i in range(generated_images.shape[0]):
            x = x_test[i, :, :, :]
            img = generated[i, :, :, :]
            output = np.concatenate((x, img), axis=1)
            im = Image.fromarray(output.astype(np.uint8))
            im.save(os.path.join(output_dir, image_name))
    return

# according the image path to read the image and covert it
# to the given size, then slice it, finally return the full and blur images
def format_image(image_path, size):
    image = Image.open(image_path)
    # slice image into full and blur images
    image_full = image.crop((0, 0, image.size[0] / 2, image.size[1]))
    # Note the full image in left, the blur image in right
    image_blur = image.crop((image.size[0] / 2, 0, image.size[0], image.size[1]))
    # image_full.show()
    # image_blur.show()
    image_full = image_full.resize((size, size), Image.ANTIALIAS)
    image_blur = image_blur.resize((size, size), Image.ANTIALIAS)
    # return the numpy arrays
    return np.array(image_full), np.array(image_blur)