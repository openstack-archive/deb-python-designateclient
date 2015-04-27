Contributing
============

Code is hosted `on GitHub`_. Submit bugs to the Designate Client project on
`Launchpad`_. Submit code to the openstack/python-designateclient project using
`Gerrit`_.

.. _on GitHub: https://github.com/stackforge/python-designateclient
.. _Launchpad: https://launchpad.net/python-designateclient
.. _Gerrit: http://wiki.openstack.org/GerritWorkflow

Here's a quick summary:

Install the git-review package to make life easier

.. code-block:: shell-session

  pip install git-review

Branch, work, & submit:

.. code-block:: shell-session

  # cut a new branch, tracking master
  git checkout --track -b bug/id origin/master
  # work work work
  git add stuff
  git commit
  # rebase/squash to a single commit before submitting
  git rebase -i
  # submit
  git-review

