.PHONY: install clean git-plan

BASE_DIR=${HOME}/.local
INSTALL_DIR=${BASE_DIR}/bin
FILES_DIR=${BASE_DIR}/share/git-plan

EXEC_FILES=git-plan
SHARE_FILES=PLAN_MSG
PYTHON=python3.7-git-plan

install:
	@echo "Installing to $(INSTALL_DIR)"
	install -m 0755 scripts/* $(INSTALL_DIR)
	mkdir $(FILES_DIR)
	install -m 0644 share/* $(FILES_DIR)
	python3.7 -m venv $(FILES_DIR)/venv
	$(FILES_DIR)/venv/bin/python -m pip install .

uninstall:
	test -d $(INSTALL_DIR) && \
		cd $(INSTALL_DIR) && \
		rm -f $(EXEC_FILES) $(PYTHON)
	test -d $(FILES_DIR) && \
		rm -rf $(FILES_DIR)
