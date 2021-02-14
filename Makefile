.PHONY: install clean git-plan

BASE_DIR=${HOME}/.local
INSTALL_DIR=${BASE_DIR}/bin
FILES_DIR=${BASE_DIR}/share/git-plan
SYSTEMD_DIR=${BASE_DIR}/share/systemd/user

EXEC_FILES=git-plan
SHARE_FILES=PLAN_MSG
SERVICE_FILE=gitplan-oracle.service
PYTHON=python3.7-git-plan

install:
	@echo "Installing to $(INSTALL_DIR)"
	install -d $(INSTALL_DIR)
	install -m 0755 scripts/* $(INSTALL_DIR)
	install -d $(FILES_DIR)
	install -m 0644 share/PLAN_MSG $(FILES_DIR)
	install -d $(SYSTEMD_DIR)
	install -m 0644 share/$(SERVICE_FILE) $(SYSTEMD_DIR)
	python3.7 -m venv $(FILES_DIR)/venv
	$(FILES_DIR)/venv/bin/python -m pip install -U pip
	$(FILES_DIR)/venv/bin/python -m pip install .
	#systemctl --user enable $(SERVICE_FILE) --now

uninstall:
	@echo "Deleting executable files..."
	@test -d $(INSTALL_DIR) && \
		cd $(INSTALL_DIR) && \
		(test -e $(EXEC_FILES) || echo "No executable files found") && \
		rm -f $(EXEC_FILES) $(PYTHON) && \
		echo "Done..."
	@echo "Deleting share files..."
	@test -d $(FILES_DIR) && \
		rm -rf $(FILES_DIR) && \
		echo "Done..." || \
		echo "No share directory found"
	@echo "Deleting service file..."
	@systemctl --user disable $(SERVICE_FILE) --now || echo "Attempting to remove service file anyway..."
	@test -d $(SYSTEMD_DIR) && \
		cd $(SYSTEMD_DIR) && \
		rm -f $(SERVICE_FILE) && \
		echo "Done." || \
		echo "Could not delete service file."

reinstall: uninstall install

observe:
	@echo "Starting oracle..."
	@/home/rory/.local/share/git-plan/venv/bin/python -m git_plan.__oracle__
