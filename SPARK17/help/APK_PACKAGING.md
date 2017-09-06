## steps followed to make and sign an apk for android

```
cordova create myapk com.expeyes.help ExpEYES17Docs

cd myapk
cordova platform add android
```

### Adding paths to android sdk, gradle, build tools. Your paths may be different. Restart terminal after / `source ~/.bashrc`

```
export PATH=$PATH:~/Downloads/android-studio/gradle/gradle-3.2/bin/:~/Android/Sdk/platform-tools/
export PATH=$PATH:~/Android/Sdk/tools/
export ANDROID_HOME=~/Android/Sdk/
export ORG_GRADLE_PROJECT_cdvMinSdkVersion=18
```

### Running the apk
The following step builds and loads an apk to a connected android device

```
cd myapk
cordova run --platform=android
```

### Making a key , if you don't have one
filename : cordova.keystore . key-alias : mycordovakey . validity : in days

` keytool -genkey -v -keystore cordova.keystore -alias mycordovakey -validity 3650`

### Signing the apk
cd to the apk folder

`jarsigner -verbose -keystore cordova.keystore android-release-unsigned.apk mycordovakey`

Your APK is now signed, and can be copied to an android phone and installed.

### Debugging the cordova app.


+ go to the cordova folder, and run cordova which will automatically use the files in ../dist, and install the apk on a connected device

`cd myapk`

` cordova run --platform=android`

+ use chrome inspector to remotely inspect your app via your desktop's chrome window. it's awesome!

  + open chrome.
  + go to chrome://inspect
  + If you see your device, click on `inspect` , and you'll be able to see a copy of your phone's screen in your browser along with JS console, components, and even keyboard/mouse input.


