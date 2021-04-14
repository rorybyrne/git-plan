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
    "template": {
        "edit": EDIT_TEMPLATE,
        "plan": PLAN_TEMPLATE
    },
    "project_root": None,
    "label": "GP"
}
