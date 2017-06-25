# bbq-thermometer
A (hopefully) lightweight app for a thermometer based on the NTC C.H.I.P and MAX31855 thermocouple chips.

The system will probably be based on Django + Django Rest Framework for what concerns the server backend.
RESTful APIs will be implemented and the temperature graph visualization will be based on ChartJS.

For the "IOT" part a light Python routine will be used. It will gather data from the sensors and send it
to the backend probably using the requests library.
