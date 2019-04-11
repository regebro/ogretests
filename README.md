Ogretests
=========

The idea of ogretests is to be able to create testing data easily for your application.

Setups should be doable in a readable text format,
so it's possible to understand what is going on in the test for a non-expert.
A setup should also be able to extend other setups,
so that you can easily extend and existing setup without copying all of it.
This means you end up with layered setups, hence the reference to ogres.

Once the setup is created, and all the data inserted in the database,
the data will be dumped out to tar files called "houses".
Future invocations of the same setup will load the data from these "houses" into the database,
bypassing the need to run the setups again, speeding up future test runs.

The intention is not just to speed up tests but also to support running user interface tests,
like browser tests on a remote machine.
You still need some way to load the houses into the database(s),
but you no longer need full access to the server software to create the data,
since that can be done on the server, and not the client.
