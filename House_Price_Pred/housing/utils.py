import os
import joblib
import numpy as np

MODEL_PATH = os.environ.get('HOUSE_MODEL_PATH', os.path.join(os.path.dirname(__file__), 'model.joblib'))

_model_cache = None

def load_model():
    global _model_cache
    if _model_cache is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Train it with manage.py train_model or set HOUSE_MODEL_PATH.")
        _model_cache = joblib.load(MODEL_PATH)
    return _model_cache

def predict_price(area, room, parking, warehouse, elevator, address):
    """
    Accepts raw inputs (area: float, room/parking/warehouse/elevator: int (0/1), address: string)
    Returns tuple: (predicted_price_log, predicted_price_usd)
    """
    model = load_model()
    import pandas as pd
    X = pd.DataFrame([{
        'Area': area,
        'Room': int(room),
        'Parking': int(parking),
        'Warehouse': int(warehouse),
        'Elevator': int(elevator),
        'Address': str(address)
    }])
    # model is a pipeline that includes the encoder; it expects same columns used in training
    pred_log = model.predict(X)[0]
    pred_usd = float(np.expm1(pred_log))
    return float(pred_log), pred_usd