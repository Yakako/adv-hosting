import tensorflow as tf

MODEL_PATH = "app/ml/best_model.h5"

model = tf.keras.models.load_model(MODEL_PATH)

def predict(input_data):
    """
    input_data: numpy array
    """
    prediction = model.predict(input_data)
    return prediction
