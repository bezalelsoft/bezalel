# How to run unit tests

```bash
# run tests
pytest

```


# How to deploy

https://packaging.python.org/en/latest/tutorials/packaging-projects/

## Run only once:
```shell
python -m pip install --upgrade build
python -m pip install --upgrade twine
```

TODO: generate token in PyPi and store it in laptop... 


## run every time to build package
```sh

python -m build

# for test
python -m twine upload --repository testpypi dist/*

# TODO: for prod
python -m twine upload dist/*

```
