#!/usr/bin/env python2
"""
Helper script for staged roll-out for application updates on resin.io
"""
from __future__ import division
import sys
from random import shuffle

import click
from resin import Resin

resin = Resin()

@click.command()
@click.option('--number', '-n', type=click.INT, help="Number of devices to trigger the update on")
@click.option('--percent', '-p', type=click.INT, help="Percentage of fleet to trigger the update on")
@click.option('--token', '-t', envvar='TOKEN', required=True, help="Resin.io auth token, can specify it with the TOKEN env var as well")
@click.option('--quiet', '-q', is_flag=True, help="Toggles hiding process details")
@click.argument('app_id', required=True, nargs=1)
def trigger_update(app_id, number, percent, quiet, token):
    """Helper script for staged roll-out for application updates on resin.io

    Call it with a numerical APP_ID, and one of a number of devices (-n) or
    percentage of fleet (-p) to trigger update on. If no number added, then only
    query is run.

    Only triggers online, idle, not updated, not provisioning devices.
    """
    if number is None and percent is None:
        number = 0
    if number is not None and percent is not None:
        print("Please choose only number or percentage but not both!")
        sys.exit(1)

    # Authenticate with the resin API
    resin.auth.login_with_token(token)
    if not quiet:
        print("Logged in user: {}".format(resin.auth.who_am_i()))

    # Get app information, such as name and current commit hash
    application = resin.models.application.get_by_id(app_id)
    app_name, app_commit = application['app_name'], application['commit']
    if not quiet:
        print("App: {} / Commit: {}".format(app_name, app_commit))

    # Query devices and their status on this app
    devices = resin.models.device.get_all_by_application(app_name)
    fleet_size = len(devices)
    if percent:
        number = int(fleet_size / 100.0 * percent)  # round down
    eligible_devices = []
    if not quiet:
        print("=== Devices ===")
    for device in devices:
        # print(device)
        device_name = device['name']
        device_uuid = device['uuid']
        device_status = device['status']
        device_commit = device['commit']
        device_online = device['is_online']
        device_provisioning_state = device['provisioning_state']
        if device_online and device_status == 'Idle' and device_commit != app_commit and device_provisioning_state == '':
            eligible_devices += [device]
            colorstr = '\x1b[6;30;42m'  # Green
        else:
            colorstr = '\x1b[0;37;41m'  # Red
        if  not quiet:
            print("{}Device: {} {} / Commit: {} / Online: {} / Status: {}\x1b[0m".format(colorstr, device_name, device_uuid[:7], device_commit[:7], device_online, device_status))
    num_eligible = len(eligible_devices)
    if num_eligible < 1:
        if not quiet:
            print("There are no eligible devices to trigger update on.\n(either all updated, not online, or not idle).")
        sys.exit(0)
    update_count = number if number < num_eligible else num_eligible
    if not quiet:
        print("Number of eligible devices: {}".format(num_eligible))
        print("Devices to update         : {}".format(update_count))
    if update_count < 1:
        sys.exit(0)

    # Updating: select a random subset of devices and trigger the supervisor
    shuffle(eligible_devices)
    if not quiet:
        print("=== Updates ===")
    for i in range(update_count):
        device = eligible_devices[i]
        device_name = device['name']
        device_uuid = device['uuid']
        if not quiet:
            print("Updating: {} {}".format(device_name, device_uuid[:7]))
        resin.models.supervisor.update(device_uuid=device_uuid, app_id=app_id, force=True)

if __name__ == "__main__":
    trigger_update()
