[app]
title = Kolkata Weather
package.name = kolkata_weather
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png
fullscreen = 0
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.gradle_dependencies = com.android.support:support-compat:28.0.0
android.enable_androidx = True
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.arch = armeabi-v7a
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
[buildozer]
log_level = 2
warn_on_root = 1
