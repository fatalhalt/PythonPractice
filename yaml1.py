import yaml
import pprint as pp

with open('config.yaml', "r") as f:
    yamlconfig = yaml.load(f, Loader=yaml.FullLoader)

#pp.pprint(yamlconfig)
#for i, d in yamlconfig.items():
#    print(i, ":", d)

print(yamlconfig['server']['users'][0]['ssh_key'])
