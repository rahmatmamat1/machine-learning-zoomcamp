import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.get_bucket('machine_learning_model')
blob = bucket.blob('clothing-model.tflite')
blob.download_to_filename('/tmp/clothing-model.tflite')

preprocessor = create_preprocessor('xception', target_size=(299, 299))


interpreter = tflite.Interpreter(model_path='/tmp/clothing-model.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


classes = [
    'dress',
    'hat',
    'longsleeve',
    'outwear',
    'pants',
    'shirt',
    'shoes',
    'shorts',
    'skirt',
    't-shirt'
]

def predict(request):
    data = request.get_json()
    url = data['url']
    X = preprocessor.from_url(url)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)

    float_predictions = preds[0].tolist()

    return dict(zip(classes, float_predictions))