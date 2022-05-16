
# How to deploy

https://packaging.python.org/en/latest/tutorials/packaging-projects/

## Run only once:
```shell
py -m pip install --upgrade build
py -m pip install --upgrade twine
```

TODO: generate token in PyPi and store it in laptop... 


## run every time to build package
```sh

py -m build

# for test
py -m twine upload --repository testpypi dist/*

# TODO: for prod
py -m twine upload dist/*

```
