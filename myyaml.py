import yaml

def yamldef():
        with open('Userdata.yaml', 'r') as file:
            yamlSetting = yaml.safe_load(file)
        return yamlSetting