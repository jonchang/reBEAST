# reBEAST

reBEAST is a utility script that updates the starting parameters in a BEAST 1.x XML file based on a tracelog from a previous BEAST run.

## Installing

reBEAST is written in pure Python and has no dependencies. It should work on any version of Python 2.7.

The recommended installation method uses `pip`:

```
pip install https://github.com/jonchang/reBEAST/archive/master.zip
rebeast --help
```

You can also just download the Python script and run it directly, though this is not recommended:

```
curl -O https://raw.githubusercontent.com/jonchang/reBEAST/master/rebeast/rebeast.py
python rebeast.py --help
```

## Examples

Write a new XML file `beast.rebeast.xml` based on the average of posterior samples from `beast.log` and the original XML file `beast.xml`

```
rebeast beast.xml beast.log
```

Removes the first 5,000,000 states as burnin, and averages the remaining posterior samples:

```
rebeast beast.xml beast.log --burnin 5000000
```

Creates a file `restart.xml` with the last sampled state, as a poor man's checkpoint restart (since BEAST 1.x doesn't support checkpointing):

```
rebeast beast.xml beast.log --lastn 1 --output restart.xml
```

Combines samples from multiple tracelogs:

```
rebeast beast.xml run1_beast.log run2_beast.log
```

Use the default values of the HKY model, instead of the sampled values:

```
rebeast beast.xml beast.log --ignore hky.kappa
```

Use the default values for all HKY models (if you have a lot of partitions):

```
rebeast beast.xml beast.log --ignore-tag hkyModel
```

## Caveats

* Not tested on BEAST 2, but based on the BEAST 2 XML files I've seen I don't see a reason why it wouldn't work.
* Certain parameters don't like it when you put a sampled value as their initial value. In this case, use `--ignore` or `--ignore-tag` to exclude these misbehavers. They will typically lead to an XML parse error or -Inf log-likelihood on first run.
* May mangle the whitespace or comments in your XML file.

## Developing

```
git clone https://github.com/jonchang/reBEAST.git
cd reBEAST
virtualenv env
source env/bin/activate
./setup.py develop
```

## License

This software is licensed under the [GNU Affero GPL](http://choosealicense.com/licenses/agpl-3.0/). For more information, see the `LICENSE` file.

## References

* [BEAST software](http://beast.bio.ed.ac.uk/)
