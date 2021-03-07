"""Exceptions

@author Rory Byrne <rory@rory.bio
"""


class CommandNotFound(Exception):
    """Command doesn't exist"""


class CommitAbandoned(Exception):
    """The user abandoned their commit"""
