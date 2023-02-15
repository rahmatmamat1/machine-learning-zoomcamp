import urllib.request
import tensorflow as tf

url = "https://github.com/alexeygrigorev/mlbookcamp-code/releases/download/chapter7-model/xception_v4_large_08_0.894.h5"
filename = "clothing-model-v4.h5"

# download model
urllib.request.urlretrieve(url, filename)

# covert SavedModel format
model = tf.keras.models.load_model(filename)
tf.saved_model.save(model, 'clothing-model')