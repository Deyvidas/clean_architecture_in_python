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

mypy_check:	## Make mypy checking.
	poetry run mypy \
		--python-executable python \
		${root}

formating:	## Run make commands autoflake -> isort -> black -> mypy_check.
	make autoflake
	echo
	make isort
	echo
	make black
	echo
	make mypy_check

dependencies:	## Run script gen_requirements.sh that generate {type}_requirements.txt
	sh ${root}/gen_requirements.sh

before_commit: 	## Run scripts formatting -> run tests -> dependencies.
	make formating
	echo
	poetry run pytest ${root}
	echo
	make dependencies