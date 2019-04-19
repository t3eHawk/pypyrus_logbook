
class Formatter():
    """Class represents object's formats."""
    def __init__(self, record=None, error=None, length=80, div='*'):
        def_record = '{isotime}\t{rectype}\t{message}\n'
        def_error = '{err_name}\t{err_value}\t{err_file}\t{err_line}\t{err_obj}'

        record = record or def_record
        error = def_error if error is None else error

        self.configure(record=record, error=error, length=length, div=div)
        pass

    def configure(self, record=None, error=None, length=None, div=None):
        if record is not None: self.record = record
        if error is not None: self.error = error
        if length is not None: self.length = length
        if div is not None: self.div = div
        pass

    # def _set_pattern(self, pattern=None):
    #     """Initialize the pattern."""
    #     if pattern is not None:
    #         self.pattern = str(pattern)
    #         # Test pattern on unknown forms.
    #         used_forms = re.findall(r'{.*?[}|:]', self.pattern)
    #         for form in used_forms:
    #             name_form = form[1:-1]
    #             str_w_form = f'{{{name_form}}}'
    #             try:
    #                 str_w_form.format(**self.forms)
    #             except KeyError:
    #                 self._set_forms(name_form)
    #     elif hasattr(self, 'pattern') is False:
    #         self.pattern = ''
    #     pass
    #
    # def _set_forms(self, *args, **kwargs):
    #     """
    #     Initialize the forms.
    #     If the variable is ordered then add it with "None" value.
    #     Used mostly for the cases when the pattern include unknown forms to
    #     prevent errors.
    #     """
    #     if args:
    #         for arg in args:
    #             self.forms[arg] = 'NONE'
    #     if kwargs:
    #         for key, value in kwargs.items():
    #             if value is None:
    #                 value = 'NONE'
    #             self.forms[key] = value
    #     pass
