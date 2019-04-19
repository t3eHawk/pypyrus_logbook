from .formatter import Formatter

class Header():
    """
    This class represents logger header which used to record the most significant
    variables from application process. All that variables consolidated
    to internal data dictionary where key is a name of variable and its value
    is a variable meaning.
    """
    def __init__(self, logger, *args, length=80, div='*', **kwargs):
        self.logger = logger
        self._used = False
        self.length = logger.formatter.length
        self.div = logger.formatter.div
        self.data = {
            'app': logger.sysinfo.stat['app'],
            'desc': logger.sysinfo.stat['desc'],
            'version': logger.sysinfo.stat['version'],
            'hostname': logger.sysinfo.stat['hostname'],
            'ip': logger.sysinfo.stat['ip'],
            'user': logger.sysinfo.stat['user'],
            'pid': logger.sysinfo.stat['pid'],
            'system': logger.sysinfo.stat['system'],
            'python': logger.sysinfo.stat['python'],
            'pyexe': logger.sysinfo.stat['pyexe'],
            'script': logger.sysinfo.stat['script'],
            'compiler': logger.sysinfo.stat['compiler'],
            'pip': logger.sysinfo.stat['pip'],
            'loctime': logger.sysinfo.stat['loctime']
        }
        if args or kwargs:
            self.add(**kwargs)
            self.delete(*args)
        pass

    def create(self):
        """Main method to build formatted header in the form of string."""
        self._used = True
        ln_out, ln_in, ln_name, ln_value = self._calc_len()
        div = self.div
        data = self.data
        lines = []

        frame_format = '{div}{content:{filler}<{ln_in}}{div}\n'
        all = dict(div=div, ln_in=ln_in)

        top = frame_format.format(content='', filler=div, **all)
        top += frame_format.format(content='', filler='', **all)
        lines.append(top)

        content_format = '{name:>{ln_name}}: {value}'
        for d_name, d_value in data.items():
            name = d_name.upper()
            value = d_value
            content = content_format.format(
                name=name, ln_name=ln_name, value=value)
            frame = frame_format.format(content=content, filler='', **all)
            lines.append(frame)

        bottom = frame_format.format(content='', filler='', **all)
        bottom += frame_format.format(content='', filler=div, **all)
        lines.append(bottom)

        return ''.join(lines)

    def add(self, pos='start', **kwargs):
        """
        Add the variable to the data dictionary.
        Parameters:
        pos
            Describing the position of new variables in the data dictionary.
            Use "start" to insert values on top and "end" to use them on bottom.
        """
        if pos == 'start':
            self.data = {**kwargs, **self.data}
        elif pos == 'end':
            self.data = {**self.data, **kwargs}
        pass

    def delete(self, *args):
        """Delete some variables from the data dictionary to not show them."""
        for arg in args:
            del self.data[arg]
        pass

    def refresh(self):
        """Update dynamic data variables."""
        if hasattr(self, 'data') is True:
            if self.data.get('loctime') is not None:
                self.data['loctime'] = self.logger.sysinfo.stat['loctime']
        pass

    def _calc_len(self):
        """Calculate all lengths used in header formatting."""
        ln_out = self.length
        ln_in = ln_out - 2
        ln_name = max([len(key) for key in self.data.keys()]) + 3
        ln_value = ln_in - ln_name
        return (ln_out, ln_in, ln_name, ln_value)

    @property
    def used(self):
        """Flag to define whether header was used or not."""
        return self._used
