[app]

title = Portefeuille de Poche
package.name = portefeuille
package.domain = org.wallet

source.include_exts = py,png,jpg,kv,atlas,json
source.include_dir = .
source.exclude_exts = spec
source.exclude_dirs = tests, bin, venv

requirements = python3,kivy

orientation = portrait
android.permissions = INTERNET
fullscreen = 0
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_root = 1
