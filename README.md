<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/110315084-a7e39f80-8000-11eb-8a14-3799c7e2cfd3.png">
</p>
<p align="center">
  <b>A better workflow for git.</b>
</p>
<hr></hr>
<p align="center">
  <img src="https://github.com/synek/git-plan/workflows/Full%20Tests/badge.svg">
</p>
<p>
    Git plan inverts the git workflow so that you can write your commit message first, before you start writing code. 
    This makes it easier to plan your work and stay on-track.
</p>
<p>
    To use the tool, run <code>git plan init</code> (or simply <code>gp [command]</code>) to initialize, and then 
    <code>git plan add</code> to plan a new commit. Then when you have finished writing the code, use 
    <code>git plan commit</code> to use the plan as a template for your commit message.
</p>
<p>
    <b>This tool is in <b>early alpha</b> stage, so be careful and please make an issue or let me know if anything breaks.</b>
</p>

<h2>Installation</h2>
<p><code>python3.8</code> is required for now.</p>
<ol>
    <li><code>git clone https://github.com/synek/git-plan</code></li>
    <li><code>cd git-plan</code></li>
    <li><code>make install</code></li>
</ol>
<p>
    If you have trouble with the install, check what the <code>Makefile</code> is doing. Get in touch with me if you need help.
</p>
<p>
    To uninstall, run <code>make uninstall</code>
</p>

<h2>Usage</h2>
<ul>
  <li><code>git plan init</code> - initialize git plan in the <code>.plan/</code> directory</li>
  <li><code>git plan</code> - plan your first commit, or list existing plans</li>
  <li><code>git plan --version</code> - print the version</li>
  <li><code>git plan --help</code> - print the help</li>
  <li><code>git plan list [--long]</code> - list existing plans</li>
  <li><code>git plan add</code> - plan a new commit</li>
  <li><code>git plan edit</code> - edit an existing plan</li>
  <li><code>git plan delete</code> - delete an existing plan</li>
  <li><code>git plan commit</code> - commit one of your plans (launches <code>git commit -t <YOUR_PLAN></code> with your plan as a template)</li>
</ul>

<h2>Background</h2>
<p>
    Here is an interesting <a href="https://arialdomartini.wordpress.com/2012/09/03/pre-emptive-commit-comments/">blog post</a>
    about pre-emptive commit comments.
</p>

## Contributing

* Download and try it out
* Create an [issue](https://github.com/synek/git-plan/issues) if you find a problem or want to discuss something
* [Fork](https://guides.github.com/activities/forking/) the repository, fix a bug or add a feature, and open a PR

### Development

1. Install the dev requirements `pip install -r requirements_dev.txt`
2. Install the package in [develop mode](https://pip.pypa.io/en/stable/reference/pip_install/#install-editable) `pip install -e .`
3. Install the pre-commit hooks `pre-commit install -t pre-commit` and `pre-commit install -t pre-push`

### Hooks

Failure on any of the hooks will prevent the action taking place.

#### Pre-Commit

* [pylint](https://pylint.org/) on changed source files
* [mypy](http://mypy-lang.org/) on changed source files

#### Pre-Push

* [tox](https://tox.readthedocs.io/en/latest/) test suite runs
