## History Link
[https://docs.google.com/spreadsheets/d/1I9FkE2kBgWvkfvFvr0fTtwTk_30CCcvVFsWzilBXxHg/edit#gid=0](https://docs.google.com/spreadsheets/d/1zuyh-xpjTfRkvMg3lGsySdkzC4LMfYkDvWTwDdEiXgk/edit#gid=127736069)

## Dataset

|  LANGUAGE  | Train  |  Dev  | Test  |
| ---------- | ------ | ----- | ----- |
|   Korean   | 4,478  |  500  |  893  |
|   English  | 10,880 | 3,627 | 3,627 |
|  Japanese  | 13,198 | 4,400 | 4,400 |
|    Zh_CN   | 13,357 | 4,453 | 4,453 |


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

|   LANGUAGE    |       Model      | Intent acc (%) | Slot F1 (%) | Slot Precision (%) | Slot Recall (%) | Sentence acc (%) |
|  ----------   | ---------------- | -------------- | ----------- | ------------------ | --------------- | ---------------- |
|  **Korean**   |   KoBert + CRF   |    **89.3**    |     78.4    |        74.5        |      81.9       |       60.4       |
|               |  KoElectra + CRF |      89.1      |   **80.6**  |      **77.4**      |    **84.2**     |     **62.3**     |
|  **English**  |    Bert + CRF    |    **96.9**    |   **95.8**  |      **95.2**      |    **96.4**     |     **89.6**     |
|               |   Electra + CRF  |      96.4      |     94.8    |        93.9        |      95.7       |       88.1       |
|  **JAPANESE** |    Bert + CRF    |    **90.4**    |   **82.2**  |      **79.6**      |    **85.0**     |     **72.2**     |
|  **CHINESE**  |    Bert + CRF    |    **93.4**    |   **85.0**  |      **82.9**      |    **87.2**     |     **75.6**     |

## References

- [Huggingface Transformers](https://github.com/huggingface/transformers)
- [KoElectra](https://github.com/monologg/KoELECTRA)
- [KoBert](https://github.com/monologg/JointBERT)
- [pytorch-crf](https://github.com/kmkurn/pytorch-crf)
