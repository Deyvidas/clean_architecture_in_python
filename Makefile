black:
	poetry run black -Sl 79 ~/dev/made_com
dependencies:
	cd ~/dev/made_com && sh gen_requirements.sh