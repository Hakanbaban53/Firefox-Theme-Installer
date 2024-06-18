
<h1 align="center">
  <br>
  <a><img src="assets/Preview_Images/home_page.png" alt="RealFire Installer" width="800"></a>
  <br>
  RealFire Installer
  <br>
</h1>

<h4 align="center">A minimal Firefox theme installer written with <a href="https://www.python.org" target="_blank">Python</a>.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#build-for-testing">Build For Testing</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

## Key Features


* Cross platform
  - Windows, macOS and Linux ready.

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), Python and some python libraries installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/Hakanbaban53/RealFire-Installer

# Go into the repository
$ cd RealFire-Installer

# Install dependencies
$ pip3 install customtkinter tk pillow requests

# Run the app
$ python ./main.py
```
> **Note 1**
> If App want to admin request urn the line [here](https://github.com/Hakanbaban53/RealFire-Installer/blob/c2f6685af88cb3729435ab97fbaea4b7cbdf59a9/main.py#L19C9-L21C19) into a comment line.


> **Note 2**
> If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `Python` from the command prompt.



## Build For Testing

To clone and run this application, you'll need [Git](https://git-scm.com), Python and some python libraries installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/Hakanbaban53/RealFire-Installer

# Go into the repository
$ cd RealFire-Installer

# Install dependencies
$ pip3 install customtkinter tk pillow requests pyinstaller

# Build the app
$ pyinstaller --onefile .\main.py --icon=../RealFire-Installer/assets/icons/firefox.ico --add-data "../RealFire-Installer/data/installer_data.json:data" --add-data "../RealFire-Installer/assets/icons;assets/icons" --add-data "..\RealFire-Installer\assets\backgrounds;assets\backgrounds"
```

> **Note**
> If you want to launch with no console add the '--noconsole' argument.

## Download



## Emailware



## Credits





## License

MIT

---

