<h1 align="center">git plan</h1>
<p align="center">
  <img src="https://github.com/synek/git-plan/workflows/Full%20Tests/badge.svg">
</p>
<p align="center">
A better workflow for git.
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/110201184-ae83e280-7e59-11eb-82a0-7b205d8a725b.png">
</p>

<p>
    Plan your commits before you start writing code.
</p>

<p>
    Staging files for a <code>git commit</code> is frustrating if you have to untangle your changes into
    multiple commits. The standard git workflow of "write code -> stage changes -> commit changes" encourages us to
    write code without thinking, and then punishes us when the time comes to commit.
</p>
<p>
    Now you can run <code>git plan</code> to write your commit message in advance, and then run <code>git plan commit</code>
    to use that message as a template for your commit once you're ready to commit.
</p>
<p>
    You can even run <code>git plan add</code> to add more pre-planned commits, and then choose which one you want to
    commit via <code>git plan commit</code>.
</p>
<p>
    <b>This tool is in <i>very early</i> alpha stages, so please make an issue or let me know if anything breaks.</b>
</p>

<h2>Installation</h2>
<p><code>python3.8</code> is required.</p>
<ol>
    <li><code>git clone https://github.com/synek/git-plan</code></li>
    <li><code>cd git-plan</code></li>
    <li><code>make install</code></li>
</ol>
<p>
    To uninstall, run <code>make uninstall</code>
</p>

<h2>Usage</h2>
<ul>
    <li><code>git plan</code> - plan your first commit, or list existing plans</li>
    <li><code>git plan help</code> - show the help message</li>
    <li><code>git plan list</code> - list existing plans</li>
    <li><code>git plan add</code> - plan a new commit</li>
    <li><code>git plan edit</code> - edit an existing plan</li>
    <li><code>git plan delete</code> - delete an existing plan</li>
    <li><code>git plan commit</code> - commit one of your plans (launches <code>git commit</code> with your plan as a template)</li>
</ul>

<h2>Contributing</h2>
<p>Give me a shout - rory@rory.bio</p>
