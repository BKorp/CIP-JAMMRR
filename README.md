# 1. CIP-JAMMRR
 Conversational Interfaces: Practice - A project for the creation of the JAMMRR chatbot

## 1.1. Table of Contents
- [1. CIP-JAMMRR](#1-cip-jammrr)
  - [1.1. Table of Contents](#11-table-of-contents)
  - [1.2. General](#12-general)
    - [1.2.1. The project](#121-the-project)
    - [1.2.2. The chatbot](#122-the-chatbot)
  - [1.3. Running the chatbot](#13-running-the-chatbot)
    - [1.3.1. Requirements](#131-requirements)
    - [1.3.2. Using the chatbot](#132-using-the-chatbot)
      - [1.3.2.1. Battle](#1321-battle)
      - [1.3.2.2. Prototype](#1322-prototype)
    - [1.3.3. Turning off the chatbot](#133-turning-off-the-chatbot)

## 1.2. General
### 1.2.1. The project
This is a project that was made for the course [`Conversational Interfaces: Practice`](https://ocasys.rug.nl/current/catalog/course/LCX070M05) `2022/2023`, at the [`University of Groningen (RUG)`](https://www.rug.nl/).

The goal of the course was for the class to be split up into two groups to produce a chatbot for specific tasks that are set during the course. Our projects focused on the use of the creation of chatbots that could hold a conversation in a general and domain-specific way.

After the chatbot battle, this would then be used to write an internal paper for a grade.

### 1.2.2. The chatbot
The JAMMRR chatbot is a chatbot built with the following three core tenets in mind:

1. **(Research focus) Be able to hold a general and domain-specific conversation**.
2. Be able to talk in a 'human-like' fashion by way of:
   1. listening/understanding (a Speech-To-Text or STT system).
   2. speaking (a Text-To-Speech TTS system).
3. Be constrained to the general requirements of the CIP course project and ChatBotBattle.

**An overview of the chatbot architecture**

![Overview of the chatbot architecture](prototype/diagrams/system_overview.png)

## 1.3. Running the chatbot
### 1.3.1. Requirements
Tested on `Python 3.11.3`, but anything close to that is likely to work as well.

To run the chatbot, one is required to install a small number of packages which can be found in `requirements.txt`.
This can be used as follows:

First, we recommend the creation of a virtual environment:
```bash
python -m venv env-cip_jammrr --upgrade-deps
```

Following this, one can move into the virtual environment and install the requirements:
```bash
source env-cip_jammrr/bin/activate
pip install -r requirements.txt
```

### 1.3.2. Using the chatbot
As highlighted in [section 1.2.2.](#122-the-chatbot), the JAMMRR chatbot makes use of STT and TTS. Interaction with the chatbot is performed through the use of a microphone and speakers (or any other kind of input and output system for sound).

There are two versions of the JAMMRR chatbot within this repository:
1. [Battle](#1321-battle) is the chatbot as it was used during the chatbot battle, with the addition of comments, changes to conform to the pep8 standard, and a small bugfix for SIGINT to stop the program. Some aspects that are found in the prototype version are missing here.
2. [Prototype](#1322-prototype) is the chatbot as it was prepared before the battle, with some bugs in place for the systems that were turned off during the battle. Here too with the addition of comments, changes to conform to the pep8 standard, and a small bugfix for SIGINT to stop the program.

#### 1.3.2.1. Battle
The program can be started by moving into the `battle` folder and using Python to run `ml_system.py`:
```bash
cd battle
python ml_system.py
```

**On runtime:**
1. After startup, JAMMRR will start by preparing the systems that will be used during its runtime (such as the language model).
2. Once the startup is finished, JAMMRR will start listening for input.
3. The chatbot makes use of the language model to generate responses for a given input.
4. When finished, the chatbot can be [`deactivated`](#133-turning-off-the-chatbot)`.

#### 1.3.2.2. Prototype
The program can be started by moving into the `prototype` folder and using Python to run `ml_system.py`:
```bash
cd prototype
python ml_system.py
```

**On runtime:**
1. After startup, JAMMRR will start by preparing the systems that will be used during its runtime (such as the language model).
2. Once the startup is finished, JAMMRR will start listening for input.
3. If no input is given, the current system will try to ask whether anyone is there, waiting for input from the conversational partner.
4. Once input is given, the chatbot will give a random greeting to its conversational partner.
5. Afterwards, the chatbot makes use of the language model to generate responses for a given input.
6. When finished, the chatbot can be [`deactivated`](#133-turning-off-the-chatbot)`.

### 1.3.3. Turning off the chatbot
As an explicit stop functionality has not been implemented for this version of the chatbot, one can stop the program through the use of a `SIGINT signal (Ctrl + c)`.

Once finished you can deactivate the virtual environment:
```bash
deactivate
```