# Web Scraper

### Description:
Web scraper collecting content data from https://habr.com

This script downloads articles to the base folder (by default `articles`). 
Each articles is saved in a separate folder. There is a file `article.txt`
which contains all text of the article. There are also images in the folder
if they are included in the article.

### Install
```poetry install```


### Run

```shell
Usage: scraper [OPTIONS]

  Save articles from habr.com

Options:
  --threads INTEGER     [required]
  --articles INTEGER    [required]
  --help                Show this message and exit.

```

### Example

Executing `scraper --threads 4 --articles 25` 
will run the script with 4 threads to download 25 latest articles.

The process of downloading will take some time depending on the speed 
of your internet connection. There is a progress bar showing how 
many articles have been downloaded:
```shell
Fetching urls for articles
Downloading  [####################################]  100%          
Done
```

After the script finishes running, the destination folder has structure:
```shell
articles
├── STM32 LTDC и 7-дюймовый дисплей часть 1  Хабр
│   ├── 01052f2d029397184c3b44ec64d7b6ab.png
│   ├── 331b9d22fe0ba644b7b6299ba0d70af7.png
│   ├── 39a069271bf7bb0a2b4993e7938e185f.png
│   ├── 40c54fa20c6853bca8e29de224c55b0d.png
│   ├── 509ad2927c7cb0d5bf25e7f69b6ffab9.jpg
│   ├── 549c11b6af909ff871931f8b3d80756e.png
│   ├── 7f6882895be7fb403fe3fea1c67ef540.png
│   ├── 87f079e5e644cac4963652a63f7a1ec4.png
│   ├── a96f21726556c531dc63943328ffcc20.jpg
│   ├── article.txt
│   └── b8d51a27ce1409382103fbc27cbfe1f1.jpg
├── Визуализация данных в интерфейсе  Блог компании EPAM  Хабр
│   ├── 0f0b155e73e96645d73c17431f8d629e.jpeg
│   ├── 1ebbeaad9ee2450740a00b4d5bcebc4f.png
│   ├── 224fa455216e773e4670878557669e05.png
│   ├── 237475ddb4d90e6c8fe831517b8793ab.png
│   ├── 239f13bbedf8d4e6d85383ed3286f202.png
│   ├── 23f65407f9f4d962854ad77aa896289a.png
│   ├── 3cae38d62f5903ce5856ae72c5a4a459.png
│   ├── 455d2d6aa98d0d4f220fecdf93e0b3cc.png
│   ├── 692c12093e40db1100897a7d718a6651.jpeg
│   ├── 7c973902f3566f04e333ec45ce72cc06.png
│   ├── 81242b2ee1c4d58e0b718d69b7d7dd8f.png
│   ├── 8bc42da44467593ae54e8860d814a729.png
│   ├── 8d8819b65a40838149ebf60cbb144a96.png
│   ├── 8e5dcc3a537d93e8f056dee9257c9d1b.png
│   ├── 9e96281e985cd43857ed5a8fbc27c64b.jpeg
│   ├── a079d3b9c1c9e6e1b8b6c1267c416646.png
│   ├── a594066406adb414c7647a41b1397c5c.png
│   ├── a70eab586c9f9f3dc44514692f7417f0.png
│   ├── a9538f3d61b2fe6e58d2fd2d8cbe5bbb.jpeg
│   ├── article.txt
│   ├── bb1dffb2522abfb66214800a4987aa01.png
│   ├── cb7aa7ff6eec36ddf2a04937d438ce44.jpg
│   ├── d1a2c814610a3945a363cfade610517c.png
│   ├── d23f5009d593009c4c98733a72a05a08.png
│   ├── e117658d3f011c67a87c06feb067aaa1.png
│   ├── eaf25c0051b405ac185cb5410066141c.png
│   ├── ec01e6892ebb4ff3471086c4d5fcf008.png
│   └── fe6b4ce97d2cc280e1915baae7ef9da6.png
├── Конструирование эпидемиологических моделей  Хабр
│   ├── 05bd7252f55cd39971c17b49fc716fd2.png
│   ├── 24fe160e97f5fb0a6e1b69bf9e4788ed.png
│   ├── 35467441f63ff6872d25218f6c3d59dc.png
│   ├── 486d8492890da206d1758b0ca9a5b34b.png
│   ├── 560aa5c7008493a0cbfea7d8fe2981c0.png
│   ├── ad2eceafe776687ae4ba6c90576a402d.png
│   ├── article.txt
│   ├── c5f776027af4a19f66efbd66510e8506.png
│   ├── cdf7fa94492eb08bfdec4f14d73b2e76.png
│   └── e1f3883d94e2a4a4691b39c644daaddf.png
└── Преобразуем графику Fortnite в PUBG новым более быстрым подходом  Блог компании OTUS  Хабр
    ├── 0b44eaf96d86ee1793417dad145df568.png
    ├── 392a88322bf975f29840a7f9dcc0eb7e.png
    ├── 47e56c551b54c388d1b1dfd5314a7126.gif
    ├── 90b160182307ab5e86596d4f367d89d9.png
    ├── article.txt
    ├── b46051181a4f221c990bedb4ecb0478d.png
    └── f8f82fdb9edc14d4619ddfb06d325ff3.png

```

### Create venv:
    make venv

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format
