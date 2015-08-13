# reBEAST

reBEAST is a utility script that updates the starting parameters in a BEAST 1.x XML file based on a tracelog from a previous BEAST run. It is useful for when:

* The cluster admin terminates your run because you accidentally ran it on the scratch node yet again
* You want to run your analysis for slightly longer but don't want to have to wait quite so long for it to get through burnin
* You were trying to spread some cream cheese on a bagel, but you bought the wrong, difficult-to-spread kind, so you brace the bagel against your computer but you lose your grip and your knife slips into the computer's vents and shorts the delicate electronics inside, ruining both your analysis and breakfast

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

Remove the first 5,000,000 states as burnin, and average the remaining posterior samples:

```
rebeast beast.xml beast.log --burnin 5000000
```

Create a file `restart.xml` with the last sampled state, as a poor man's checkpoint restart (since BEAST 1.x doesn't support checkpointing):

```
rebeast beast.xml beast.log --lastn 1 --output restart.xml
```

Combine samples from multiple tracelogs:

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
* This might actually be a bad idea. Ideally you would perform multiple analyses from a variety of different starting values and see if those randomized runs give you similar results. Though it's unlikely, starting your analysis from a peak of already high probability may give you a misleading or biased sample of the posterior. 

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
