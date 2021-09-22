#!/usr/bin/env python3

import json
import os
import requests

# TODO: Add deployment_tier to environments https://docs.gitlab.com/ee/ci/environments/index.html#deployment-tier-of-environments
# TODO: Send deployment tiers to different channels
# TODO: Use CI_JOB_STATUS with https://docs.gitlab.com/ee/ci/yaml/index.html#after_script
# TODO: Build logic for build status / color change
# TODO: Build logic for channel notification
# TODO: Build button URL to be able to approve deployment
# TODO: Send deployment requests to a separate channel
# TODO: Send metric to datadog? is there a gitlab integration? to track successful/failed builds over time, and duration?

CI_COMMIT_BRANCH     = os.getenv('CI_COMMIT_BRANCH')
CI_COMMIT_MESSAGE    = os.getenv('CI_COMMIT_MESSAGE')
CI_COMMIT_SHA        = os.getenv('CI_COMMIT_SHA')
CI_COMMIT_SHORT_SHA  = os.getenv('CI_COMMIT_SHORT_SHA')
CI_COMMIT_TITLE      = os.getenv('CI_COMMIT_TITLE')
CI_ENVIRONMENT_NAME  = os.getenv('CI_ENVIRONMENT_NAME')
CI_JOB_ID            = os.getenv('CI_JOB_ID')
CI_JOB_STATUS        = os.getenv('CI_JOB_STATUS')
CI_JOB_URL           = os.getenv('CI_JOB_URL')
CI_PROJECT_NAME      = os.getenv('CI_PROJECT_NAME')
CI_PROJECT_NAMESPACE = os.getenv('CI_PROJECT_NAMESPACE')
CI_PROJECT_URL       = os.getenv('CI_PROJECT_URL')
CI_PIPELINE_SOURCE   = os.getenv('CI_PIPELINE_SOURCE')
CI_SERVER_URL        = os.getenv('CI_SERVER_URL')
GITLAB_USER_LOGIN    = os.getenv('GITLAB_USER_LOGIN')
SLACK_WEBHOOK_URL    = os.getenv('SLACK_WEBHOOK_URL')
BUTTON_URL           = CI_SERVER_URL

DEPLOY_MESSAGE = "Deploy to {0} triggered by {1} - {2}".format(CI_ENVIRONMENT_NAME, CI_PIPELINE_SOURCE, CI_JOB_STATUS)
COMMIT_MESSAGE = "<{0}|{1}/{2}> commit to {3} with job <{4}|{5}> by <{6}/{7}|{7}>".format(CI_PROJECT_URL, CI_PROJECT_NAMESPACE, CI_PROJECT_NAME, CI_COMMIT_BRANCH, CI_JOB_URL, CI_JOB_ID, CI_SERVER_URL, GITLAB_USER_LOGIN)
HASH_MESSAGE   = "<{0}/-/commit/{1}|{2}> - {3}".format(CI_PROJECT_URL, CI_COMMIT_SHA, CI_COMMIT_SHORT_SHA, CI_COMMIT_TITLE)


HEADERS = {'Content-type': 'application/json'}

PAYLOAD = {
  "attachments": [
    {
      "color": "#36a64f",
      "blocks": [
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": DEPLOY_MESSAGE
          }
        },
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": COMMIT_MESSAGE
          }
        },
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": HASH_MESSAGE
          },
        },
      ]
    }
  ]
}

r = requests.post(SLACK_WEBHOOK_URL, headers=HEADERS, json=PAYLOAD)
print(r.content)
# print("STATUS: {0}".format(r.status_code))
# r.json()

# curl -X POST -H 'Content-type: application/json' --data "$JSON" 

        # {
        #   "type": "actions",
        #   "elements": [
        #     {
        #       "type": "button",
        #       "text": {
        #         "type": "plain_text",
        #         "text": "Deploy Me!",
        #       },
        #       "value": "deploy_value",
        #       "url": CI_SERVER_URL,
        #       "action_id": "actionId-0"
        #     }
        #   ]
        # }
