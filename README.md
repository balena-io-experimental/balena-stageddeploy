# stageddeploy

**Deprecated: see instead https://github.com/resin-io-playground/staged-releases**

Helper script for staged roll-out for application updates on resin.io. The script
uses the [Python SDK](https://github.com/resin-io/resin-sdk-python).

It's a proof-of-concept, non-production-quality script to showcase what can you
build with the SDK, so your mileage might vary!

## Usage

In your resin.io application enable the update lock on the devices by Creating
the `/data/resin-updates.lock` file, for example by running `touch /data/resin-updates.lock`
in your Dockerfile `CMD` step, or in your start script. That will block the
supervisor from updating the application on the device (still downloads the update,
though). The update is blocked until a call to the supervisor overrides this lock.
That can be done either though the device dashboard manually, or through the API.

Install the prerequisites by running `pip install -r requirements.txt` in the
source folder.

This script lets you define how many devices or what percentage of your fleet
you would like to trigger update on.

```
$./stageddeploy.py --help
Usage: stageddeploy.py [OPTIONS] APP_ID

  Helper script for staged roll-out for application updates on resin.io

  Call it with a numerical APP_ID, and one of a number of devices (-n) or
  percentage of fleet (-p) to trigger update on. If no number added, then
  only query is run.

  Only triggers online, idle, not updated, not provisioning devices.

Options:
  -n, --number INTEGER   Number of devices to trigger the update on
  -p, --percent INTEGER  Percentage of fleet to trigger the update on
  -t, --token TEXT       Resin.io auth token, can specify it with the TOKEN
                         env var as well  [required]
  -q, --quiet            Toggles hiding process details
  --help                 Show this message and exit.
```

Running the script without number values shows the current update status:

```
$ ./stageddeploy.py 126746
Logged in user: imrehg
App: MakerFaireDemo / Commit: ec6568e7153d1059e351bfd90caa48c0b70acf00
=== Devices ===
Device: B3 5577326 / Commit: 449385a / Online: True / Status: Idle
Device: B2 859eb5a / Commit: 4e7dedb / Online: True / Status: Idle
Device: A2 c3bcb2d / Commit: 4e7dedb / Online: True / Status: Idle
Device: B1 531a886 / Commit: ec6568e / Online: True / Status: Idle
Device: A1 4da60b4 / Commit: 4e7dedb / Online: True / Status: Idle
Device: A3 33adbe1 / Commit: 4e7dedb / Online: True / Status: Idle
Number of eligible devices: 5
Devices to update         : 0
```

Running it with a number or percentage will trigger an update:

```
$ ./stageddeploy.py 126746 -n 2
Logged in user: imrehg
App: MakerFaireDemo / Commit: ec6568e7153d1059e351bfd90caa48c0b70acf00
=== Devices ===
Device: B3 5577326 / Commit: 449385a / Online: True / Status: Idle
Device: B2 859eb5a / Commit: 4e7dedb / Online: True / Status: Idle
Device: A2 c3bcb2d / Commit: 4e7dedb / Online: True / Status: Idle
Device: B1 531a886 / Commit: ec6568e / Online: True / Status: Idle
Device: A1 4da60b4 / Commit: 4e7dedb / Online: True / Status: Idle
Device: A3 33adbe1 / Commit: 4e7dedb / Online: True / Status: Idle
Number of eligible devices: 5
Devices to update         : 2
=== Updates ===
Updating: B2 859eb5a
Updating: A3 33adbe1
```

## License

Copyright 2016 Resinio Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
