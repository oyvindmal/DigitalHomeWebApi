# Digital Home Web API

### Endpoints
##### /
Index action. Does nothing
##### /test
To be removed, only used to test out url patterns
##### /telldus/sensor/ID
Get the temperature of a telldus sensor. Does not distinguish between temperature and non-temperature sensors and will fail if sensor doesnt have temperature. Replace id with sensor-id found via tdtool --list-sensor
##### /telldus/switches
Lists all switches defined in Telldus config

##### /telldus/switch/ID/ACTION
Preforms actions on a Telldus Switch. ID is is from /telldus/switches and allowed actions are on (turns on), off (turns off) and state (Displays the last sent/captured command for the switch. Which at the moment is the most accurate way to get the current state of the switch)

##### /sonos/players
Lists sonos players discovered on the network.

##### /sonos/xxx.xxx.xxx.xxx
Gets the current status of a Sonos player on the network. Find the ipadress via /sonos/players
##### /zones
Outputs the JSON datafile found in data/zones.json

