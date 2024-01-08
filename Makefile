root := ~/dev/made_com

help:	## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

black:	## Formats the code base.
	poetry run black \
		--skip-string-normalization \
		--line-length 79 \
		${root}

isort:	## Sort all imports.
	poetry run isort \
		--force-single-line-imports \
		--lines-after-imports 2 \
		${root}

autoflake:	## Delete all unused imports.
	poetry run autoflake \
		--recursive \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		${root}

formating:	## Run make commands isort -> autoflake -> black.
	make isort
	echo
	make autoflake
	echo
	make black

dependencies:	## Run script gen_requirements.sh that generate {type}_requirements.txt
	sh ${root}/gen_requirements.sh