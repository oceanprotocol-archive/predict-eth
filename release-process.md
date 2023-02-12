
## Release Process

### 1. Build distribution archive

Find the current version number at [pypi](https://pypi.org/project/predict-eth/).

Open `pyproject.toml` in an editor, and update the value in `"version" = x.y.z`.

In terminal:

```console
#go to root of directory
cd ~/code/predict-eth

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

### 2. Distribute to pypi

In terminal:
```console
#run twine to upload `dist` files *main* pypi
python -m twine upload dist/*

# -when prompted, give username: __token__
# -when prompted, given password: <pypi API token>
```

Done! The updated package will be [at pypi](https://pypi.org/project/predict-eth/).

### Notes

This readme is a distillation of the [packaging-projects tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) at python.org.
