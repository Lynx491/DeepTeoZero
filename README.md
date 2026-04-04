# 🤖 TicTacToe AI engine (v0.1.1-Alpha)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PySide6](https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)

> An intelligent Tic-Tac-Toe engine developed with **Reinforcement Learning** (DQN) and a modern **PySide6** GUI.

---

## 🎲 About intelligence
🧠 This engine has learned only with **16K self-play** with the **reinforcement learning** method, it can be further developed if desired.

- **Current State:** 🦊 This engine is **a brilliant tactician**; thanks to its neural networks, it has a **cunning** habit of trapping you in forks. 

- **The Challenge:** 🪨 trained with a **7-year-old laptop**


## 🚀 Features
- **Neural Engine:** Powered by Stable Baselines3 and Gymnasium infrastructure.
- **Modern UI:** A modern, simple and stylish GUI interface.

- **Our Goal:** 🚩 We aim to build an engine with a **+1 million neuron neural network** and bring **optimization updates.**

## 📸 ScreenShot
|No Start|Player Win|Engine Fork|
|---|---|---|
|![Game Screen](ScreenShot/ss1.png) |![Game Screen](ScreenShot/ss2.png) |![Game Screen](ScreenShot/ss3.png)|

---

## 🛠️ Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Run the game: `python3 engine.py`

> To play matches with the engine, it requires a neural network.

> ./models/Neural Networks

---
## 🛠️ Windows Build
1. Install dependencies: `pip install -r requirements.txt && pip install pyinstaller`
2. Compilation: `pyinstaller engine.py --onefile --noconsole --add-data "DTZ_icon.ico" --icon=DTZ_icon.ico --collect-all stable_baselines3 --collect-all torch`

## 🛠️ Linux And MacOS Build
1. Install dependencies: `pip install -r requirements.txt && pip install pyinstaller`
2. Compilation: `pyinstaller engine.py --onefile --noconsole --add-data "DTZ_icon.png" --icon=DTZ_icon.png --collect-all stable_baselines3 --collect-all torch`

---

## 📄 Licence
This project is licensed under the **Apache2.0 License**.
