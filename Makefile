.PHONY: install clean git-plan

BASE_PYTHON=python3.8

BASE_DIR=${HOME}/.local
INSTALL_DIR=${BASE_DIR}/bin
SHARE_DIR=${BASE_DIR}/share/git-plan
SYSTEMD_DIR=${BASE_DIR}/share/systemd/user

EXEC_FILES=git-plan
EXEC_FILES+=gp
VERSION!=python setup.py --version
VERSION_FILE=git_plan/_version

check-env:
ifndef HOME
	$(error Environment variable HOME is undefined)
endif

check-dirs:
	@test -d $(BASE_DIR) || (echo "Missing $(BASE_DIR) directory, which is base directory" && exit 1)
	@test -d $(INSTALL_DIR) || (echo "Missing the install directory: $(INSTALL_DIR)" && exit 1)

install: version check-env check-dirs
	@echo "Installing to $(INSTALL_DIR)"
	@( \
		install -d $(INSTALL_DIR) && \
		install -m 0755 scripts/* $(INSTALL_DIR) && \
		ln -s $(INSTALL_DIR)/git-plan $(INSTALL_DIR)/gp && \
		install -d $(SHARE_DIR) && \
		$(BASE_PYTHON) -m venv $(SHARE_DIR)/venv && \
		$(SHARE_DIR)/venv/bin/python -m pip install -U pip && \
		$(SHARE_DIR)/venv/bin/python -m pip install .  && \
		echo "Install complete." \
	) || ( \
		echo "Install failed, rolling back..." && \
		$(MAKE) uninstall \
	)

clean_bin:
	@echo "Deleting executable files..."
	@test -d $(INSTALL_DIR) && \
		cd $(INSTALL_DIR) && \
		rm -f $(EXEC_FILES) && \
		echo "Done..."

clean_share:
	@echo "Deleting share files..."
	@test -d $(SHARE_DIR) && \
		rm -rf $(SHARE_DIR) && \
		echo "Done..." || \
		echo "No share directory found"


uninstall: clean_bin clean_share

reinstall: uninstall install

version:
	@echo "Generating version"
	@test -f $(VERSION_FILE) && \
		rm $(VERSION_FILE) && \
		echo "Removed old version file" || \
		echo "No version file found"
	echo $(VERSION) > $(VERSION_FILE)
