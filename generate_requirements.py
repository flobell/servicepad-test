import json

with open('Pipfile.lock') as f:
    lock_data = json.load(f)

requirements = lock_data['default'].items()
requirements_txt = '\n'.join([f"{package}{version}" for package, version in requirements])

with open('requirements.txt', 'w') as f:
    f.write(requirements_txt)