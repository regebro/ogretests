Ogretests
=========

Ogretests is a feasability study into two problems.

The first one is that enabling you to create testing data easily for your application,
in a manner that is easily readable for non-developers.

The second is that it client testing that doesn't run the client on the same machine as the server,
must have all test setup also done through the client.
Ogretests will help you make packages of database dumps that can be loaded onto the server database.
You still need a way for the client to make that load happen, but Ogretest provides a framework.

Context
-------

When running GUI tests, like Selenium etc, you typically have to automate the client to create all the testdata.
Since end user client tests are typically very slow, that helps slow down the testing a lot.

This can be solved by running the client tests on the server, but that's not always feasible.
In my current usecase, the server is a headless machine, and although we can run selenium with headless clients,
this makes it very hard to debug the test cases.
You want to run it locally, so you see what the test is doing.

But when you run it locally you don't have database access,
and can't even set up the correct admin user to log in and create the test user accounts.

Ogretests have test setups where you create the test data, and then dump that from the databases out in a local file.
Each test can then specify a specific test setup,
and do the test setup not by stepping through all the required steps,
but by loading these database dumps into the database.

For example, if you use Robotframework, whenever a test needs a particular setup,
if the setup hasn't changed, it will simply load the dump.
But if the test setup has changed, it will first recreate the dump,
although that will only work if run on the server.

Requirements
------------

* Setups should be doable in a readable text format,
  so it's possible to understand what is going on in the test for a non-expert.

* A setup should also be able to extend other setups,
  so that you can easily extend and existing setup without copying all of it.
  This means you end up with layered setups, hence the reference to ogres.

* Once the setup is created, and all the data inserted in the database,
  the data will be dumped out to tar files called "houses".

* Future invocations of the same setup will load the data from these "houses" into the database,
  bypassing the need to run the setups again, speeding up future test runs.

* The intention is not just to speed up tests but also to support running user interface tests,
  like browser tests on a remote machine.

* You still need some way to load the houses into the database(s),
  but you no longer need full access to the server software to create the data,
  since that can be done on the server, and not the client.
