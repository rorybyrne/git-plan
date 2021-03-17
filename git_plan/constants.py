"""Template utils

Author: Rory Byrne <rory@rory.bio>
"""


class DefaultTemplate:

    PLAN = """########### PLAN SUMMARY (50 chars) #############
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

    EDIT = """########### PLAN SUMMARY (50 chars) #############
%headline%
########### DETAILS #################################################
%body%
########### END ###########################################
# Edit your plan and save.
###########################################################
"""


DEFAULT_SETTINGS = {
    "template": {
        "edit": DefaultTemplate.EDIT,
        "plan": DefaultTemplate.PLAN
    },
    "project_root": None
}
