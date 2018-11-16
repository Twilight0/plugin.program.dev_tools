# common.py - common functions
#
# Copyright 2016 kharts (https://github.com/kharts)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import xbmc
import xbmcaddon
import os
import json


this_addon = xbmcaddon.Addon()
addonID = this_addon.getAddonInfo("id")
addonName = this_addon.getAddonInfo("name")
addon_folder = xbmc.translatePath(this_addon.getAddonInfo("path"))


def error(message):
    """
    Opens notification window with error message
    :param: message: str - error message
    :return: None
    """

    header = "Error:"

    notify(header, message)


def info(message):
    """
    Opens info windows with message
    :param: message: str - message
    :return: None
    """

    header = "Info:"

    notify(header, message)


def notify(header, message):

    """
    Opens notification window with message
    :param: message: str - message
    :return: None
    """

    icon = ""  # os.path.join(addonFolder, "icon.png")

    xbmc.executebuiltin('XBMC.Notification("{0}","{1}",3000,"{2}")'.format(header, message, icon))


def debug(content):
    """
    Outputs content to log file
    :param content: content which should be output
    :return: None
    """
    try:
        if type(content) is str:
            message = unicode(content, "utf-8")
        else:
            message = content
    except NameError:
        message = content
    log(message, xbmc.LOGDEBUG)


def log_exception(content):
    """
    Outputs content to log file
    :param content: content which should be output
    :return: None
    """

    try:
        if type(content) is str:
            message = unicode(content, "utf-8")
        else:
            message = content
    except NameError:
        message = content
    log(message, xbmc.LOGERROR)


def log(msg, level=xbmc.LOGNOTICE):
    """
    Outputs message to log file
    :param msg: message to output
    :param level: debug levelxbmc. Values:
    xbmc.LOGDEBUG = 0
    xbmc.LOGERROR = 4
    xbmc.LOGFATAL = 6
    xbmc.LOGINFO = 1
    xbmc.LOGNONE = 7
    xbmc.LOGNOTICE = 2
    xbmc.LOGSEVERE = 5
    xbmc.LOGWARNING = 3
    """

    log_message = u'{0}: {1}'.format(addonID, msg)
    xbmc.log(log_message.encode("utf-8"), level)


def image(filename):
    """
    Construct full filename of the image, using short name
    and path to addon folder
    :param filename: short filename of the image
    :return: full filename of the image
    :rtype: str
    """

    return os.path.join(addon_folder, "resources", "img", filename)


def JSONRPC(method, params=None):
    """
    Execute JSON-RPC method
    :param method: name of the method. Example "Input.Back"
    :type method: str
    :param params: dictionary with parameter values
    :type params: dict
    :return: response as a string or None (in case of exception)
    :rtype: str or None
    """

    if params is None:
        params = {}

    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }

    command = json.dumps(data)

    try:

        response = xbmc.executeJSONRPC(command)

    except Exception as e:

        log_exception("Error executing JSON RPC method " + method)
        log_exception("Params: " + str(params))
        log_exception(str(e))

        return None

    return response
