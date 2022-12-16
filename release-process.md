
## Release Process

### 1. Build distribution archive

Find the current version number at [pypi](https://pypi.org/project/pybundlr/).

Open `pyproject.toml` in an editor, and update the value in `"version" = x.y.z`.

In terminal:

```console
#go to root of directory
cd ~/code/pybundlr

#ensure repo is up-to-date
git commit -am "Release x.y.z"
git push

#turn off virtual env't
deactivate

#ensure `dist/` folder is empty
rm -rf dist

#generate distribution archives: create `dist` folder with two files 
python -m build
```


### 2. Test the library, via test.pypi.org (optional)

In terminal:
```
#run twine to upload `dist` files to *test* pypi
python3 -m twine upload --repository testpypi dist/*

# -when prompted, give username: __token__
# -when prompted, given password: <*test* pypi API token>
```

Then, open a _different_ terminal, and:
```console
python -m venv venv
source venv/bin/activate
pip3 install -i https://test.pypi.org/simple/ pybundlr==<x.y.z>

#Then: go through "Using Pybundlr Library" section above
```

The updated test package will be [at test pypi](https://test.pypi.org/project/pybundlr/).

If things don't work, loop through steps 1-2 until they do.

### 3. Distribute to main pypi

In terminal:
```console
#run twine to upload `dist` files *main* pypi
python -m twine upload dist/*

# -when prompted, give username: __token__
# -when prompted, given password: <pypi API token>
```

Done! The updated package will be [at pypi](https://pypi.org/project/pybundlr/).

### Notes

This readme is a distillation of the [packaging-projects tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) at python.org.
