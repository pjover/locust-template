# locust-template

Locust performance test template for running locust tests for a REST service*

## Requirements and Installation

To run the Locust scripts you need Python 3.6 or later (developed and tested with 2.7.15) with `pip`, and the dependences specified in requirements.txt (specific versions of: locustio, gevent and Jinja2) which can be installed by running 

```
sudo apt install python3-pip
pip3 install -r requirements.txt
```

## Configuration

### Test URL

The default TEST URL `http://localhost:8085` is hardcoded in the scripts for quick testing. You should always use the locust **-H** command line argument to override this default value and specify the base URL you want to attack with your locust swarm.

### Timing

Locust tries to simulate real users, a great number of concurrent users with random behaviors including random timing. By default the simulated users wait between 0 and 500 milliseconds between requests (uniform random variable). These parameters can be changed by editing the `min_wait` and `max_wait` values at the end of each script. For maximum throughput, set both parameters to 0.

## Execution

### One server

After configuring the scripts, just run them with `locust`. For example to run the test TestOne against the URL http://my-url:8080/ run:

```
locust -f locustfile-TestOne.py -H http://my-url:8080/
```

After running this command, go to the URL printed by `locust`, by default http://localhost:8089/ and follow the on-screen instructions. You will be able to specify the number of clients to simulate and the ramp-up rate, and then lauch the tests and see the statistics in real time (as well as stop the tests when needed).


### Distributed execution

To run a cluster of Locust clients just add the argument `--master` to one of them, which will be the master, and `--slave --master-host=<master's IP>` to each of the slaves. The master will show the whole cluster's activity and statistics through its web interface.
