# Portable Arcade Project

Welcome to the official page of the CS-358 Portable Arcade team project. This project was development during a semester at EPFL. All work is open-source and this page acts as a manual to let you build your own portable arcade !

# General Description

This project provides with all necessary assets to recreate a portable arcade system. This system is built with modularity in mind, such that you will be able to create new input methods for your needs ! 

## Requisites

- Raspberry Pi 1, 2, 3 or 4
- One arduino Uno, Nano or Leonardo per input method 
- USB cables to connect arduinos to the raspberry
- Jumper cables for the arduino
- At least 4 microswitches
- At least one joystick 
- Access to a 3D printer
- Access to soldering material 
- Access to an internet connection on the raspberry
- Some courage ! 

# Part 1. Software

## Arduino

Each Arduino board acts as the microcontroller of one input method, for example the joysticks and buttons. Even if it is not the best choice for value and space, it enables everyone to create new input device, without needing additional drivers. Every input method is plug and play ! 

In the repository, you will find all the sketches for the three input devices we developed. Take the ```JoystickController.ino``` file for example. All input pins for buttons and joystick are specified as constants, you can freely change them as long as they match your connections. As you may notice, how the data is sent is not very clear. For performance reasons, we decided to use binary encoding of the controller status. Refer to the below section to understand it and be able to add custom input methods.

### Binary encoding of the controller

** TODO **



### Steering wheel

 Our steering wheel has two potentiometers and a button. Following our will of keeping the modularity present in our code we are going to follow  the same logic as the joystick controller. 
 The potentiometer inside our wheel will be encoded as the joystick but only in the axis X. Following a mathematical conversion we are able to have the same values as the joystick. 

The lever has also a potentiometer but instead of having some values in the axis-Y, which is not really helpful in car games we are going to model our level as two buttons. If the lever is up- BTN A is HIGH, if the lever is down - BTN B is HIGH
 The button inside the lever is coded as before.

The string of bits that we will send to our raspberry pi will be as:

                                 XXXUUUUUUUUUUUXXXXXXXXXX
 The 3 MSB will be used to know if the buttons that we described before are HIGH. The 10 LSB are the encryption of the AXIS X of the potentiometer.
 The other bits are unused.
## Raspberry Pi

### Retropie

For this project, we used Retropie to run the emulators. Please follow this link to learn how to install Retropie on your Raspberry Pi. We recommend you using the Raspberry installation utiliy that can be found here in order to install it rapidly. Once you installed it, you will need to install some additional python libraires namely :
1. Py-Serial
2. Python-Uinput



### Main.py 

Once this is done, you can download the ```main.py``` script from our repository. This script will enable the communication between the arduino boards and Retropie. This script supports plug and play as well as unplug ! 
This section describes how the code works in case you are interested.

### Making it all work together

** TODO **



### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/TheCl3m/PortableArcade/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
