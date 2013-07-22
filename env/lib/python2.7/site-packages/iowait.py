# Copyright (C) 2011  Andrea Corbellini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Platform-independent module for I/O completion events.

This module provides objects to watch file descriptors for I/O events. The
objects have all the same interface and work in the same way in every platform.
The only limitation of this module is that, on Windows, it only works for
sockets.

This module defines the following classes:

* SelectIOWait -- based on the select() system call;
* PollIOWait -- based on poll();
* EPollIOWait -- based on epoll();
* KQueueIOWait -- based on kqueue().

In addition, IOWait is also defined. It is a reference to the best
implementation available for the current platform (for example, it references
EPollIOWait on Linux and KQueueIOWait on FreeBSD).

The functions poll(), epoll() and kqueue() are not available on all operating
systems, so not all the classes defined by this module can be used on every
platform. For this reason, it is recommended to always use IOWait instead of
referencing the other classes directly.

Every IOWait-like object in this module provide the following methods:

* watch(file[, read[, write]])

  Register the given file object. The type of event to wait for can be
  specified using the boolean read and write parameters (both False by
  default).

  If the file is already registered, just the type of event to wait for is
  changed. If neither read nor write is specified, ValueError is raised.

* unwatch(file)

  Remove the given file object from the list of registered files. If the file
  isn't registered, ValueError is raised.

* wait([timeout])

  Wait for the events registered using watch(). This function returns a list
  containing items in this format: (file, read, write). file is a file object,
  read and write are two booleans that specify whether the file is ready to be
  read or written without blocking.

  The optional timeout argument specifies the time-out as a float in seconds.
  If not specified or None, the function will block until at least an event is
  received.

  If no files are registered, ValueError is raised.

