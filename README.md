# www.babycode.ca
#### Video Demo: https://youtu.be/cQVS18_0JDo
#### Description:

Babycode is a website where users capture baby memories in games. There are a variety of games where users can upload their family photos. The website will render their family photos into the game. Follow the instructions on the website and upload one photo per character. Our program running on OpenCV will remove the photo background and cartoonize the images. Finally, the processed images will be incorporated into the games. Then the user will be prompted for optional donation and the game download link.  The OpenCV AI algorithm is still at its growing stage. If users don't like how their images are rendered into the game. Users can also create an account and put in an order for human artists to draw the game characters.



## Installation

visit www.babycode.ca
Games downloaded are made by pycharm and rendered by Pyinstaller. Installation not required to play the game. However, when opening the game .exe file, users may be prompted by antivirus software that finds the pyinstaller.exe file as unknown. Game source code is in the downloaded folder incase user wants to review it before executing the game file. 

TODO:
Solve windows defender unknown publisher warning for downloaded games. 

## Codes/FrameWork

Django Frame is the backbone of the website. OpenCV and rembg.bg are two core python packages utilized to process user-uploaded images. Pygame is the package used for game development. Builtin email functions in Django are used for communicating with users. 
Various CDN such as bootstrap, stripe, crop, were used to make the site operational.
Domain name of website from NameCheap, HTTPS enabled by Lets Encrypt, RemoveServer setup at Linode. 


## Usage

1. Visit www.babycode.ca
2. Browse for games of interest and click. Games published as of Nov 07, 2021: FlappyBaba, CryBabyCry, and 123Jump
3. Read the game description and watch demo videos if desired.
4. Scroll to the bottom of the page and upload a photo for each character. 
5. Click the upload image button and wait. May take up to a minute due to the large volume of data processing. 
6. Download the game and unzip to play. Each game has their own unique play instructions which are available on the website. 

## Contributions

-CS50 OPENCOURSEWARE
-https://inventwithpython.com/ Opensource Python Books.
-ClearCode Youtube Channel on Pycharm tutorials 
-CoreySchafer Youtube Channel on Django tutorials.
-Dennis Ivy Youtube Channel on Stripe Payment tutorials. 
-My Wife gave me the free time for website development.


## ToDo Tasks:
- create contents: develop more games to publish.
- Market website
- Make the site more mobile friendly. ie allow users to play games directly on mobile.


## License
[BabyCode](www.babycode.ca)

