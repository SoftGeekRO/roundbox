### How do I get started?

- [Download the code]
- Install RoundBox
- Check out the rest of the documentation, and [ask questions] if you run into trouble.

## What are RoundBox's prerequisites?

RoundBox requires [Python]. See the table in the next question for the versions of
Python that work with each version of RoundBox. Other Python libraries may be
required for some use cases, but you'll receive an error about them as they're
needed.

[Download the code]: https://github.com/soulraven/roundbox/archive/refs/heads/main.zip
[ask questions]: https://github.com/soulraven/roundbox/discussions
[Python]: https://www.python.org/

## What Python version can I use with RoundBox?

| RoundBox version | Python versions |
|------------------|-----------------|
| 1.0              | >=3.10          |

For each version of Python, only the latest micro release (A.B.C) is officially supported.
You can find the latest micro version for each series on the [Python download page].

[Python download page]: https://www.python.org/downloads/

## What Python version should I use with RoundBox?

Since newer versions of Python are often faster, have more features, and are
better supported, the latest version of Python 3 is recommended.

You don't lose anything in RoundBox by using an older release, but you don't take
advantage of the improvements and optimizations in newer Python releases.
Third-party applications for use with RoundBox are free to set their own version
requirements.

## Should I use the stable version or development version?

Generally, if you're using code in production, you should be using a
stable release. The RoundBox project publishes a full stable release
every nine months or so, with bugfix updates in between. These stable
releases contain the API that is covered by our backwards
compatibility guarantees; if you write code against stable releases,
you shouldn't have any problems upgrading when the next official
version is released.
