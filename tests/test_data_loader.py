"""Uji KDD-1 Data Loader & inferensi Predictor + pipeline end-to-end ringkas."""

import pandas as pd
import pytest

from prediksi_haid import data_loader, predictor
from prediksi_haid.constants import FEATURE_COLUMNS, LIKERT_ITEM_COLUMNS, TARGET_COLUMN


def test_validate_schema_ok():
    cols = {c: [1] for c in LIKERT_ITEM_COLUMNS}
    cols[TARGET_COLUMN] = ["teratur"]
    assert data_loader.validate_schema(pd.DataFrame(cols)) is True


def test_validate_schema_missing():
    df = pd.DataFrame({"q1": [1]})
    with pytest.raises(ValueError):
        data_loader.validate_schema(df)


def test_load_dataset_csv(tmp_path):
    p = tmp_path / "d.csv"
    pd.DataFrame({"a": [1, 2]}).to_csv(p, index=False)
    out = data_loader.load_dataset(str(p))
    assert len(out) == 2


def test_label_prediction():
    assert predictor.label_prediction(1) == "Teratur"
    assert predictor.label_prediction(0) == "Tidak Teratur"


def test_predict_single_and_batch():
    from prediksi_haid import model as model_mod

    # data mainan pakai nama kolom fitur asli
    train = pd.DataFrame({c: [1, 2, 3, 4, 5, 6] for c in FEATURE_COLUMNS})
    y = pd.Series([0, 0, 0, 1, 1, 1])
    m = model_mod.train_model(model_mod.build_model({}), train, y)

    one = predictor.predict_single(m, {c: 6 for c in FEATURE_COLUMNS})
    assert one in (0, 1)

    batch = predictor.predict_batch(m, train)
    assert len(batch) == len(train)
