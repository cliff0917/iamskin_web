from tensorflow.keras.utils import img_to_array, load_img
import keras
import numpy as np
from PIL import Image

# 回傳切割結果圖片
def predict(model, img_path):
  img_rows, img_cols = 128, 128
  img = load_img(img_path, target_size=(img_rows, img_cols, 3))
  x_1 = img_to_array(img)
  x = np.expand_dims(x_1, axis=0)
  y = model.predict(x)
  y_overall = np.multiply(x_1, y).reshape(img_rows, img_cols, 3)
  img = Image.fromarray(np.uint8(y_overall), "RGB")
  # img.save('test.jpg')
  return img


def load_model(path):
  return keras.models.load_model(path)