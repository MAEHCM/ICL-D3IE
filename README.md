## ICL-D3IE: In-Context Learning with Diverse Demonstrations Updating for Document Information Extraction

Congratulations on our paper being accepted by ICCV 2023! 
We will continue to update the repository.

## Table of contents
* [Installation](#installation)
* [Datasets](#datasets)
* [Predict](#predict)
* [Eval](#eval)
* [Results](#results)


We propose a simple but effective in-context learning framework called ICL-D3IE, which enables LLMs to perform DIE with different types of demonstration examples. 

![](https://user-images.githubusercontent.com/111342294/223765044-5fcfc41b-0b5f-4b56-bd64-9aeefba39791.png)


# Installation

Installation for Project，if you need to study the robustness of the model to text shift, you need to install [Textattack](https://github.com/QData/TextAttack)

```
git clone https://anonymous.4open.science/r/ICL-D3IE-B1EE && cd ICL-D3IE
```

# Datasets

| Dataset | Link      |
|:--------:| :------------:|
| FUNSD | [download](https://www.kaggle.com/datasets/aravindram11/funsdform-understanding-noisy-scanned-documents)|
| CORD | [download](https://github.com/clovaai/cord)|
| SROIE | [download](https://www.kaggle.com/datasets/urbikn/sroie-datasetv2)|


### Preprocess Input

The data is processed as follows, like "****.json"，set your input path and run `preprocess_{ }.py`.

```
{text:"TAX 5.455",Box:[490 743 819 777]}{text:"TOTAL 60.000",Box:[101 820 851 858]}{text:"(Qty 2.00",Box:[314 820 615 856]}{text:"EDC CIMB NIAGA No: xx7730 60.000",Box:[138 898 847 938]}{text:"901016",Box:[97 604 212 635]}...
```

### Preprocess GT

The data is processed as follows, like "****.json"，set your GT path and run `preprocess_{ }.py`.

```
{text:"TAX 5.455",Box:[490 743 819 777],entity:SUB_TOTAL.TAX_PRICE}{text:"TOTAL 60.000",Box:[101 820 851 858],entity:TOTAL.TOTAL_PRICE}{text:"(Qty 2.00",Box:[314 820 615 856],entity:TOTAL.MENUQTY_CNT}{text:"EDC CIMB NIAGA No: xx7730 60.000",Box:[138 898 847 938],entity:TOTAL.CREDITCARDPRICE}{text:"901016",Box:[97 604 212 635],entity:MENU.NUM}
```

# Predict

Use GPT3 to predict the ouput perfectly!

```
cd GPT3 && python gpt3_{ }.py 
```

Or use ChatGPT to predict the ouput perfectly!

```
cd chatgpt && python chatgpt_{ }.py
```

# Eval

```
cd eval && python eval_{ }.py
```

# Results

### Reulst of comparing ICL-D3IE with Standard ICL and existing pre-trained VDU models fine-tuned with full training samples and a few sample on three benchmark datasets in ID and OOD settings.

![](https://user-images.githubusercontent.com/111342294/223914428-6f8c0f1a-9ce7-4675-b3f0-28fe66230a03.png)