In addition, the attribute available is also defined. When True, the class can
be used without problems, else the class won't work. Its value varies depending
on the platform (for example, EPollIOWait.avaliable is True on Linux, but False
on all other platforms).
"""

import select

__all__ = [
    'IOWait', 'SelectIOWait', 'PollIOWait', 'EPollIOWait', 'KQueueIOWait']


class SelectIOWait(object):
    """Implementation based on the select() system function."""

    # select() is assumed to be always available.
    available = True

    def __init__(self):
        self._rlist = []
        self._wlist = []
        self._files_map = {}

    def watch(self, fileobj, read=False, write=False):
        if not (read or write):
            raise ValueError('either read or write must be specified')

        if hasattr(fileobj, 'fileno'):
            fileno = fileobj.fileno()
        else:
            fileno = fileobj

        files_map = self._files_map
        try:
            old_fileobj, old_read, old_write = files_map[fileno]
        except KeyError:
            # This is the first time this file is registered.
            if read:
                self._rlist.append(fileno)
            if write:
                self._wlist.append(fileno)
        else:
            # The file has already been registered.
            if read:
                if not old_read:
                    self._rlist.append(fileno)
            elif old_read:
                self._rlist.remove(fileno)
            if write:
                if not old_write:
                    self._wlist.append(fileno)
            elif old_write:
                self._wlist.remove(fileno)

        files_map[fileno] = (fileobj, bool(read), bool(write))

    def unwatch(self, fileobj):
        if hasattr(fileobj, 'fileno'):
            fileno = fileobj.fileno()
        else:
            fileno = fileobj

        _, read, write = self._files_map.pop(fileno)
        if read:
            self._rlist.remove(fileno)
        if write:
            self._wlist.remove(fileno)

    def wait(self, timeout=None):
        files_map = self._files_map
        if not files_map:
            raise ValueError('no file descriptors registered')

        # Call select().
        rlist, wlist, _ = select.select(self._rlist, self._wlist, (), timeout)

        # Look first in rlist to build the result.
        result = []
        for fileno in rlist:
            fileobj = files_map[fileno][0]
            # Check whether this file descriptor is also in wlist.
            try:
                wlist.remove(fileno)
            except ValueError:
                result.append((fileobj, True, False))
            else:
                result.append((fileobj, True, True))

        # Look for the remaining file descriptors in wlist.
        for fileno in wlist:
            fileobj = files_map[fileno][0]
            result.append((fileobj, False, True))

        return result


class PollIOWait(object):
    """Implementation based on the poll() system function.

    Not available on all platforms.
    """

    available = hasattr(select, 'poll')

    def __init__(self):
        self._files_map = {}
        self._poll = select.poll()
        self._read_mask = select.POLLIN | select.POLLPRI
        self._write_mask = select.POLLOUT

    def watch(self, fileobj, read=False, write=False):
        if not (read or write):
            raise ValueError('either read or write must be specified')

        event = self._read_mask if read else 0
        if write:
            event |= self._write_mask

        if hasattr(fileobj, 'fileno'):
            fileno = fileobj.fileno()
        else:
            fileno = fileobj

        poll = self._poll
        try:
            poll.modify(fileno, event)
        except IOError:
            poll.register(fileno, event)

        self._files_map[fileno] = fileobj

    def unwatch(self, fileobj):
        if hasattr(fileobj, 'fileno'):
            fileno = fileobj.fileno()
        else:
            fileno = fileobj

        del self._files_map[fileno]
        self._poll.unregister(fileno)

    def wait(self, timeout=None):
        files_map = self._files_map
        if not files_map:
            raise ValueError('no file descriptors registered')

        # Call poll().
        timeout = timeout if timeout is not None else -1
        poll_result = self._poll.poll(timeout)

        # Build and return the result.
        read_mask = self._read_mask
        write_mask = self._write_mask
        return [
            (files_map[fileno],
             bool(event & read_mask),
             bool(event & write_mask))
            for fileno, event in poll_result]


class EPollIOWait(PollIOWait):
    """Implementation based on the epoll() system function.

    This is a subclass of PollIOWait. Only supported on Linux 2.5.44 and newer.
    """

    available = hasattr(select, 'epoll')

    def __init__(self):
        self._files_map = {}
        self._poll = select.epoll()
        self._read_mask = select.EPOLLIN | select.EPOLLPRI
        self._write_mask = select.EPOLLOUT


class KQueueIOWait(object):

    available = hasattr(select, 'kqueue')

    def __init__(self):
        self._files_map = {}
        self._kqueue = select.kqueue()

    def watch(self, fileobj, read=False, write=False):
        if not (read or write):
            raise ValueError('either read or write must be specified')

        if hasattr(fileobj, 'fileno'):
            fileno = fileobj.fileno()
        else:
            fileno = fileobj

        files_map = self._files_map
        try:
            del files_map[fileno]
        except KeyError:
            pass

        kevents = []
        if read:
            kevents.append(select.kevent(
                fileno, select.KQ_FILTER_READ,
                select.KQ_EV_ADD | select.KQ_EV_ONESHOT))
        if write:
            kevents.append(select.kevent(
                fileno, select.KQ_FILTER_WRITE,
                select.KQ_EV_ADD | select.KQ_EV_ONESHOT))

        files_map[fileno] = (fileobj, kevents)

    def unwatch(self, fileobj):
        if hasattr(fileobj, 'fileno'):
            fileno = fileobj.fileno()
        else:
            fileno = fileobj
        del self._files_map[fileno]

    def wait(self, timeout=None):
        files_map = self._files_map
        if not files_map:
            raise ValueError('no file descriptors registered')

        # Build the changelist for the kqueue object.
        changelist = []
        for fileobj, kevents in files_map.itervalues():
            changelist.extend(kevents)

        # Call kqueue() and destroy the changelist.
        kqueue_result = self._kqueue.control(
            changelist, len(changelist), timeout)
        del changelist

        # Merge the kevents that share the same ident.
        kevents_merged = {}
        KQ_FILTER_READ = select.KQ_FILTER_READ
        for kevent in kqueue_result:
            value = kevents_merged.setdefault(kevent.ident, [False, False])
            if kevent.filter == KQ_FILTER_READ:
                value[0] = True
            else:
                value[1] = True
        del kqueue_result

        # Build and return the result.
        return [
            (files_map[fileno][0], read, write)
            for fileno, (read, write) in kevents_merged.iteritems()]


# Define IOWait.
if EPollIOWait.available:
    IOWait = EPollIOWait
elif KQueueIOWait.available:
    IOWait = KQueueIOWait
elif PollIOWait.available:
    IOWait = PollIOWait
else:
    IOWait = SelectIOWait
