# Copyright (c) 2015, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.

from .basebyteaccess import BaseByteAccess
from mmap import mmap

def open_file(filepath):
    """Define a ByteAccess for reading and writing to a specific file.

    filepath -- Full path to the file which will be opened.

    Usage:
        ByteAccess = byteaccess_for_file('test.bin')
        foo = ByteAccess(offset, size)
        bar = ByteAccess(other_offset, other_size)
    """

    class FileByteAccess(BaseByteAccess):

        """Read/write bytes to a file on disk."""

        file_handle = open(filepath, 'r+b')
        mmap_f = mmap(file_handle.fileno(), 0)

        @classmethod
        def close(self):
            """Close the file and invalidate all child ByteAccesses."""
            FileByteAccess.mmap_f.close()
            FileByteAccess.file_handle.close()

        def _read_bytes(self, offset, size):
            begin = self.offset + offset
            end = begin + size
            buf = FileByteAccess.mmap_f[begin:end]

            if len(buf) != size:
                raise RuntimeError(('requested {} bytes but got only buffer:{}\n' +
                                    '    begin:{} end:{}' +
                                    '    offset:{} self.offset:{}')
                                    .format(size, buf, begin, end,
                                            offset, self.offset))
            return buf

        def _write_bytes(self, offset, to_write):
            begin = self.offset + offset
            end = begin + len(to_write)
            self.mmap_f[begin:end] = to_write

    return FileByteAccess
