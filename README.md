<h1 align="center">git plan</h1>
<p align="center">
  <img src="https://github.com/synek/git-plan/workflows/Full%20Tests/badge.svg">
</p>
<p align="center">
A better workflow for git.
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/110315084-a7e39f80-8000-11eb-8a14-3799c7e2cfd3.png">
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
    <li><code>git plan init</code> - initialize git plan in the current .git/ directory</li>
    <li><code>git plan [--long]</code> - plan your first commit, or list existing plans</li>
    <li><code>git plan help</code> - show the help message</li>
    <li><code>git plan list [--long]</code> - list existing plans</li>
    <li><code>git plan add</code> - plan a new commit</li>
    <li><code>git plan edit</code> - edit an existing plan</li>
    <li><code>git plan delete</code> - delete an existing plan</li>
    <li><code>git plan commit</code> - commit one of your plans (launches <code>git commit</code> with your plan as a template)</li>
</ul>

<h2>Background</h2>
<p>
    Here is an interesting <a href="https://arialdomartini.wordpress.com/2012/09/03/pre-emptive-commit-comments/">blog post</a>
    about pre-emptive commit comments.
</p>

<h2>Contributing</h2>
<p>Give me a shout - rory@rory.bio or @ryrobyrne</p>
