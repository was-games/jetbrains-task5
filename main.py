TOKEN = "" # Your auth token
SERVER = "http://localhost:8111" # Your TeamCity Server address
ROOT = SERVER + "/app/rest/"
PROJECT_NAME = "test1" # Project name
VCS_ROOT = "https://github.com/JetBrains/teamcity-rest-client"
VCS_ROOT_ID = PROJECT_NAME + "_" + VCS_ROOT.replace(":", "").replace("/", "").replace(".", "").replace("-", "")

import http
import requests

class BlockAll(http.cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

s = requests.Session()
s.cookies.set_policy(BlockAll())

# Creating a project
data = {"parentProject": {
        "id": "_Root"
    },
    "name": PROJECT_NAME,
    "id": PROJECT_NAME,
    "copyAllAssociatedSettings": True}

response = s.post(ROOT + "projects", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

# Setting a VCS root
data = {
    "id": VCS_ROOT_ID,
    "name": VCS_ROOT,
    "vcsName": "jetbrains.git",
    "project": {
        "id": PROJECT_NAME
    },
    "properties": {
        "property": [
            {
                "name": "authMethod",
                "value": "ANONYMOUS"
            },
            {
                "name": "branch",
                "value": "refs/heads/master"
            },
            {
                "name": "url",
                "value": VCS_ROOT
            },
            {"name": "teamcity:branchSpec",
             "value": "project.branch.spec"
            }
        ]
    }
}

response = s.post(ROOT + "vcs-roots", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

data = {
  "name" : "project.branch.spec",
  "value" : "+:refs/heads/*"
}

response = s.post(ROOT + "projects/id:" + PROJECT_NAME + "/parameters", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

# Build configuration A
data = {
    "id": PROJECT_NAME + "_A",
    "name": "A",
    "project": {
        "id": PROJECT_NAME,
    },
    "settings": {
        "property": [
            {
                "name": "artifactRules",
                "value": "+:README.md"
            }
        ]
    }
}

response = s.post(ROOT + "buildTypes", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

data = {
	"id": VCS_ROOT_ID,
	"vcs-root": {
		"id": VCS_ROOT_ID
	}
}

response = s.post(ROOT + "buildTypes/id:" + PROJECT_NAME + "_A" + "/vcs-root-entries", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

# Build configuration B
data = {
    "id": PROJECT_NAME + "_B",
    "name": "B",
    "project": {
        "id": PROJECT_NAME,
    }
}

response = s.post(ROOT + "buildTypes", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

data = {
	"name": "CMD",
	"type": "simpleRunner",
	"properties": {
		"property": [
			{
				"name": "script.content",
				"value": "sleep 10"
			}
		]
	}
}

response = s.post(ROOT + "buildTypes/id:" + PROJECT_NAME + "_B" + "/steps", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

data = {
	"type": "equals",
	"properties": {
		"property": [
			{
				"name": "property-name",
				"value": "system.agent.name"
			},
			{
				"name": "property-value",
				"value": "Default Agent"
			}
		]
	}
}

response = s.post(ROOT + "buildTypes/id:" + PROJECT_NAME + "_B" + "/agent-requirements", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

# Build configuration C
data = {
    "id": PROJECT_NAME + "_C",
    "name": "C",
    "project": {
        "id": PROJECT_NAME,
    }
}

response = s.post(ROOT + "buildTypes", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

data = {
	"type": "snapshot_dependency",
	"properties": {
		"property": [
			{
				"name": "run-build-if-dependency-failed",
				"value": "RUN_ADD_PROBLEM"
			},
			{
				"name": "run-build-if-dependency-failed-to-start",
				"value": "MAKE_FAILED_TO_START"
			},
			{
				"name": "run-build-on-the-same-agent",
				"value": "false"
			},
			{
				"name": "sync-revisions",
				"value": "true"
			},
			{
				"name": "take-started-build-with-same-revisions",
				"value": "true"
			},
			{
				"name": "take-successful-builds-only",
				"value": "true"
			}
		]
	},
	"source-buildType": {
		"id": PROJECT_NAME + "_A"
	}
}

response = s.post(ROOT + "buildTypes/id:" + PROJECT_NAME + "_C" + "/snapshot-dependencies", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

data = {
	"type": "snapshot_dependency",
	"properties": {
		"property": [
			{
				"name": "run-build-if-dependency-failed",
				"value": "RUN_ADD_PROBLEM"
			},
			{
				"name": "run-build-if-dependency-failed-to-start",
				"value": "MAKE_FAILED_TO_START"
			},
			{
				"name": "run-build-on-the-same-agent",
				"value": "false"
			},
			{
				"name": "sync-revisions",
				"value": "true"
			},
			{
				"name": "take-started-build-with-same-revisions",
				"value": "true"
			},
			{
				"name": "take-successful-builds-only",
				"value": "true"
			}
		]
	},
	"source-buildType": {
		"id": PROJECT_NAME + "_B"
	}
}

response = s.post(ROOT + "buildTypes/id:" + PROJECT_NAME + "_C" + "/snapshot-dependencies", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

data = {
	"type": "artifact_dependency",
	"properties": {
		"property": [
			{
				"name": "cleanDestinationDirectory",
				"value": "false"
			},
			{
				"name": "pathRules",
				"value": "README.md"
			},
			{
				"name": "revisionBranch",
				"value": "+:refs/heads/main"
			},
			{
				"name": "revisionName",
				"value": "sameChainOrLastFinished"
			},
			{
				"name": "revisionValue",
				"value": "latest.sameChainOrLastFinished"
			}
		]
	},
	"source-buildType": {
		"id": PROJECT_NAME + "_A"
	}
}

response = s.post(ROOT + "buildTypes/id:" + PROJECT_NAME + "_C" + "/artifact-dependencies", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")

data = {
	"type": "vcsTrigger",
	"properties": {
		"property": [
			{
				"name": "branchFilter",
				"value": "+:refs/heads/master"
			},
			{
				"name": "enableQueueOptimization",
				"value": "true"
			},
			{
				"name": "quietPeriodMode",
				"value": "DO_NOT_USE"
			}
		]
	}
}

response = s.post(ROOT + "buildTypes/id:" + PROJECT_NAME + "_C" + "/triggers", json=data, auth=BearerAuth(TOKEN))
print(response.text)
print(" ")