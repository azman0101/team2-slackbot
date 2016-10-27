# -----------------------------------------------------------------------------
# docker-slackbot
#
# Builds a basic docker image that can run a slack bot
# (http://teamspeak.com/).
#
# Authors: Simon Watier
# Updated: October 26th, 2016
# Require: Docker (http://www.docker.io/)
# -----------------------------------------------------------------------------

# Base system is the LTS version of Debian.
FROM   debian:latest

# Make sure we don't get notifications we can't answer during building.
ENV    DEBIAN_FRONTEND noninteractive

# Download and install everything from the repos.
RUN    apt-get --yes update; apt-get --yes upgrade
RUN    apt-get --yes install curl python-pip
RUN    pip install slackclient

# Env variables


# Load in all of our config files.
ADD    ./scripts/slackbot.py /slackbot.py

# Fix all permissions
RUN    chmod +x /slackbot.py

# expose the slackbot port.
EXPOSE 6000

CMD   ["python /skackbot.py"]
