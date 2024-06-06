## Dataset

|         | Train  | Dev | Test | Intent Labels | Slot Labels |
| ------- | ------ | --- | ---- | ------------- | ----------- |
| Korean  | 4,478  | 500 | 893  | 21            | 120         |


## Training & Evaluation

```bash
$ python3 main.py --task {task_name} \
                  --model_type {model_type} \
                  --model_dir {model_dir_name} \
                  --do_train --do_eval \
                  --use_crf

# ex. For "Ko" / Model "KoElectra" or "KoBert"
$ python3 main.py --task ko \
                  --model_type KoElectra \
                  --model_dir {model_dir_name} \
                  --do_train --do_eval

## Prediction

```bash
$ python3 predict.py --input_file {INPUT_FILE_PATH} --output_file {OUTPUT_FILE_PATH} --model_dir {SAVED_CKPT_PATH}
```

## Results

|               |                  | Intent acc (%) | Slot F1 (%) | Slot Precision (%) | Slot Recall (%) | Sentence acc (%) |
|  ----------   | ---------------- | -------------- | ----------- | ------------------ | --------------- | ---------------- |
|  **Korean**   | KoBert + CRF     |    **89.3**    |     78.4    |        74.5        |      81.9       |       60.4       |
|               | KoElectra + CRF  |      89.1      |   **80.6**  |      **77.4**      |    **84.2**     |     **62.3**     |
| -----------   | ---------------- | -------------- | ----------- | ------------------ | --------------- | ---------------- |
| **English**   | KoBert + CRF     |    **89.3**    |     78.4    |        74.5        |      81.9       |       60.4       |
|               | KoElectra + CRF  |      89.1      |   **80.6**  |      **77.4**      |    **84.2**     |     **62.3**     |
| ----------    | ---------------- | -------------- | ----------- | ------------------ | --------------- | ---------------- |
|  **JAPANESE** | KoBert + CRF     |    **89.3**    |     78.4    |        74.5        |      81.9       |       60.4       |
|               | KoElectra + CRF  |      89.1      |   **80.6**  |      **77.4**      |    **84.2**     |     **62.3**     |
|  -----------  | ---------------- | -------------- | ----------- | ------------------ | --------------- | ---------------- |
|  **CHINESE**  | KoBert + CRF     |    **89.3**    |     78.4    |        74.5        |      81.9       |       60.4       |
|               | KoElectra + CRF  |      89.1      |   **80.6**  |      **77.4**      |    **84.2**     |     **62.3**     |

## References

- [Huggingface Transformers](https://github.com/huggingface/transformers)
- [KoElectra](https://github.com/monologg/KoELECTRA)
- [KoBert](https://github.com/monologg/JointBERT)
- [pytorch-crf](https://github.com/kmkurn/pytorch-crf)
