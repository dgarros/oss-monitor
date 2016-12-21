import requests
import boto3
import yaml


projects_url = "https://raw.githubusercontent.com/dgarros/oss-monitor/master/projects.yaml"
projects_local = 'projects.yaml'
namespace = 'oss-monitor'
use_github = True

def load_project_list(github=True):

  projects_raw = ''

  if github:
    r = requests.get( projects_url )
    if r.status_code != 404:
      projects_raw = r.content

  else:
    import os
    projects_raw = open(projects_local).read()

  projects = yaml.load(projects_raw)
  return projects

def lambda_handler(event, context):

  cloudwatch = boto3.client('cloudwatch')

  ## Load projects list from a Yaml file, either locally or from Github
  repos = load_project_list(github=use_github)

  ## For each Github repos, collect the number of start and publish in Github
  for repo in repos['github']:

    url = "https://api.github.com/repos/{0}".format(repo)
    r = requests.get( url )

    if r.status_code != 404:
      resources = r.json()
      print "{0}: {1}".format(resources['full_name'], resources['stargazers_count'] )

      cloudwatch.put_metric_data(
        Namespace=namespace,
        MetricData=[ { 'MetricName': resources['full_name'], 'Value': resources['stargazers_count'], 'Unit': 'Count' }]
      )

if __name__ == "__main__":

    use_github = False
    lambda_handler(None, None)
