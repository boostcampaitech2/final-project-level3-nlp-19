from typing import Tuple
import numpy as np

from utils_qa import postprocess_qa_predictions
from arguments import DataTrainingArguments
from transformers import EvalPrediction, TrainingArguments

def post_processing_function(
        examples,
        features,
        predictions: Tuple[np.ndarray, np.ndarray],
        data_args: DataTrainingArguments,
        training_args: TrainingArguments,
    ) -> EvalPrediction:
    # Post-processing: start logits과 end logits을 original context의 정답과 match시킵니다.
    predictions = postprocess_qa_predictions(
        examples=examples,
        features=features,
        predictions=predictions,
        max_answer_length=data_args.max_answer_length,
        output_dir=training_args.output_dir,
    )
    # Metric을 구할 수 있도록 Format을 맞춰줍니다.
    formatted_predictions = [
        {"id": k, "prediction_text": v} for k, v in predictions.items()
    ]

    if training_args.do_predict:
        return formatted_predictions

    elif training_args.do_eval:
        references = [
            {"id": ex["id"], "answers": ex[answer_column_name]} for ex in datasets["validation"]
        ]

        return EvalPrediction(
            predictions=formatted_predictions, label_ids=references
        )
