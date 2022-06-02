Signals
=======

RoundBox includes a "signal dispatcher" which helps decoupled applications get notified when actions occur elsewhere in
the framework. In a nutshell, signals allow certain *senders* to notify a set of *receivers* that some action has
taken place. They're especially useful when many pieces of code may be interested in the same events.

***

### Listening to signals

To receive a signal, register a *receiver* function using the `#!python Signal.connect()` method. The receiver function is called
when the signal is sent. All the signal's receiver functions are called one at a time, in the order they were registered.

- Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)

  * *receiver* The callback function which will be connected to this signal.
               See `receiver-functions` for more information.

  * *sender* Specifies a particular sender to receive signals from.
               See`connecting-to-specific-signals` for more information.

  * *weak* RoundBox stores signal handlers as weak references by default. Thus, if your receiver is a local
                   function, it may be garbage collected. To prevent this, pass ``weak=False`` when you call
                   the signal's ``#!python connect()`` method.

  * *dispatch_uid* A unique identifier for a signal receiver in cases where duplicate signals may be sent. See
                             `preventing-duplicate-signals` for more information.

***

### Receiver functions

First, we need to define a receiver function. A receiver can be any Python function or method:

```python
def my_callback(sender, **kwargs):
    print("Request finished!")
```

Notice that the function takes a ``sender`` argument, along with wildcard keyword arguments (``**kwargs``);
all signal handlers must take these arguments.

We'll look at senders `a bit later`, but right now look at the ``**kwargs``
argument. All signals send keyword arguments, and may change those keyword arguments at any time. In the case of
`~RoundBox.core.signals.request_finished`, it's documented as sending no arguments, which means we might be tempted to
write our signal handling as ``my_callback(sender)``.

This would be wrong -- in fact, Django will throw an error if you do so. That's because at any point arguments could
get added to the signal and your receiver must be able to handle those new arguments.

***

### Connecting receiver functions

There are two ways you can connect a receiver to a signal. You can take the
manual connect route:

```python
from RoundBox.core.signals import request_finished

request_finished.connect(my_callback)
```

Alternatively, you can use a `receiver` decorator:


Here’s how you connect with the decorator:

```python
from RoundBox.core.signals import request_finished
from RoundBox.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")
```

Now, our ``my_callback`` function will be called each time a request finishes.

!!! note "Where should this code live?"
    Strictly speaking, signal handling and registration code can live anywhere you like

    In practice, signal handlers are usually defined in a ``signals`` submodule of the application they relate to.
    Signal receivers are connected in the `~RoundBox.apps.AppConfig.ready` method of your application
    `configuration class`. If you're using the `receiver` decorator,
    import the ``signals`` submodule inside `~RoundBox.apps.AppConfig.ready`, this will implicitly
    connect signal handlers:

    ```python
        from RoundBox.apps import AppConfig
        from RoundBox.core.signals import request_finished

        class MyAppConfig(AppConfig):
            ...

            def ready(self):
                # Implicitly connect a signal handlers decorated with @receiver.
                from . import signals
                # Explicitly connect a signal handler.
                request_finished.connect(signals.my_callback)
    ```

!!! Note
    The `~RoundBox.apps.AppConfig.ready` method may be executed more than once during testing, so you may want to
    `guard your signals from duplication`, especially if you're planning
    to send them within tests.

***

### Connecting to signal's sent by specific senders

Some signals get sent many times, but you'll only be interested in receiving a
certain subset of those signals.

***

### Preventing duplicate signals

In some circumstances, the code connecting receivers to signals may run multiple times.
This can cause your receiver function to be registered more than once, and thus called as many times for a signal event.
For example, the `~RoundBox.apps.AppConfig.ready` method may be executed more than once during testing.
More generally, this occurs everywhere your project imports the module where you define the signals,
because signal registration runs as many times as it is imported.

If this behavior is problematic, pass a unique identifier as the ``dispatch_uid`` argument to identify your receiver
function. This identifier will usually be a string, although any hashable object will suffice.
The end result is that your receiver function will only be bound to the signal once for each unique ``dispatch_uid``
value:

```python
from RoundBox.core.signals import request_finished

request_finished.connect(my_callback, dispatch_uid="my_unique_identifier")
```

***

### Defining and sending signals

Your applications can take advantage of the signal infrastructure and provide its own signals.

!!! note "When to use custom signals"
    Signals are implicit function calls which make debugging harder.
    If the sender and receiver of your custom signal are both within your project,
    you're better off using an explicit function call.

### Defining signals

> Signal()

All signals are `RoundBox.dispatch.Signal` instances.

For example:

```python
import RoundBox.dispatch

pizza_done = RoundBox.dispatch.Signal()
```

This declares a ``pizza_done`` signal.

### Sending signals

> Signal.send(sender, **kwargs)
>
> Signal.send_robust(sender, **kwargs)

To send a signal, call either `Signal.send` (all built-in signals use this) or `Signal.send_robust`.
You must provide the ``sender`` argument (which is a class most of the time) and may provide as many other keyword
arguments as you like.

For example, here's how sending our ``pizza_done`` signal might look:

```python
class PizzaStore:
        ...

        def send_pizza(self, toppings, size):
            pizza_done.send(sender=self.__class__, toppings=toppings, size=size)
            ...
```

Both ``send()`` and ``send_robust()`` return a list of tuple pairs``[(receiver, response), ... ]``,
representing the list of called receiver functions and their response values.

``send()`` differs from ``send_robust()`` in how exceptions raised by receiver functions are handled. ``send()``
does *not* catch any exceptions raised by receivers; it simply allows errors to propagate. Thus not all receivers may
be notified of a signal in the face of an error.

``send_robust()`` catches all errors derived from Python's ``Exception`` class, and ensures all receivers are notified
of the signal. If an error occurs, the error instance is returned in the tuple pair for the receiver that raised the error.

The tracebacks are present on the ``__traceback__`` attribute of the errors returned when calling ``send_robust()``.

***

### Disconnecting signals

> Signal.disconnect(receiver=None, sender=None, dispatch_uid=None)

To disconnect a receiver from a signal, call `Signal.disconnect`. The arguments are as described in
`.Signal.connect`. The method returns``True`` if a receiver was disconnected and ``False`` if not.

The ``receiver`` argument indicates the registered receiver to disconnect. It may be ``None`` if ``dispatch_uid``
is used to identify the receiver.

***
