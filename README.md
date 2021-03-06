# AI Paperboy

## ๐ Project Abstract

### Purpose

* ์ฌ์ฉ์๊ฐ ์ง๋ฌธ์ผ๋ก ์์ฒญํ๋ฉด ๋ต๋ณ์ด ์๋ ๋ด์ค ๊ธฐ์ฌ๋ฅผ ์คํฌ๋ฉ ํด์ฃผ๋ ์๋น์ค

### Functions
* ๊ธฐ์ฌ๋ฅผ ์ฝ๊ณ  ๋ค์ ๋ณด๊ณ  ์ถ์ ๊ธฐ์ฌ ์คํฌ๋ฉ ๊ธฐ๋ฅ
* ์ค์๊ฐ ์ง๋ฌธ์ ๋ํ ๋ต๋ณ ๊ธฐ์ฌ AI ์คํฌ๋ฉ ๊ธฐ๋ฅ
* ์ผ์  ์๊ฐ๋ง๋ค ๊ธฐ์ฌ ๋ชฉ๋ก ์๋ฐ์ดํธ ํ ์ง๋ฌธ์ ๋ํ ๋ต๋ณ ๊ธฐ์ฌ AI ์คํฌ๋ฉ ๊ธฐ๋ฅ

## ๐จโ๐จโ๐งโ๐ฆ Team Covit-19

### Members

| <center>๋ฐ๋ณ์ด</center> | <center>์ด์ค์</center> | <center>์ต์์ค</center> | <center>์ถ์ฐฝํ</center>
| -------- | -------- | -------- | -------- |
| [<img src="https://i.imgur.com/1zMaAt1.png" height=100px width=100px></img>](https://github.com/ParkByeolYi) | [<img src="https://i.imgur.com/o3BFRGk.png" height=100px width=100px></img>](https://github.com/JunsooLee) | [<img src="https://i.imgur.com/GzN3ZOv.png" height=100px width=100px></img>](https://github.com/woongjoonchoi) | [<img src="https://i.imgur.com/S4cM768.png" height=100px width=100px></img>](https://github.com/cnckdgks) |
| <center>[github](https://github.com/ParkByeolYi)</center> | <center>[github](https://github.com/JunsooLee)</center> | <center>[github](https://github.com/woongjoonchoi)</center> | <center>[github](https://i.imgur.com/S4cM768.png)</center> |


### Responsibilities
|                     | ๋ฐ๋ณ์ด | ์ด์ค์ | ์ต์์ค | ์ถ์ฐฝํ |
| ------------------- | ------ | ------ | ------ | ------ |
| Data collection <br> make test dataset and analysis | common | common | common | common |
| Code refactoring    | Retrieval | post_processing <br> train |extraction_pre_process <br>generation_pre_process <br>generation_compute_metrics <br>configuration  <br>building tiny dataset  | Retrieval |
| User flow/Data flow |        | User Flow <br> Data Flow |    training pipeline    |  User Flow<br> Data Flow  |
| Modeling            | Apply BM 25       | build train dataset <br> model training | train with tiny dataset <br>training reader model <br> error analysis on generation model         |   Apply BM 25   |
| Prototyping         |        |        |  reader model demo      |  ODQA model / Batch Serving      |
| Frontend            |  web design <br> sign in <br> sign up <br> news scrap  | article_form <br>performance improvement with UI policy |  homepage_news title list <br> ai scrap news title list <br>my scrap news title list   | performance improvement with UI policy  |
| Backend             | build sqlite schema <br> sign in <br> sign up <br> news scrap | user_input |  homepage_news title list  with wiki_news_db<br> ai scrap news title list  with ai_scrap_db<br>my scrap news title list  with user_scrap_db     |  build layered architecture design <br> get article page and user_input with real time service <br> batch serving |


### Collaboration tool
<img src="https://img.shields.io/badge/Google Drive-4285F4?style=flat-square&logo=Google Drive&logoColor=white"/> <img src="https://img.shields.io/badge/MS ToDo-6264A7?style=flat-square&logo=Microsoft&logoColor=white"/> <img src="https://img.shields.io/badge/Notion-5E5E5E?style=flat-square&logo=Notion&logoColor=white"/> 

## ๐พ Installation
### 1. Set up the python environment:
- Recommended python version 3.8.5

```
$ conda create -n venv python=3.8.5 pip
$ conda activate venv
```
### 2. Install other required packages

```
$ cd $ROOT/final-project-level3-nlp-19/code
$ poetry install
$ poetry shell
```

## ๐ฅ Usage
### 1. Project Structure
```
code
โโโrouters/
โโโschema/
โโโservices/
โโโtemplates/
โโโAIPaperboy.py
โโโmodel train file (.py)
```
**4 folder for serving**
- **routers**: Controller
- **schema**: Model
- **sevices**: Project's functions
- **templates**: HTML & CSS file

### 2. Train
```
$ cd $ROOT/final-project-level3-nlp-19/code
$ python train_copy.py --output_dir ./outputs  --run_extraction True --run_generation False --do_train --do_eval \
--evaluation_strategy 'steps' --eval_steps 60 --logging_steps 60 --per_device_eval_batch_size 16 \
 --per_device_train_batch_size 16 --save_strategy "no" --fp16 True --fp16_full_eval True --num_train_epochs 9 --report_to "wandb" \
 --overwrite_output_dir
```

### 3. Inference
```
$ python inference_copy.py --output_dir ./outputs/test_dataset/ --dataset_name ../data/test_dataset/ --model_name_or_path ./models/train_dataset/ --do_predict  --overwrite_cache --overwrite_output_dir
```

### 4. Execute
```
$ cd $ROOT/final-project-level3-nlp-19/code
$ python AIPaperboy.py --output_dir ./outputs/test_dataset/ --model_name_or_path ./models/train_dataset/ --dataset_name ../data/test_dataset/ --do_predict
```

## ๐ฝ Demo
* [AI Paperboy Demo Video](https://www.youtube.com/watch?v=n7oPu7vrQ8s)
* [AI Paperboy Presentation](https://docs.google.com/presentation/d/1rpgp9knamiiqs4lITZMEiixSA8sfWyvv/edit?usp=sharing&ouid=110643334622897859461&rtpof=true&sd=true)

