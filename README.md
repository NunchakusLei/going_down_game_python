<!-- MIT License

Copyright (c) 2018 Chenrui Lei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. -->


# Going Down Game implemented in Python 3

This is the implementation of Going Down Game in python 3.

![alt text][gaming_screencast]

---


# Dependencies

- Python v3.x
- Collision Engine 2D v0.0.1 ([https://github.com/NunchakusLei/collision-engine-2d](https://github.com/NunchakusLei/collision-engine-2d))

---


# How to play (Game controls)

#### Rudes

The deeper you go donw the higher points you will get. You will die if you touch the top or bottom. 

#### Game controls

- key **A**: moving to left
- key **D**: moving to right
- key **SPACE**: jump

---


# Code Execution

You can use the commands below to execute the game.

```bash
git clone https://github.com/NunchakusLei/going_down_game_python.git
cd going_down_game_python/scripts/
python3 going_down_game.py
```
---


# References

- https://github.com/NunchakusLei/collision-engine-2d

---

[gaming_screenshot]: ./Doc/images/going_down_game_screenshot.png "gaming screenshot"
[gaming_screencast]: ./Doc/images/going_down_game_screencast.gif "gaming screenshot"