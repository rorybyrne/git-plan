"""Template utils

Author: Rory Byrne <rory@rory.bio>
"""

PLAN_TEMPLATE = """########### PLAN SUMMARY (50 chars) #############
Insert headline
########### DETAILS #################################################
What does this commit do?
=========================
* Something

Why are we doing this?
======================
* Something

Notes
=====
########### END ###########################################
# Fill in the template with your planned work.
###########################################################
"""

EDIT_TEMPLATE = """########### PLAN SUMMARY (50 chars) #############
%headline%
########### DETAILS #################################################
%body%
########### END ###########################################
# Edit your plan and save.
###########################################################
"""


DEFAULT_SETTINGS = {
    "template": {"edit": EDIT_TEMPLATE, "plan": PLAN_TEMPLATE},
    "project_root": None,
    "label": "GP",
}

GIT_DIR = ".git"

GP_PROJECT_FNAME = "project.json"
GP_DIR = ".plan"
GP_PLANS_SUBDIR = "plans"
GP_PLAN_FILE_EXT = ".json"
