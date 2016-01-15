import os
import urllib
import urllib2
import json
 
redmineUrl = os.environ.get("REDMINE_URL")
redmineProject = os.environ.get("REDMINE_PROJECT")
redmineKey = os.environ.get("REDMINE_KEY")
redmineProjectId = os.environ.get("REDMINE_PROJECT_ID")
redmineRelationProjectId = os.environ.get("REDMINE_RELATION_PROJECT_ID")

query = {}
query['key'] = redmineKey
query['limit'] = '100'
query['status_id'] = '*'
query['sort'] = 'updated_on:desc'
url = "%sprojects/%s/issues.json?%s" % (redmineUrl, redmineProject, urllib.urlencode(query))
response = urllib2.urlopen(url)
issues = json.loads(response.read())

def request(id):
    query = {}
    query['key'] = redmineKey
    query['include'] = 'relations'
    url = "%sissues/%s.json?%s" % (redmineUrl, id, urllib.urlencode(query))
    response = urllib2.urlopen(url)
    return json.loads(response.read())

for i in issues['issues']:
    issue = request(i.get('id'))['issue']
    if issue.get('custom_fields') is not None:
        flg = issue.get('custom_fields')[0].get('value')
        if flg == '1':
            continue
    relations = issue.get('relations')
    entryFlg = False
    if relations is not None:
        for n in relations:
            relationId = n.get('issue_to_id')
            relation = request(relationId)['issue']
            if str(relation['project']['id']) != str(redmineRelationProjectId):
                entryFlg = True
    if entryFlg is False:
        print '#%s %s' % (issue['id'], issue['subject'])
