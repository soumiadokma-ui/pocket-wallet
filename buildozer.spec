[app]

# (str) Title of your application
title = Portefeuille de Poche

# (str) Package name
package.name = portefeuille

# (str) Package domain (needed for android packaging)
package.domain = org.wallet

# (list) Source files to include (let it empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Source files to include (let it empty to include all)
source.include_dir = .

# (list) List of inclusion/exclusion patterns
source.exclude_exts = spec

# (list) List of exclusions using pattern matching
source.exclude_dirs = tests, bin, venv

# (list) Application requirements
# تأكد من إضافة المكتبات التي يعتمد عليها تطبيقك هنا
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (list) The permissions for your application
android.permissions = INTERNET

# (str) Supported orientations (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android SDK version to use
# android.sdk = 20

# (str) Android NDK version to use
# android.ndk = 25b

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_root = 1
